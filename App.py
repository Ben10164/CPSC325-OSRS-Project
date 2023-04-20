import streamlit as st

import DateTimeHelper
import ChartHelper
import Ideas.PredictorTest as PredictorTest
import Predictor
import pandas as pd



def get_predictor(ITEM, DELTA):
    test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]
    model = Predictor.get_model(MAX_EPOCHS=200,
                                PATIENCE=400,
                                normalize=False,
                                ITEM=ITEM,
                                # ITEM="Twisted bow",
                                # ITEM="Osmumten's fang",
                                INPUT_WIDTH=30,
                                LABEL_WIDTH=30,
                                CONV_WIDTH=30,
                                LABEL_COLUMNS=['average',
                                            'avgHighPrice', 'avgLowPrice'],
                                #    MODEL="Linear",
                                MODEL="Conv1D",
                                DELTA=DELTA)


name = st.text_input("Input the item name", placeholder="Twisted bow")
prediction_delta = st.selectbox('choose how far forward in the future you want. (Limited for now)', ['1h' , '6h'])


  ## Range selector
historical = st.checkbox("Include historical values in the graph? (Performance decrease when start date is further from the present)", value=False)


if len(name) != 0:
    data = Predictor.get_data(name, prediction_delta)

    cols1,_ = st.columns((1,2)) # To make it narrower
    format = 'MMM DD, YYYY'  # format output
    if(historical):
        start_date = data.index[-366]
        end_date = data.index[0]   
    else:
        start_date = data.index[-1]
        end_date = data.index[-365]


    slider = cols1.slider('Select the start date of the graph', max_value=start_date.to_pydatetime(), value=end_date.to_pydatetime() ,min_value=end_date.to_pydatetime(), format=format)

    # len = st.slider(label="# of datapoints (Large values cause performance issues)",max_value=data.index[-1], format='dddd, MMMM Do YYYY, h:mm:ss a', key=data.index)
    # len = st.slider(label="# of datapoints (Large values cause performance issues)")
    ChartHelper.get_altair_chart(data.loc[pd.to_datetime(slider):].reset_index(),name)
    st.write(data)


    model = Predictor.get_model(ITEM=name, DELTA=prediction_delta)
    test_df = DateTimeHelper.getDT(name, prediction_delta)[-30:]
    te = Predictor.predict(model, test_df)
    st.write(te)

    # ChartHelper.get_sam_altair_chart(PredictorTest.getNeatGraph(name, time),name)
    # get_predictor(name, prediction_delta)


# # st.write(PredictorTest.data)