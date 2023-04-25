import json
import os
import time
from datetime import datetime
from urllib.request import Request, urlopen
import HistoricalDataHelper
import Predictor


# HistoricalDataHelper.create_complete_historical('6h')
# temp = HistoricalDataHelper.get_historical_local('Twisted bow', '6h')

u = HistoricalDataHelper.update_historical('6h')
print(u)