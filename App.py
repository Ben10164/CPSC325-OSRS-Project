import streamlit as st

import DateTimeHelper
import ChartHelper
import Ideas.PredictorTest as PredictorTest
import Predictor



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
time = st.selectbox('choose what time delta you want.', ['1h' , '6h'])
prediction_delta = st.selectbox('choose how far forward in the future you want. (Limited for now)', ['1h' , '6h'])


name = 'Twisted bow'
prediction_delta = '1h'
data = Predictor.get_data(name, prediction_delta)
ChartHelper.get_altair_chart(data.reset_index(),name)
st.write(data)

t = Predictor.get_model(ITEM=name, DELTA=prediction_delta)


test_df = DateTimeHelper.getDT(name, prediction_delta)[-30:]
te = Predictor.predict(t, test_df)
st.write(te)

# if len(name) != 0:
#     data = Predictor.get_data(name, prediction_delta)
#     ChartHelper.get_altair_chart(data.reset_index(),name)
#     st.write(data)
#     # ChartHelper.get_sam_altair_chart(PredictorTest.getNeatGraph(name, time),name)
#     # get_predictor(name, prediction_delta)


# # st.write(PredictorTest.data)