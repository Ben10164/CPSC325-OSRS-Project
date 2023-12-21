import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import DateTimeHelper as help
import NameIDHelper
from urllib.request import Request, urlopen
from datetime import datetime
import json
import pandas as pd


def hm(name, timestep):
    url = "https://prices.runescape.wiki/api/v1/osrs"
    # we want the latest data, so lets add that to the url
    url += "/timeseries?timestep="
    url += timestep
    url += "&id="
    # lets add the abyssal whip to the url:
    url += str(NameIDHelper.NameToID(name))

    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
        "User-Agent": "Accessing Past 365 6h times - @Be#9998",
    }
    req = Request(url, headers=headers)

    with urlopen(req) as response:
        latestData = response.read()
    data = json.loads(latestData)

    for date in data["data"]:
        date["timestamp"] = datetime.utcfromtimestamp(date["timestamp"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    data = data["data"]

    dt_pandas = pd.DataFrame(data)
    dt_pandas = dt_pandas.set_index("timestamp")


tmp = hm("Twisted bow", "6h")
print(tmp)
