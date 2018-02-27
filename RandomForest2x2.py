#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:48:02 2017

Program that reads the tables and plots the different random forest correlations 2 by two.

Note: try and make the correlations in normal units, the standard scaled ones should suffice to start with

@author: Jack
"""

# Open the tables


from astropy.table import Table
import numpy as np

shots = Table.read('allShots.fits')         # Read the astropy table with all the shots from all the games are stored.
# 1:NNDAvg and 0:... depending on which table took the shot.
# RHS is the away goal position. ->get the RHS is distance, RHSANG is the angle

#Start with easy, Just NNDAvgs
NNDAttack = []
NNDDef = []
NNPlayer = []
ballAng = []
ballDist = []
outcome = []
for shot in shots:
    filename = "VarTable"+str(shot['file'])+".fits"
    varTable = Table.read(filename)
    frame = shot['frame']
    team = shot['team']
    player = shot['player']
    if team == 0:
        defTeam = 1
        # home team attacks to the right and is 1
        pitchside = "LH"
        
    else:
        defTeam = 0
        pitchside = "RH"
    NNDAttack.append(varTable[frame][str(team)+":NNDAvg"])
    NNDDef.append(varTable[frame][str(defTeam)+":NNDAvg"])
    NNPlayer.append(varTable[frame]["NND:"+str(team)+":"+str(player)])
    ballAng.append(varTable[frame]["ball:"+str(pitchside)+"A"])
    ballDist.append(varTable[frame]["ball:"+str(pitchside)+"D"])
    if shot['eventID'] == 16:
        outcome.append(1)
    else:
        
        outcome.append(0)

Xs = [ballAng,NNPlayer] #When plotting this will be in format x,y on the axis
Y = outcome
Xs = np.transpose(Xs)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(Xs, Y, test_size = 0.30, random_state = 2)

## Feature Scaling
#from sklearn.preprocessing import StandardScaler
#sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 400, criterion = 'entropy', random_state = 2)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_test, y_pred)

roc_auc = auc(fpr, tpr)
import matplotlib.pyplot as plt

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC) curve for the passes classifier')
plt.legend(loc="lower right")
plt.show()

# Visualising the Training set results
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 1),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 1))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('#E7843A', '#38F510',)))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest Classification (Training set)')
plt.xlabel('Angle between the ball and the goal [rad]')
plt.ylabel('Nearest Neighbour Distance from the player [cm]')
plt.legend()
plt.show()



# Visualising the Test set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 1),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 1))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('#E7843A', '#38F510',)))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest Classification (Test set)')
plt.xlabel('Angle between the ball and the goal [rad]')
plt.ylabel('Nearest Neighbour Distance from the player [cm]')
plt.legend()
plt.show()
'''
import plotly.offline as offline
import plotly.graph_objs as go

offline.init_notebook_mode()
#
#offline.plot({'data': [{'y': [4, 2, 3, 4]}], 
#               'layout': {'title': 'Test Plot', 
#                          'font': dict(size=16)}},
#             image='png')

X2 = np.array([NNDAttack,NNDDef,NNPlayer,ballAng])


data = [
    go.Parcoords(
        line = dict(color = Y,
                    colorscale = [[0,'#E70F0F'],[1,'#22F038']]),
        dimensions = list([
            dict(range = [X2[0].min(),X2[0].max()],
                 label = 'Average Nearest Neighbour Distance Attack [cm]', values = X2[0]),
            dict(range = [X2[1].min(),X2[1].max()],
                 label = 'Average Nearest Neighbour Distance Defense [cm]', values = X2[1]),
            dict(range = [X2[2].min(),X2[2].max()],
                 label = 'Nearest Neighbour distance from player [cm]', values = X2[2],
                 ticktext = ['text 1', 'text 2', 'text 3', 'text 4']),
            dict(range = [X2[3].min(),X2[3].max()],
                 label = 'Angle between the ball and the centre of the goal [rad]', values = X2[3])
            
            
        ]) 
            
            
    ) 
]


offline.plot(data)
'''