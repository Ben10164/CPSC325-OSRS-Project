import streamlit as st

import DateTimeHelper
import ChartHelper

name = st.text_input("Input the item name", placeholder="Twisted bow")
time = st.selectbox('choose what time delta you want.', ['5m', '1h' , '6h'])

if len(name) != 0:
    data = DateTimeHelper.getDT(name , time)
    ser = DateTimeHelper.getSeries(name, time)
    ChartHelper.get_altair_chart(data.reset_index(),name)
    st.write(data)



