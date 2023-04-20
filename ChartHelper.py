import streamlit as st
import altair as alt

# Define the base time-series chart.


def get_chart(data, title):
    hover = alt.selection_single(
        fields=["timestamp"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x=alt.X("timestamp:T"),
            # x=alt.X("timestamp:T", scale=alt.Scale(domainMin=data.iloc[data.index[-30]]['timestamp'] )),
            # x=alt.X("timestamp:T", scale=alt.Scale(domain=[data.iloc[data.index[-30]]['timestamp'], data.iloc[data.index[-3]]['timestamp']])),
            y=alt.Y("average", scale=alt.Scale(zero=False)),
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="timestamp:T",
            y="average",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("utcmonthdate(timestamp):T", title="Date"),
                alt.Tooltip("utchoursminutes(timestamp):T", title="Time"),
                alt.Tooltip("average:Q", title="Price (GP)"),
            ],
        )
        .add_selection(hover)
    )
    chart = (lines + points + tooltips).interactive()
    return chart



def get_sam_chart(data, title):
    hover = alt.selection_single(
        fields=["timestamp"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x="timestamp:T",
            y=alt.Y("average", scale=alt.Scale(zero=False)),
            color=alt.value('red')
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="timestamp:T",
            y="average",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("utcmonthdate(timestamp):T", title="Date"),
                alt.Tooltip("utchoursminutes(timestamp):T", title="Time"),
                alt.Tooltip("average:Q", title="Price (GP)"),
            ],
        )
        .add_selection(hover)
    )

    deltaStuff = []
    on = (data['nextDeltaInc'][0] == 1)
    if on:
        curr_start = 0
    for idx in range(len(data['nextDeltaInc'])):
        if(on):
            if data['nextDeltaInc'][idx] != 1:
                deltaStuff.append({"start": data['timestamp'][curr_start], "end": data['timestamp'][idx]})
                on = False
        else:
            if data['nextDeltaInc'][idx] == 1:
                on = True
                curr_start = idx

    # st.write(deltaStuff)
    # st.write(deltaStuff[:10])
    import pandas as pd
    rect = alt.Chart(pd.DataFrame(deltaStuff)).mark_rect().encode(
        x="start:T",
        x2="end:T", 
        color=alt.value('grey')
    )
    return (rect + lines + points + tooltips).interactive()


def get_sam_altair_chart(data, title):
    chart = get_sam_chart(data.reset_index(), title)
    st.altair_chart(chart.interactive(),use_container_width=True)

def get_altair_chart(data, title):
    chart = get_chart(data, title)
    st.altair_chart(chart.interactive(),use_container_width=True)
