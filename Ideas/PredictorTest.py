from scipy import stats as st
import warnings
warnings.simplefilter(action='ignore', category=Warning)
import os
# Disable TensorFlow warnings and info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import json
import numpy as np
import datetime
import pandas as pd
import datetime
import pandas as pd
import numpy as np
from finta import TA
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn import metrics

# df = pd.read_csv("DataIntake/Data/"+ticker+"/Stock_Data.csv")

def _exponential_smooth(data, alpha):
    """
    Function that exponentially smooths dataset so values are less 'rigid'
    :param alpha: weight factor to weight recent values more
    """
    
    return data.ewm(alpha=alpha).mean()



def _get_indicator_data(data):
    """
    Function that uses the finta API to calculate technical indicators used as the features
    :return:
    """

    # Instead of using the actual volume value (which changes over time), we normalize it with a moving volume average
    data['normAvg'] = data['average'] / data['average'].ewm(5).mean()

    # Remove columns that won't be used as features
    del (data['avgLowPrice'])
    del (data['avgHighPrice'])
    
    return data


def _produce_prediction(data, window):
    """
    Function that produces the 'truth' values
    At a given row, it looks 'window' rows ahead to see if the price increased (1) or decreased (0)
    :param window: number of days, or rows to look ahead to see what the price did
    """
    
    prediction = (data.shift(-window)['normAvg'] >= data['normAvg'])
    prediction = prediction.iloc[:-window]
    data['nextDeltaInc'] = prediction.astype(int)
    
    return data



def cross_Validation(data):
    # Split data into equal partitions of size len_train
    
    num_train = 200 # Increment of how many starting points (len(data) / num_train  =  number of train-test sets)
    len_train = 40 # Length of each train-test set
    
    # Lists to store the results from each model
    rf_RESULTS = []
    knn_RESULTS = []
    gbt_RESULTS = []
    ensemble_RESULTS = []
    
    i = 0
    
    # Models which will be used
    rf = RandomForestClassifier()
    knn = KNeighborsClassifier()
    ada = AdaBoostClassifier()
    gb = GradientBoostingClassifier()
    
    # Create a tuple list of our models
    estimators=[('knn', knn), ('rf', rf),('ada', ada), ('gb', gb)]
    ensemble = VotingClassifier(estimators, voting='soft')
    
    while True:
        
        # Partition the data into chunks of size len_train every num_train days
        df = data.iloc[i * num_train : (i * num_train) + len_train]
        i += 1
        #print(i * num_train, (i * num_train) + len_train)
        if len(df) < 40:
            break
        
        df['nextDeltaInc'] = df['nextDeltaInc'].shift(periods=1)
        df = df.reset_index()
        df = df.drop(['timestamp'], axis=1)
        first_row = df.iloc[0]
        first_row = first_row.drop(['nextDeltaInc'])
        df = df.tail(-1)
        #df = df.drop(data.index[0])
        # df['nextDeltaInc'][0] = 0
        print(df)
        y = df['nextDeltaInc']
        # print(y)
        features = [x for x in df.columns if x not in ['nextDeltaInc']]
        X = df[features]

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size= 7 * len(X) // 10,shuffle=False)
        
        # fit models
        rf.fit(X_train, y_train)
        knn.fit(X_train, y_train)
        ensemble.fit(X_train, y_train)
        
        # get predictions
        rf_prediction = rf.predict(X_test)
        knn_prediction = knn.predict(X_test)
        ensemble_prediction = ensemble.predict(X_test)
        
#         print('rf prediction is ', rf_prediction)
#         print('knn prediction is ', knn_prediction)
#         print('ensemble prediction is ', ensemble_prediction)
#         print('truth values are ', y_test.values)
        
        # determine accuracy and append to results
        rf_accuracy = accuracy_score(y_test.values, rf_prediction)
        knn_accuracy = accuracy_score(y_test.values, knn_prediction)
        ensemble_accuracy = accuracy_score(y_test.values, ensemble_prediction)
        
#         print(rf_accuracy)
#         print(knn_accuracy)
#         print(ensemble_accuracy)
        rf_RESULTS.append(rf_accuracy)
        knn_RESULTS.append(knn_accuracy)
        ensemble_RESULTS.append(ensemble_accuracy)
                
    print('RF Accuracy = ' + str( sum(rf_RESULTS) / len(rf_RESULTS)))
    print('KNN Accuracy = ' + str( sum(knn_RESULTS) / len(knn_RESULTS)))
    print('ENSEMBLE Accuracy = ' + str( sum(ensemble_RESULTS) / len(ensemble_RESULTS)))
    

def getNeatGraph(name, time):

    import DateTimeHelper
    df = DateTimeHelper.getDT(name, time)
    data = _exponential_smooth(df, 0.65)
    data = _get_indicator_data(data)
    data = _produce_prediction(data, window=15)
    data = data.dropna() # Some indicators produce NaN values for the first few rows, we just remove them here
    print(data)
    cross_Validation(data)
    return data

def getNeatGraphFolder(name, time):

    import Functions
    df = Functions.getDT(name, time)
    data = _exponential_smooth(df, 0.65)
    data = _get_indicator_data(data)
    data = _produce_prediction(data, window=15)
    data = data.dropna() # Some indicators produce NaN values for the first few rows, we just remove them here
    print(data)
    cross_Validation(data)
    return data
