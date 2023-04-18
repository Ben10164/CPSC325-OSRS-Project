import HistoricalDataHelper

# HistoricalDataHelper.create_complete_historical('6h')
temp = HistoricalDataHelper.get_historical_local('Twisted bow', '6h')
temp = HistoricalDataHelper.get_historical_local('Twisted bow', '1h')
temp = temp.sort_index()
print(temp)
print(type(temp))