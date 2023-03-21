import requests

url = 'https://prices.runescape.wiki/api/v1/osrs'
# we want the latest data, so lets add that to the url
url += "/latest?"
# lets add the abyssal whip to the url:
url += "id=4151"

headers = {
    # the wiki blocks all common user-agents in order to prevent spam
    # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
    'User-Agent': 'volume_tracker - @Be#9998',
}

# response = requests.get(url, headers=headers)
# print(response.text)

import NameIDHelper

print(NameIDHelper.IdToName(100000))