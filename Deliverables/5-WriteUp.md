# Project Log <!-- omit in toc -->

This is the final Progress Log / Write-up for the project. Here is the [previous log](https://github.com/Ben10164/CPSC325-Research/blob/main/ProgressLog.md) for the Project Research.

* [NameIDHelper](#nameidhelper)
* [DateTimeHelper](#datetimehelper)
* [ChartHelper](#charthelper)
* [Ideas](#ideas)
  * [skforecast](#skforecast)
* [Tensorflow, the breakthrough](#tensorflow-the-breakthrough)
* [Integrating with Streamlit](#integrating-with-streamlit)
* [Deploying](#deploying)
* [Testing](#testing)

## NameIDHelper

First I want the program to import some modules

```py
import requests
import pandas as pd
```

Now the program will read the locally stored json containing the mappings from ID to names

```py
# Creating df with json data instead of calling the API
# this is to lower the amount of calls needed for this helper function!
mapping_df = pd.read_json('Data/NameIDMap.json')
```

Now the program can drop some cols that wont be used for this

```py
# we are going to drop the useless cols that we wont be needing
mapping_df = mapping_df.drop(
    columns=['examine', 'lowalch', 'limit', 'value', 'highalch', 'icon', 'members'])
```

Now the program can directly create the two dicts (name->ID, ID->name)

```py
name_dict = mapping_df.set_index('name')['id'].to_dict()
id_dict = mapping_df.set_index('id')['name'].to_dict()
```

These are the actual helper functions that returns the result

```py
def NameToID(name):
    return name_dict[name]


def IdToName(id):
    return id_dict[id]
```

Although to minimize the amount of API calls the program uses a locally stored database, it is sometimes necessary to update the local database, a new update for example.

```py
# This function will update the locally stored JSON
def UpdateJson():
    url = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
    # we want the latest data, so lets add that to the url

    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord 
        # they asked me to include my discord in the user-agent
        'User-Agent': 'Item_ID_Helper_Functions - @Be#9998',
    }

    response_json = requests.get(url, headers=headers).text
    f = open('Data/NameIDMap.json', 'w')
    import json
    mydata = json.loads(response_json)
    f.write(json.dumps(mydata, indent=4))
    f.close()
```

## DateTimeHelper

Import everything needed

```py
import numpy as np
import NameIDHelper
from urllib.request import urlopen, Request
import json
from datetime import datetime
import pandas as pd
```

This function is used to replace all nan values while also adding an average col. This can be altered in the future to determine other ways of calculating averages

* there are many times for smaller items that dont have enough trade volume that have null for some of the values
* if this is the case i want to set the value equal to the other val:
  * highval = null, set highval = lowval
  * lowval = null, set lowval = highval
  * if both are null... remove row

```py
def addAverage(dt):
    # the volumes will still be there to calculate an average
    average = []
    for time in dt.values:
        averageVal = (time[3]*time[1] + time[2]*time[0]) / (time[3] + time[2])
        if (np.isnan(averageVal)):
            if time[0] == time[1]:
                # uh oh
                continue
            elif np.isnan(time[0]):
                averageVal = time[1]
            elif np.isnan(time[1]):
                averageVal = time[0]
        average.append(averageVal)
    dt['average'] = average
    return dt
```

This is a function that gets the DateTime formatted DataFrame

```py
def getDT(name,timestep):
    url = 'https://prices.runescape.wiki/api/v1/osrs'
    # we want the latest data, so lets add that to the url
    url += "/timeseries?timestep="
    url += timestep
    url += "&id="
    # lets add the abyssal whip to the url:
    url += str(NameIDHelper.NameToID(name))

    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
        'User-Agent': 'DateTimeHelper - @Be#9998',
    }
    req = Request(url, headers=headers)
    with urlopen(req) as response:
                latestData = response.read()
    data = json.loads(latestData)

    for date in data['data']:
        date['timestamp'] = datetime.utcfromtimestamp(date['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    data = data['data']
    
    dt_pandas = pd.DataFrame(data)
    dt_pandas = dt_pandas.set_index('timestamp')
    dt_pandas = addAverage(dt_pandas)
    dt_pandas.drop(columns=['lowPriceVolume', 'highPriceVolume'], inplace=True)
    return dt_pandas
```

## ChartHelper

[ChartHelper.py](../ChartHelper.py) is a module I made that focuses on creating a very simple altair chart. This chart is then used in `App.py` for displaying the graph.

The reason I decided to create my own graphs rather than use the built in `st.line_chart()` was because the built in function would not scale the y-axis properly. After doing some research and forum browsing, people seemed to recommend using `st.altair_chart()`, since thats what `st_line_chart()` is built on, and allows for more customization.

## Ideas

This is a folder that I made that I will use as a place to test certain things. This reduces clutter of the main repo.

### skforecast

See [skforecast.pynb](../Ideas/skforecast.ipynb)

This seemed to be a very simple way to get started with a model for datetime formatted dataframe/series. However, it did not go very well.

I am not very familiar with any machine learning algorithms such as Tensorflow, so I decided to use a scikit inspired (maybe official branch) package.

Lets just say it was very inaccurate. The notebook goes over the results.

## Tensorflow, the breakthrough

After discoving multiple extremely useful tensorflow examples of time series, progress picked up substantially.

See [Predictor.ipynb](3-Predictor.ipynb) for a notebook that shows my approach.

Although this took multiple weeks, the following are the main breakthroughs I had:

* Discovered Conv1D and Multi_Step_Dense models work very well will my dataset
  * Here is the model I focused on

    ```py
    def conv1d() -> tf.keras.Sequential:
        """Trains a 1-dimensional Convolution model and returns it. 

        Returns:
            tf.keras.Sequential: Conv1D
        """
        conv_model = tf.keras.Sequential([
            tf.keras.layers.Conv1D(filters=32,
                                kernel_size=(CONV_WIDTH,),
                                activation='relu',
                                input_shape=(None, 5)),
            tf.keras.layers.Dense(units=32, activation='relu'),
        ])
    ```

* Discovered saving and loading models in a smart way

    ```py
    try:
        conv_model = tf.keras.models.load_model(model_location + '/Conv_model-' + str(DELTA))
    except:
        history = compile_and_fit(conv_model, conv_window)
        conv_model.save(model_location + '/Conv_model-'+str(DELTA))
    return conv_model
    ```

* Discovered how to reshape input to be predicted

    ```py
    def predict(model : tf.keras.Sequential, test_df):
        """Returns a prediction

        model (Conv1D Model): Must be a Conv1D model (for now)
        """
        t = test_df.to_numpy()
        t_reshaped = t.reshape((1,-1,5)) 
        y_pred = model(t_reshaped)
        return y_pred
    ```

## Integrating with Streamlit

You can see that [App.py](../App.py) has been updated a lot

As the grand finale of this Progress Log, I will go through all the lines explaining them

First I just import everything I need

```py
import streamlit as st

import DateTimeHelper
import ChartHelper
import Predictor
import pandas as pd
import tensorflow as tf

# Next I get information from the user that will tell the program what to do

name = st.selectbox('Chose the Mega-Rare BIS item to view trading info for', ['Twisted bow' , 'Scythe of vitur (uncharged)', 'Tumeken\'s shadow (uncharged)'], label_visibility="visible")
prediction_delta = st.selectbox('Delta used in Model and Data Display', ['1h' , '6h'])
historical = st.checkbox("Include historical values in the graph? (Performance decrease when start date is further from the present)", value=False)
if(historical):
    view_delta = '6h'
else:
    view_delta = prediction_delta


# After the user has entered the information, the program starts the main portion

if len(name) != 0: # if the name has been selected

# Gets the data and formats it

    data = Predictor.get_data(name, view_delta)

# Here I handle how much data the graph shows (to make sure the website runs fast)

    cols1,_ = st.columns((1,2)) # To make it narrower
    format = 'MMM DD, YYYY'  # format output
    if(historical):
        start_date = data.index[-366]
        end_date = data.index[1]   
    else:
        start_date = data.index[-1]
        end_date = data.index[-365]
    slider = cols1.slider('Select the start date of the graph', max_value=start_date.to_pydatetime(), value=end_date.to_pydatetime() ,min_value=end_date.to_pydatetime(), format=format)

# Here I call my function to create the graph

    ChartHelper.get_altair_chart(data.loc[pd.to_datetime(slider):].reset_index(),name)

# I ask the user what model they want to use

    MODEL = st.selectbox('Chose the Model to predict with', [None, 'Conv1D' , 'Linear', 'Multi_Step_Dense'], label_visibility="visible")
    if(MODEL is not None):

# I get the model

        model = Predictor.get_model(ITEM=name, DELTA=prediction_delta, MODEL=MODEL)

# I create the data that will be passed into the model to predict the future

        test_df = DateTimeHelper.getDT(name, prediction_delta)[-30:]
        te = Predictor.predict(model, test_df)

# Graph the results

        ChartHelper.get_altair_chart(data.loc[pd.to_datetime(slider):].reset_index(),name, te.numpy()[0][0])
```

## Deploying

Deploying with streamlit was very VERY easy. It uses the git repo to get the code, and containerizes it on their servers, allowing for constant pulling of new data whenever a request is made.

## Testing

See [NameIDTest](1-NameIDTest.ipynb)

See [DateTimeTest](2-DateTimeTest.ipynb)

I also did alot of manual testing for the graphs and Streamlit deployment.
