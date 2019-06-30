import  pandas as pd
import numpy as np
import data_cleaning
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.tree import DecisionTreeClassifier
from  sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def weight():
    names = ['age', 'sex', 'chest pain type', 'resting blood pressure', 'serum cholestoral', 'fasting blood sugar',
         'resting electrocardiographic results', 'maximum heart rate', 'exercise induced angina',
         'oldpeak', 'the slope of ST', 'number of major vessels', 'thal']
    data = data_cleaning.data_uniform('clean_data.csv')
    x, y = data.shape
    k = 1 / np.log(x)
    nij = data.sum(axis=0)

    pij = data / nij
    result = pij * np.log(pij)
    result = np.nan_to_num(result)
    # Calculate the information entropy of each index
    e = -k * (result.sum(axis=0))
    # Calculate the weight
    wi = (1 - e) / np.sum(1 - e)
    dict = {}
    for i in range(data.shape[1]):
        dict[data.keys()[i]] = wi[i]
    x1, y1 = data[data.keys()[:-1]], data[data.keys()[-1]]
    X_new = SelectKBest(chi2, k=8).fit_transform(x1, y1)

    #######decision tree#######
    tree = DecisionTreeClassifier(random_state=0)
    tree.fit(x1, y1)
    tree_list = {}
    for i in range(len(names)):
        tree_list[names[i]] = tree.feature_importances_[i]
    tree_list = sorted(tree_list.items(), key=lambda item: item[1], reverse = True)
    result = {}
    for i in range(len(tree_list)):
        result[tree_list[i][0]] = round(tree_list[i][1],5)
    return result

# #######random forest#######
# rf = RandomForestClassifier(n_estimators=100,random_state=0)
# rf.fit(x1,y1)
# rf_list = {}
# for i in range(len(names)):
#     rf_list[names[i]] = rf.feature_importances_[i]
# print(sorted(rf_list.items(),key=lambda item:item[1]))
#
#
# #######LogisticRegression#########
# LR = LogisticRegression(C=10.0, penalty='l1', tol=0.01)
#
# X_train, X_test, y_train, y_test = train_test_split(x1, y1, test_size=0.3, random_state=0)
# LR.fit(X_train,y_train)
# LR.predict(X_test)
#
# lr_list = {}
# for i in range(len(names)):
#     lr_list[names[i]] = abs(LR.coef_[0][i])
# print(sorted(lr_list.items(),key=lambda item:item[1]))
