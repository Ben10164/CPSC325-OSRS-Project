import json
import os
import time
from datetime import datetime
from urllib.request import Request, urlopen

import pandas as pd
from dateutil.relativedelta import relativedelta

import NameIDHelper

# looking back at this code, this is like really bad and confusing
#   im very sorry to people who are reading this.
#   in general, 'local' means stuff that is stored in the repo (usually git ignored)
# The idea is the local functions will just grab one massive heap of data,
#   and then do logic based around that now locally stored data

# 6h - 21600
# 1h - 3600
# 5m - 300


def get_prices_at_time(delta, curr_time: float):
    url = "https://prices.runescape.wiki/api/v1/osrs/"
    url += str(delta)
    url += "?timestamp="
    if delta == "5m":
        url += str(int(curr_time - (curr_time % 300)))
    elif delta == "1h":
        url += str(int(curr_time - (curr_time % 3600)))
    elif delta == "6h":
        url += str(int(curr_time - (curr_time % 21600)))
    else:
        ValueError()

    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
        "User-Agent": "Storing Past Data - @Be#9998",
    }
    req = Request(url, headers=headers)

    with urlopen(req) as response:
        latestData = response.read()
    data = json.loads(latestData)
    return data["data"]


def get_all_historical_API(delta):
    times = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    if delta == "5m":
        t = datetime.now().timestamp() - 325 * 300
    elif delta == "1h":
        t = datetime.now().timestamp() - 325 * 3600
    elif delta == "6h":
        t = datetime.now().timestamp() - 325 * 21600
    # t = (datetime.now()- relativedelta(years=0, months=6)).timestamp()
    idxs = 0
    two_yrs_ago = datetime.now() - relativedelta(years=2)
    while t > two_yrs_ago.timestamp():
        time_df = get_prices_at_time(delta, t)

        label = 0
        if delta == "5m":
            label = str(int(t - (t % 300)))
        elif delta == "1h":
            label = str(int(t - (t % 3600)))
        elif delta == "6h":
            label = str(int(t - (t % 21600)))
        # times[label] = df_json
        if delta == "6h":
            t = t - (21600)
        elif delta == "1h":
            t = t - 3600
        elif delta == "5m":
            t = t - 300
        else:
            ValueError()

        if idxs % 10 == 0:
            times[0][label] = time_df
        # elif idxs < 1000000:
        elif idxs % 10 == 1:
            times[1][label] = time_df
        elif idxs % 10 == 2:
            times[2][label] = time_df
        elif idxs % 10 == 3:
            times[3][label] = time_df
        elif idxs % 10 == 4:
            times[4][label] = time_df
        elif idxs % 10 == 5:
            times[5][label] = time_df
        elif idxs % 10 == 6:
            times[6][label] = time_df
        elif idxs % 10 == 7:
            times[7][label] = time_df
        elif idxs % 10 == 8:
            times[8][label] = time_df
        else:
            times[9][label] = time_df
        idxs += 1

        # time.sleep(0.1)
    if time == {}:
        return None
    else:
        return times


def create_complete_historical(delta):
    try:
        if delta == "1h":
            historical_time = get_all_historical_API(delta)
        else:
            historical_time = get_all_historical_API(delta)
        for idx in range(len(historical_time)):
            try:
                f = open(
                    "Data/Historical/Complete-" + str(delta) + "-" + str(idx) + ".json",
                    "w",
                )
            except:
                try:
                    os.mkdir("Data")
                except:
                    os.mkdir("Data/Historical")
                f = open(
                    "Data/Historical/Complete-"
                    + str(delta)
                    + "-"
                    + str(idx)
                    + "-"
                    + ".json",
                    "w",
                )
            f.write(json.dumps(historical_time[idx], indent=4))
            f.close()
    except:
        return IndexError()


def get_historical_local(name, delta) -> pd.DataFrame:
    id = NameIDHelper.NameToID(name)
    times = {}
    fpath = "Data/Historical/Complete-" + str(delta) + "-0.json"
    try:
        df = pd.read_json(fpath)
    except:
        create_complete_historical(delta)
        df = pd.read_json(fpath)

    item = df.loc[int(id)]
    for i in range(1, 10):
        # try looking for the others as well
        fpath = "Data/Historical/Complete-" + str(delta) + "-" + str(i) + ".json"
        try:
            df = pd.read_json(fpath)
            item = pd.concat([item, df.loc[id]])
        except:
            pass
    # save the indexes
    item = item.dropna()
    temp = item.index
    df = pd.DataFrame(item.to_list())
    df = df.set_index(temp)
    df = df.sort_index()
    return df


def get_historical_API(delta, id, start_time=None):
    times = {}
    if start_time is None:
        temp = datetime.now() - relativedelta(months=6)
        t = temp.timestamp()
    else:
        t = start_time

    two_yrs_ago = datetime.now() - relativedelta(years=2)
    counter = 0
    while t > two_yrs_ago.timestamp():
        time_df = get_prices_at_time(delta, t)
        label = 0
        if delta == "5m":
            label = str(int(t - (t % 300)))
        elif delta == "1h":
            label = str(int(t - (t % 3600)))
        elif delta == "6h":
            label = str(int(t - (t % 21600)))
        # times[label] = df_json
        if delta == "6h":
            t = t - (21600)
        elif delta == "1h":
            t = t - 3600
        elif delta == "5m":
            t = t - 300
        else:
            ValueError()
        try:
            times[label] = time_df[str(id)]
            print(time_df[str(id)])
            counter = 0
        except:
            counter += 1
            print(
                "No info for timestamp",
                t,
                " continuing until 10 in a row with no info:",
                counter,
                "/10",
            )
            if counter >= 10:  # if there are 10 instances in a row with no item
                break
        time.sleep(0.1)
    if time == {}:
        return None
    else:
        return times


def create_historical(name, delta):
    id = NameIDHelper.NameToID(name)
    try:
        if delta == "1h":
            historical_time = get_historical_API(
                delta, id, datetime.now().timestamp() - (3600 * 365)
            )
        else:
            historical_time = get_historical_API(
                delta, id, datetime.now().timestamp() - (21600 * 365)
            )

        try:
            f = open("Data/Historical/" + str(id) + "-" + str(delta) + ".json", "w")
        except:
            try:
                os.mkdir("Data")
            except:
                os.mkdir("Data/Historical")
            f = open("Data/Historical/" + str(id) + "-" + str(delta) + ".json", "w")
        f.write(json.dumps(historical_time, indent=4))
        f.close()
    except:
        return IndexError()


def create_historical_local(name, delta):
    id = NameIDHelper.NameToID(name)
    print("id is ", id)
    if os.path.exists("Data/Historical/" + str(id) + "-" + str(delta) + ".json"):
        f = open("Data/Historical/" + str(id) + "-" + str(delta) + ".json", "w")
    else:
        historical_time = get_historical_local(name, delta)
        try:
            os.mkdir("Data")
        except:
            try:
                os.mkdir("Data/Historical")
            except:
                pass
        f = open("Data/Historical/" + str(id) + "-" + str(delta) + ".json", "w")
        historical_time = historical_time.transpose()
        historical_time.to_json(
            "Data/Historical/" + str(id) + "-" + str(delta) + ".json", indent=4
        )
    f.close()


def get_item_historical_local(name, delta):
    id = NameIDHelper.NameToID(name)
    fpath = "Data/Historical/" + str(id) + "-" + str(delta) + ".json"
    if os.path.exists(fpath):
        try:
            df = pd.read_json(fpath)
        except:
            create_historical_local(name, delta)
            df = pd.read_json(fpath)
    else:
        create_historical_local(name, delta)
        df = pd.read_json(fpath)
    return df


def get_item_historical(name, delta):
    id = NameIDHelper.NameToID(name)
    fpath = "Data/Historical/" + str(id) + "-" + str(delta) + ".json"
    try:
        df = pd.read_json(fpath)
    except:
        create_historical(name, delta)
        df = pd.read_json(fpath)
    return df


def update_historical(delta):
    fpath = "Data/Historical/Complete-" + str(delta) + "-0.json"
    try:
        df = pd.read_json(fpath)
    except:
        create_complete_historical(delta)
        df = pd.read_json(fpath)

    item = df.transpose()
    for i in range(1, 10):
        # try looking for the others as well
        fpath = "Data/Historical/Complete-" + str(delta) + "-" + str(i) + ".json"
        try:
            df = pd.read_json(fpath)
            item = pd.concat([item, df.transpose()])
        except:
            pass
    # save the indexes
    df = pd.DataFrame(item)
    # item = item.dropna()
    df = df.sort_index()

    # now df is the entire local historical
    last_item = df.index[-1]

    # now we can get the latest one the instant api gets
    import DateTimeHelper

    l = DateTimeHelper.getDT("Twisted bow", delta)
    t = datetime.strptime(l.index[0], "%Y-%m-%d %H:%M:%S").timestamp()

    new = []

    while t > last_item.timestamp():
        time_df = get_prices_at_time(delta, t)

        label = 0
        if delta == "5m":
            label = str(int(t - (t % 300)))
        elif delta == "1h":
            label = str(int(t - (t % 3600)))
        elif delta == "6h":
            label = str(int(t - (t % 21600)))
        # times[label] = df_json
        if delta == "6h":
            t = t - (21600)
        elif delta == "1h":
            t = t - 3600
        elif delta == "5m":
            t = t - 300
        else:
            ValueError()

        new.append(time_df)

    df = pd.concat([df, pd.DataFrame(new)])
    df = df.sort_index()

    times = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]

    for i in range(df.index.size):
        times[i % 10][df.index[i].timestamp()] = df.loc[df.index[i]].to_json()

    for idx in range(len(times)):
        try:
            f = open(
                "Data/Historical/Complete-" + str(delta) + "-" + str(idx) + ".json", "w"
            )
        except:
            try:
                os.mkdir("Data")
            except:
                os.mkdir("Data/Historical")
            f = open(
                "Data/Historical/Complete-"
                + str(delta)
                + "-"
                + str(idx)
                + "-"
                + ".json",
                "w",
            )
        f.write(json.dumps(times[idx], indent=4))
        f.close()
    return df
