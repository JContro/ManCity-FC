#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:17:40 2017

@author: Jack
"""
import numpy as np
from astropy.table import Table

# Test random forset classification with multiple variables.
shots = Table.read('shotTblTest.fits')
players = Table.read('playerTableTest.fits')
variables = Table.read('testVarTable.fits')

c = 0
Xs = [[] for i in range(6)]
Y = []
for frame in shots['frame']: #loop through shot frames
    frame = int(frame)
    Xs[0].append(variables['1:NNDAvg'][frame])
    Xs[1].append( variables['0:NNDAvg'][frame])
    if int(shots['team'][c]) ==1: #home attacks +x / RH
        Xs[2].append( variables['ball:RHFullA'][frame])
        Xs[3].append( variables['ball:RHD'][frame])
        Xs[4].append(variables['0:nDefs'][frame])
        Xs[5].append(variables['1:nAtt'][frame])
    else:
        Xs[2].append(variables['ball:LHFullA'][frame])
        Xs[3].append(variables['ball:LHD'][frame])
        Xs[4].append(variables['1:nDefs'][frame])
        Xs[5].append(variables['0:nAtt'][frame])
        
    if int(shots['eventID'][c]) ==16:
        Y.append('goal')
    else:
        Y.append('no goal')
    c += 1

Xs = np.transpose(Xs)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(Xs, Y, test_size = 0.25, random_state = 5)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 5, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Visualising the Training set results
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest Classification (Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()



# Visualising the Test set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest Classification (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()