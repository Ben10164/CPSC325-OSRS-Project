import streamlit as st

import DateTimeHelper
import ChartHelper
import Predictor
import pandas as pd
import tensorflow as tf

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    initial_sidebar_state="collapsed"
)

def convert_tf_to_pd(ds, limit=32):
    """
    Read data from Tensorflow dataset to Pandas dataframe
    :param ds:
    :param limit:
    :return:
    """
    batch_iterator = ds.batch(limit).make_one_shot_iterator()
    with tf.Session() as sess:
        batch = batch_iterator.get_next()
        features_and_labels = sess.run(batch)
        samples = {
            **features_and_labels[0],
            'label': features_and_labels[1],
        }

    return pd.DataFrame.from_dict(samples)


name = st.selectbox('Chose the Mega-Rare BIS item to view trading info for', ['Twisted bow' , 'Scythe of vitur (uncharged)', 'Tumeken\'s shadow (uncharged)'], label_visibility="visible")
prediction_delta = st.selectbox('Delta used in Model and Data Display', ['1h' , '6h'])

  ## Range selector
historical = st.checkbox("Include historical values in the graph? (Performance decrease when start date is further from the present)", value=False)
if(historical):
    view_delta = '6h'
else:
    view_delta = prediction_delta

if len(name) != 0:
    data = Predictor.get_data(name, view_delta)

    cols1,_ = st.columns((1,2)) # To make it narrower
    format = 'MMM DD, YYYY'  # format output
    if(historical):
        start_date = data.index[-366]
        end_date = data.index[2]   
    else:
        start_date = data.index[-2]
        end_date = data.index[-365]

    slider = cols1.slider('Select the start date of the graph', max_value=start_date.to_pydatetime(), value=end_date.to_pydatetime() ,min_value=end_date.to_pydatetime(), format=format)

    # len = st.slider(label="# of datapoints (Large values cause performance issues)",max_value=data.index[-1], format='dddd, MMMM Do YYYY, h:mm:ss a', key=data.index)
    # len = st.slider(label="# of datapoints (Large values cause performance issues)")
    """
    # Current Data
    """
    ChartHelper.get_altair_chart(data.loc[pd.to_datetime(slider):].reset_index(),name)

    MODEL = st.selectbox('Chose the Model to predict with', [None, 'Conv1D' , 'Linear', 'Multi_Step_Dense'], label_visibility="visible")
    """
    Note:  
    Conv1D is the only model that predicts more than 1 step in the future. If you would like to use a Linear or Multi_Step_Dense model to predict, the value of Delta is how far in the future it will predict.
    """
    if(MODEL is not None):
        model = Predictor.get_model(ITEM=name, DELTA=prediction_delta, MODEL=MODEL)
        test_df = DateTimeHelper.getDT(name, prediction_delta)[-30:]
        te = Predictor.predict(model, test_df)
        # st.write(te)


        """
        # Predicted Data
        """
        ChartHelper.get_altair_chart(data.loc[pd.to_datetime(slider):].reset_index(),name, te.numpy()[0][0])


    # ChartHelper.get_sam_altair_chart(PredictorTest.getNeatGraph(name, time),name)
    # get_predictor(name, prediction_delta)


# # st.write(PredictorTest.data)