import requests
import NameIDHelper


url = 'https://prices.runescape.wiki/api/v1/osrs'
# we want the latest data, so lets add that to the url
url += "/timeseries?timestep=5m&id="
# lets add the abyssal whip to the url:
url += str(NameIDHelper.NameToID("Abyssal whip"))

headers = {
    # the wiki blocks all common user-agents in order to prevent spam
    # after talking with some of the API maintainers over discord they asked me to include my discord in the user-agent
    'User-Agent': 'volume_tracker - @Be#9998',
}

response = requests.get(url, headers=headers)
print(response.text)

import pandas
import io

test = pandas.read_csv(io.StringIO(response.text))

print(test)