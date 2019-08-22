import pandas as pd
from tick_forex import constants
from sklearn.model_selection import train_test_split
from sklearn import svm, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from collections import Counter
from tick_forex.pr.functions import *

data_tick_store_path = constants.data_tick_store_path


def get_featuresets(patterns):
    X, y = [], []
    for pattern in patterns:
        pat = pattern[:-1].values
        if pattern[-1] == pattern[-2]:
            label = 0
        if pattern[-1] > pattern[-2]:
            label = 1
        if pattern[-1] < pattern[-2]:
            label = -1
        X.append(pat)
        y.append(label)
    str_vals = [str(i) for i in y]
    print('Data spread:', Counter(str_vals))
    return X, y, Counter(str_vals).most_common()


def run_ml(pattern_parameters):
    pattern_data = pd.read_pickle(
        data_tick_store_path + r"\bars\time_bars_{}_{}.pkl".format(pattern_parameters['timeframe'], pattern_parameters['stock']))

    patterns = getPatterns(data=pattern_data,
                           patternlength=pattern_parameters['patternlength'],
                           col='close', outcome_shift=2)

    X, y, data_spread = get_featuresets(patterns)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:', confidence)
    predictions = clf.predict(X_test)
    print('predicted class counts:', Counter(predictions))
    print()
    print()
    return confidence, data_spread, Counter(predictions).most_common()


multi_pattern_parameters = [{
    'stock': 'AKBNK',
    'patternlength': 10,
    'similarity': 80,
    'timeframe': '1d'
}, {
    'stock': 'AKBNK',
    'patternlength': 20,
    'similarity': 70,
    'timeframe': '1d'
}, {
    'stock': 'AKBNK',
    'patternlength': 20,
    'similarity': 80,
    'timeframe': '1H'
}, {
    'stock': 'AKBNK',
    'patternlength': 30,
    'similarity': 80,
    'timeframe': '15Min'
}, {
    'stock': 'AKBNK',
    'patternlength': 15,
    'similarity': 80,
    'timeframe': '4H'
}
]
a = []
import time

for pattern_parameters in multi_pattern_parameters:
    st = time.time()
    confidence, data_spread, predicted_class_spread = run_ml(pattern_parameters)
    et = time.time()
    resdict = pattern_parameters.copy()
    resultdict = {'accuracy': confidence,
                  'dataspread': data_spread,
                  'predictedspread': predicted_class_spread,
                  'lasted_seconds': et - st}
    resdict.update(resultdict)
    a.append(resdict)
    print('sona eren ml : {}'.format(pattern_parameters))

df = pd.DataFrame(a)
