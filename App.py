import streamlit as st

import DateTimeHelper
import ChartHelper
import Ideas.PredictorTest as PredictorTest

name = st.text_input("Input the item name", placeholder="Twisted bow")
time = st.selectbox('choose what time delta you want.', ['5m', '1h' , '6h'])

if len(name) != 0:
    data = DateTimeHelper.getDT(name , time)
    ChartHelper.get_altair_chart(data.reset_index(),name)
    # st.write(data)
    ChartHelper.get_sam_altair_chart(PredictorTest.getNeatGraph(name, time),name)

# st.write(PredictorTest.data)
 
