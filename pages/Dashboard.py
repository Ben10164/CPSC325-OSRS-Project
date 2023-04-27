import streamlit as st
import streamlit.components.v1 as components

import DateTimeHelper
import ChartHelper
import Predictor
import pandas as pd
import tensorflow as tf

st.set_page_config(
    page_title="Dashboard",
    page_icon="✅",
    layout="wide",
)

prediction_delta = st.selectbox('Delta used in Model and Data Display', ['1h' , '6h'])

MODEL = 'Conv1D'
charts = []
def hm(name):
    data = Predictor.get_data(name, prediction_delta)
    if(MODEL is not None):
        model = Predictor.get_model(ITEM=name, DELTA=prediction_delta, MODEL=MODEL)
        test_df = DateTimeHelper.getDT(name, prediction_delta)[-30:]
        te = Predictor.predict(model, test_df)
        charts.append(ChartHelper.get_dashboard_chart(data.loc[data.index.values[-30]:].reset_index(),name, te.numpy()[0][0], False))


    # ChartHelper.get_sam_altair_chart(PredictorTest.getNeatGraph(name, time),name)
    # get_predictor(name, prediction_delta)


    # # st.write(PredictorTest.data)

hm("Twisted bow")
hm("Scythe of vitur (uncharged)")
hm("Tumeken\'s shadow (uncharged)")

c1, c2, c3 =  st.columns(3)
with c1:
    st.altair_chart(charts[0].interactive(),use_container_width=True)
    components.html(
    """
    <a class="twitter-timeline" data-height="1000" href="https://twitter.com/OldSchoolRS?ref_src=twsrc%5Etfw">Tweets by OldSchoolRS</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """, height=500
    )
with c2:
    st.altair_chart(charts[1].interactive(),use_container_width=True)
    components.html(
    """
    <a class="twitter-timeline" data-height="1000" href="https://twitter.com/OSRS_Wiki?ref_src=twsrc%5Etfw">Tweets by OSRS_Wiki</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """, height=500
    )
with c3:
    st.altair_chart(charts[2].interactive(),use_container_width=True)