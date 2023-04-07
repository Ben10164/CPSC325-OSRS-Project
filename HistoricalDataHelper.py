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
    # we want the latest data, so lets add that to the url
    url += str(delta)
    url += "?timestamp="
    # url += today.strftime("%f")
    if (delta == '5m'):
        url += str(int(curr_time - (curr_time % 300)))
    elif (delta == '1h'):
        url += str(int(curr_time - (curr_time % 3600)))
    elif (delta == '6h'):
        url += str(int(curr_time - (curr_time % 21600)))
    else:
        ValueError()

    print(url)
    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
        'User-Agent': 'Storing Past Data- @Be#9998',
    }
    req = Request(url, headers=headers)

    with urlopen(req) as response:
        latestData = response.read()
    data = json.loads(latestData)

    data['data']
    return data['data']


def test(delta, start_time=None):
    times = {}
    if (start_time is None):
        t = time.time()
    else:
        t = start_time

    two_yrs_ago = datetime.now() - relativedelta(years=1)
    # two_yrs_ago = datetime.now() - relativedelta(years=1)
    while (t > two_yrs_ago.timestamp()):
        time_df = get_prices_at_time(delta, t)
        # df = pd.DataFrame.from_dict(time_df)
        # df = df.transpose()
        # df_json = df.to_json()
        # print(df_json)
        label = 0
        if (delta == '5m'):
            label = str(int(t - (t % 300)))
        elif (delta == '1h'):
            label = str(int(t - (t % 3600)))
        elif (delta == '6h'):
            label = str(int(t - (t % 21600)*4))  # once a day
        # times[label] = df_json
        times[label] = time_df
        if (delta == '6h'):
            t = t-21600
        elif (delta == '1h'):
            t = t-3600
        elif (delta == '5m'):
            t = t-300
        else:
            ValueError()
        time.sleep(0.1)
    return times


def test2(delta, id, start_time=None):
    times = {}
    if (start_time is None):
        temp = datetime.now() - relativedelta(month=6)
        t = temp.timestamp()
    else:
        t = start_time

    print(t)

    two_yrs_ago = datetime.now() - relativedelta(years=2)
    # two_yrs_ago = datetime.now() - relativedelta(years=1)
    while (t > two_yrs_ago.timestamp()):
        time_df = get_prices_at_time(delta, t)
        # df = pd.DataFrame.from_dict(time_df)
        # df = df.transpose()
        # df_json = df.to_json()
        # print(df_json)
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
            print("To soon to current date to retrieve historical data (probably)")

            continue
        time.sleep(0.1)
    return times


def create_historical(name):
    id = NameIDHelper.NameToID(name)
    print(id)
    try:
        # historical_time = test('6h', 1652175674)
        # historical_time = test2('6h', id)
        historical_time = test2(
            '6h', id, datetime.now().timestamp() - (21600*365))

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
