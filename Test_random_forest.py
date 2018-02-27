#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:17:40 2017

@author: Jack
"""
import numpy as np

# Test random forset classification with multiple variables.

X1 = np.array([2,3,4,6])
X2 = np.array([4,1,2,2])
X3 = np.array([4,1,5,1])
X = np.array([X1,X2,X3])
y = np.array(['Blue','Red','Blue'])
#X = np.array([X1,X2])




#n_samples = np.arange(len(X))
#X = [n_samples,X.transpose]
# first try 2D without scaling 
# Feature Scaling



from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.10, random_state = 10)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 5, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
