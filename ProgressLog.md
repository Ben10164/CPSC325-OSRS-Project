# Project Log

This is the Progress Log for the project. Here is the [previous log](https://github.com/Ben10164/CPSC325-Research/blob/main/ProgressLog.md) for the Project Research.

## NameIDHelper

See [NameIDHelper](NameIDHelper.ipynb)

## DateTimeHelper

See [DateTimeTest](DateTimeTest.ipynb)

## Started the App

See [App.py](App.py)

The application was created using streamlit since it seemed easy and I have never done any form of web interface developement.

Currently you can search for items and view the graph and table for said item.

### ChartHelper

[ChartHelper.py](ChartHelper.py) is a module I made that focuses on creating a very simple altair chart. This chart is then used in `App.py` for displaying the graph.

The reason I decided to create my own graphs rather than use the built in `st.line_chart()` was because the built in function would not scale the y-axis properly. After doing some research and forum browsing, people seemed to recommend using `st.altair_chart()`, since thats what `st_line_chart()` is built on, and allows for more customization.

## Ideas

This is a folder that I made that I will use as a place to test certain things. This reduces clutter of the main repo.

### skforecast

See [skforecast.pynb](Ideas/skforecast.ipynb)

This seemed to be a very simple way to get started with a model for datetime formatted dataframe/series. However, it did not go very well.

I am not very familiar with any machine learning algorithms such as Tensorflow, so I decided to use a scikit inspired (maybe official branch) package.

Lets just say it was very inaccurate. The notebook goes over the results.
