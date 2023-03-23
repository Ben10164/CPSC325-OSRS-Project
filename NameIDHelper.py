import requests
import pandas as pd

# Creating df with json data instead of calling the API
# this is to lower the amount of calls needed for this helper function!
mapping_df = pd.read_json('NameIDMap.json')
# we are going to drop the useless cols that we wont be needing
mapping_df = mapping_df.drop(
    columns=['examine', 'lowalch', 'limit', 'value', 'highalch', 'icon', 'members'])
name_dict = mapping_df.set_index('name')['id'].to_dict()
id_dict = mapping_df.set_index('id')['name'].to_dict()


def NameToID(name):
    return name_dict[name]


def IdToName(id):
    return id_dict[id]


# This function will update the locally stored JSON
def UpdateJson():
    url = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
    # we want the latest data, so lets add that to the url

    headers = {
        # the wiki blocks all common user-agents in order to prevent spam
        # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
        'User-Agent': 'Item_ID_Helper_Functions - @Be#9998',
    }

    response_json = requests.get(url, headers=headers).text
    f = open('data.json', 'w')
    f.write(response_json)
    f.close()
