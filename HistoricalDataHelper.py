import json
import os
import time
from datetime import datetime
from urllib.request import Request, urlopen

import pandas as pd
from dateutil.relativedelta import relativedelta

import NameIDHelper

# 6h - 21600
# 1h - 3600
# 5m - 300


def get_prices_at_time(delta, curr_time: float):
    url = 'https://prices.runescape.wiki/api/v1/osrs/'
    url += str(delta)
    url += "?timestamp="
    if (delta == '5m'):
        url += str(int(curr_time - (curr_time % 300)))
    elif (delta == '1h'):
        url += str(int(curr_time - (curr_time % 3600)))
    elif (delta == '6h'):
        url += str(int(curr_time - (curr_time % 21600)))
    else:
        ValueError()

    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
        'User-Agent': 'Storing Past Data - @Be#9998',
    }
    req = Request(url, headers=headers)

    with urlopen(req) as response:
        latestData = response.read()
    data = json.loads(latestData)
    return data['data']


def get_historical_API(delta, id, start_time=None):
    times = {}
    if (start_time is None):
        temp = datetime.now() - relativedelta(month=6)
        t = temp.timestamp()
    else:
        t = start_time

    two_yrs_ago = datetime.now() - relativedelta(years=2)
    counter = 0
    while (t > two_yrs_ago.timestamp()):
        time_df = get_prices_at_time(delta, t)
        label = 0
        if (delta == '5m'):
            label = str(int(t - (t % 300)))
        elif (delta == '1h'):
            label = str(int(t - (t % 3600)))
        elif (delta == '6h'):
            label = str(int(t - (t % 21600)))
        # times[label] = df_json
        if (delta == '6h'):
            t = t-(21600*4)
        elif (delta == '1h'):
            t = t-3600
        elif (delta == '5m'):
            t = t-300
        else:
            ValueError()
        try:
            times[label] = time_df[str(id)]
        except:
            counter += 1
            print("No info for timestamp",t, " continuing until 10 in a row with no info:",counter,"/10")
            if(counter >= 10): # if there are 10 instances in a row with no item 
                break
        time.sleep(0.1)
    if time == {}:
        return None
    else:
        return times


def create_historical(name):
    id = NameIDHelper.NameToID(name)
    print("id is ", id)
    try:
        historical_time = get_historical_API('6h', id, datetime.now().timestamp() - (21600*365))

        try:
            f = open('Data/Historical/' + str(id) + '.json', 'w')
        except:
            try:
                os.mkdir('Data')
            except:
                os.mkdir('Data/Historical')
            f = open('Data/Historical/' + str(id) + '.json', 'w')
        f.write(json.dumps(historical_time, indent=4))
        f.close()
    except:
        return IndexError()


def get_historical(name):
    id = NameIDHelper.NameToID(name)
    fpath = "Data/Historical/" + str(id) + ".json"
    try:
        df = pd.read_json(fpath)
    except:
        create_historical(name)
        df = pd.read_json(fpath)
    return df