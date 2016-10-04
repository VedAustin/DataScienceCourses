#!/usr/bin/python


"""
    starter code for the evaluation mini-project
    start by copying your trained/tested POI identifier from
    that you built in the validation mini-project

    the second step toward building your POI identifier!

    start by loading/formatting the data

"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 

from sklearn import cross_validation

features_train,features_test,labels_train,labels_test = cross_validation.train_test_split(features,labels,random_state=42,test_size=0.3)

from sklearn.tree import DecisionTreeClassifier


clf = DecisionTreeClassifier()
clf.fit(features_train,labels_train)
print clf.score(features_test,labels_test), sum(clf.predict(features_test)), len(features_test), sum(labels_test)

import numpy as np
pred = clf.predict(features_test)

print np.dot(np.array(pred), np.array(labels_test))

from sklearn.metrics import precision_score, recall_score

print precision_score(labels_test,pred),recall_score(labels_test,pred)
