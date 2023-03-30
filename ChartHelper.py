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
            x="timestamp:T",
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
    return (lines + points + tooltips).interactive()


def get_altair_chart(data, title):
    chart = get_chart(data, title)
    st.altair_chart(chart.interactive(),use_container_width=True)
