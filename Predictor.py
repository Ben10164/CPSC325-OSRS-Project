import HistoricalDataHelper
import DateTimeHelper
import tensorflow as tf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def get_model(MAX_EPOCHS=20000, 
         PATIENCE=400, 
         normalize=False, 
         ITEM="Twised bow", 
         INPUT_WIDTH=30, 
         LABEL_WIDTH=30, 
         CONV_WIDTH=30, 
         LABEL_COLUMNS=['average', 'avgHighPrice', 'avgLowPrice'],
         MODEL="Conv1D"):    
    """Returns a tensorflow model.

    Args:
        MAX_EPOCHS (int, optional): The maximum amount of Epochs used while training. Defaults to 20000.
        PATIENCE (int, optional): The patience value used while training the model. Defaults to 400.
        normalize (bool, optional): Normalize the values (False recommended). Defaults to False.
        ITEM (str, optional): The Item. Defaults to "Twisted bow".
        INPUT_WIDTH (int, optional): The input width for the window. Defaults to 30.
        LABEL_WIDTH (int, optional): The label width for the window. Defaults to 30.
        CONV_WIDTH (int, optional): The width of the Conv window. Defaults to 30.
        LABEL_COLUMNS (list, optional): The labels of the columns used for training. Defaults to ['average', 'avgHighPrice', 'avgLowPrice'].
        MODEL (str, optional): The wanted model ("Linear", "Multi_Step_Dense", "Conv1D). Defaults to "Conv1D".

    Returns:
        Tensorflow Model: The model
        pd.Dataframe: train_df
        pd.Dataframe: val_df
        pd.Dataframe: test_df
        int, CONV_WIDTH

    """
    model_location = 'Models/'+str(ITEM)
    model_location = model_location.replace(" ", "_")

    mpl.rcParams['figure.figsize'] = (8, 6)
    mpl.rcParams['axes.grid'] = False
    df = DateTimeHelper.getDT(ITEM, "6h")

    # import the Historical data
    test = HistoricalDataHelper.get_historical(ITEM)

    if not test.empty:
        test = test.transpose()
        test = test[['avgHighPrice', 'avgLowPrice',
                     'highPriceVolume', 'lowPriceVolume']]
        test = DateTimeHelper.addAverage(test)
        test.index.name = "timestamp"
        # now we append the historical data to the curr data
        # df = df.append(test)
        df = pd.concat([df, test])
        df

    df2 = df.copy()

    layer = tf.keras.layers.Normalization(invert=True)
    layer.adapt(df)

    df = DateTimeHelper.addAverage(df)

    if (normalize):
        df = tf.keras.utils.normalize(df)

    column_indices = {name: i for i, name in enumerate(df.columns)}

    df = df.reset_index()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    df = df.sort_index()

    n = len(df)
    train_df = df[0:int(n*0.7)]
    val_df = df[int(n*0.7):int(n*0.9)]
    test_df = df[int(n*0.9):]
    og_test_df = df2[int(n*0.9):]

    num_features = df.shape[1]

    class WindowGenerator():
        def __init__(self, input_width, label_width, shift,
                     train_df=train_df, val_df=val_df, test_df=test_df,
                     label_columns=None):
            # Store the raw data.
            self.train_df = train_df
            self.val_df = val_df
            # self.test_df = test_df

            # Work out the label column indices.
            self.label_columns = label_columns
            if label_columns is not None:
                self.label_columns_indices = {name: i for i, name in
                                              enumerate(label_columns)}
            self.column_indices = {name: i for i, name in
                                   enumerate(train_df.columns)}

            # Work out the window parameters.
            self.input_width = input_width
            self.label_width = label_width
            self.shift = shift

            self.total_window_size = input_width + shift

            self.input_slice = slice(0, input_width)
            self.input_indices = np.arange(self.total_window_size)[
                self.input_slice]

            self.label_start = self.total_window_size - self.label_width
            self.labels_slice = slice(self.label_start, None)
            self.label_indices = np.arange(self.total_window_size)[
                self.labels_slice]

        def __repr__(self):
            return '\n'.join([
                f'Total window size: {self.total_window_size}',
                f'Input indices: {self.input_indices}',
                f'Label indices: {self.label_indices}',
                f'Label column name(s): {self.label_columns}'])

    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:, :, self.column_indices[name]]
                    for name in self.label_columns],
                axis=-1)

        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    WindowGenerator.split_window = split_window

    def plot(self, model=None, plot_col='average', max_subplots=5):
        inputs, labels = self.example
        plt.figure(figsize=(12, 8))
        plot_col_index = self.column_indices[plot_col]
        max_n = min(max_subplots, len(inputs))
        for n in range(max_n):
            plt.subplot(max_n, 1, n+1)
            plt.ylabel(f'{plot_col} [normed]')
            plt.plot(self.input_indices, inputs[n, :, plot_col_index],
                     label='Inputs', marker='.', zorder=-10)

            if self.label_columns:
                label_col_index = self.label_columns_indices.get(
                    plot_col, None)
            else:
                label_col_index = plot_col_index

            if label_col_index is None:
                continue

            plt.scatter(self.label_indices, labels[n, :, label_col_index],
                        edgecolors='k', label='Labels', c='#2ca02c', s=64)
            if model is not None:
                predictions = model(inputs)
                plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                            marker='X', edgecolors='k', label='Predictions',
                            c='#ff7f0e', s=64)

            if n == 0:
                plt.legend()

        plt.xlabel('Time [h]')

    WindowGenerator.plot = plot

    def make_dataset(self, data):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.utils.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=32,)

        ds = ds.map(self.split_window)

        return ds

    WindowGenerator.make_dataset = make_dataset

    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df)

    @property
    def example(self):
        """Get and cache an example batch of `inputs, labels` for plotting."""
        result = getattr(self, '_example', None)
        if result is None:
            # No example batch was found, so get one from the `.train` dataset
            result = next(iter(self.train))
            # And cache it for next time
            self._example = result
        return result

    WindowGenerator.train = train
    WindowGenerator.val = val
    WindowGenerator.test = test
    WindowGenerator.example = example

    def compile_and_fit(model: tf.keras.models.Sequential, window, patience=PATIENCE):
        # Include the epoch in the file name (uses `str.format`)
        #   checkpoint_path = "Models/cp.ckpt"
        checkpoint_path = model_location + "/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)

        batch_size = 32

        # Create a callback that saves the model's weights every  MAX_EPOCHS/10 epochs
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path,
            verbose=1,
            save_weights_only=True,
            save_freq=int(MAX_EPOCHS/10))

        early_stopping1 = tf.keras.callbacks.EarlyStopping(monitor='loss',
                                                           patience=patience,
                                                           start_from_epoch=MAX_EPOCHS/5,
                                                           mode='min')
        early_stopping2 = tf.keras.callbacks.EarlyStopping(monitor='mean_absolute_error',
                                                           patience=patience,
                                                           start_from_epoch=MAX_EPOCHS/5,
                                                           mode='min')
        model.compile(loss=tf.keras.losses.MeanSquaredError(),
                      optimizer=tf.keras.optimizers.legacy.Adam(),
                      metrics=[tf.keras.metrics.MeanAbsoluteError()])

        history = model.fit(window.train, epochs=MAX_EPOCHS,
                            validation_data=window.val,
                            callbacks=[early_stopping1, early_stopping2, cp_callback])
        return history

    window = WindowGenerator(
        input_width=INPUT_WIDTH, label_width=LABEL_WIDTH, shift=1,
        label_columns=LABEL_COLUMNS)

    conv_window = WindowGenerator(
        input_width=CONV_WIDTH,
        label_width=1,
        shift=1,
        label_columns=['average'])

    # LABEL_WIDTH = 24
    # INPUT_WIDTH = LABEL_WIDTH + (CONV_WIDTH - 1)
    wide_conv_window = WindowGenerator(
        input_width=LABEL_WIDTH + (CONV_WIDTH - 1),
        label_width=LABEL_WIDTH,
        shift=1,
        label_columns=['average'])

    def linear() -> tf.keras.Sequential:
        # linear
        linear = tf.keras.Sequential([
            tf.keras.layers.Dense(units=1)
        ])

        try:
            linear = tf.keras.models.load_model(model_location + "/Linear")
        except:
            history = compile_and_fit(linear, window)
        linear.save(model_location + "/Linear")
        return linear

    def msd() -> tf.keras.Sequential:
        multi_step_dense = tf.keras.Sequential([
            # Shape: (time, features) => (time*features)
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=32, activation='relu'),
            tf.keras.layers.Dense(units=32, activation='relu'),
            tf.keras.layers.Dense(units=1),
            # Add back the time dimension.
            # Shape: (outputs) => (1, outputs)
            tf.keras.layers.Reshape([1, -1]),
        ])
        try:
            multi_step_dense = tf.keras.models.load_model(
                model_location + "/Multi_Step_Dense")
        except:
            history = compile_and_fit(multi_step_dense, conv_window)
        multi_step_dense.save(model_location + "/Multi_Step_Dense")
        return multi_step_dense

    def conv1d() -> tf.keras.Sequential:
        conv_model = tf.keras.Sequential([
            tf.keras.layers.Conv1D(filters=32,
                                   kernel_size=(CONV_WIDTH,),
                                   activation='relu',
                                   input_shape=(None, 5)),
            tf.keras.layers.Dense(units=32, activation='relu'),
            tf.keras.layers.Dense(units=1),
        ])
        try:
            conv_model = tf.keras.models.load_model(
                model_location + '/Conv_model')
        except:
            history = compile_and_fit(conv_model, conv_window)
        conv_model.save(model_location + '/Conv_model')
        return conv_model
    
    if MODEL == 'Conv1D':
        return conv1d(), train_df, val_df, test_df, CONV_WIDTH
    elif MODEL == 'Multi_Step_Dense':
        return msd(), train_df, val_df, test_df, CONV_WIDTH
    else:
        return linear(), train_df, val_df, test_df, CONV_WIDTH


def predict(model, test_df):
    """Returns a prediction

    model (Conv1D Model): Must be a Conv1D model (for now)
    """
    # now we are going to create the test data:

    t = test_df.to_numpy()
    t_reshaped = t.reshape((1,-1,5)) 

    y_pred = model.predict(t_reshaped)

    # p = pd.DataFrame(y_pred[0])
    p =y_pred[0]

    return p