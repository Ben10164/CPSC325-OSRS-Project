import HistoricalDataHelper
import os

HistoricalDataHelper.update_historical("6h")

if os.path.exists("Data/Historical/20997-6h.json"):
    os.remove("Data/Historical/20997-6h.json")

HistoricalDataHelper.create_historical_local("Twisted bow", "6h")

if os.path.exists("Data/Historical/22486-6h.json"):
    os.remove("Data/Historical/22486-6h.json")

HistoricalDataHelper.create_historical_local("Scythe of vitur (uncharged)", "6h")

if os.path.exists("Data/Historical/27277-6h.json"):
    os.remove("Data/Historical/27277-6h.json")

HistoricalDataHelper.create_historical_local("Tumeken's shadow (uncharged)", "6h")

HistoricalDataHelper.update_historical("1h")

if os.path.exists("Data/Historical/20997-1h.json"):
    os.remove("Data/Historical/20997-1h.json")

HistoricalDataHelper.create_historical_local("Twisted bow", "1h")

if os.path.exists("Data/Historical/22486-1h.json"):
    os.remove("Data/Historical/22486-1h.json")

HistoricalDataHelper.create_historical_local("Scythe of vitur (uncharged)", "1h")

if os.path.exists("Data/Historical/27277-1h.json"):
    os.remove("Data/Historical/27277-1h.json")

HistoricalDataHelper.create_historical_local("Tumeken's shadow (uncharged)", "1h")
