# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 13:10:48 2017

@author: user
"""

from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from itertools import cycle

passes = Table.read('allPasses.fits')         # Read the astropy table with all the shots from all the games are stored.
# 1:NNDAvg and 0:... depending on which table took the shot.
# RHS is the away goal position. ->get the RHS is distance, RHSANG is the angle

#Start with easy, Just NNDAvgs
NND = []
velocity = []
outcome = []
angle = []
ballAccn = []
goalD = []

unsuc = []
suc = []
c = 0
pastFile = str(0)
for Apass in passes:
    if pastFile == '0' or pastFile != str(Apass['file']): #update tables
        filename = str(Apass['file'])+".fits"
        varTable = Table.read('VarTable'+filename)
        plTbl = Table.read('playerTable'+filename)
        ballTbl = Table.read('ballTbl' + filename)
        
    frame = Apass['frame']
    player = Apass['player']
    team = Apass['team']
    if team == 0: #away attacks -x
        goalD.append(varTable['ball:LHD'][frame])
        defTeam = 1
    else:
        goalD.append(varTable['ball:RHD'][frame])
        defTeam = 0
    NND.append(varTable[frame]['NND:' + str(team)+":" +str(player)])
    vx = plTbl[frame]['vx:'+str(team)+':'+str(player)]
    vy = plTbl[frame]['vy:'+str(team)+':'+str(player)]
    velocity.append(np.linalg.norm([vx,vy])) #velocity mag
    angle.append(Apass['angle'])
    bax = ballTbl['aball:x'][frame]
    bay = ballTbl['aball:y'][frame]
    ballAccn.append(np.linalg.norm([bax,bay]))
    outcome.append(Apass['outcome'])
    
    if outcome[c] ==1: #successful
        suc.append([velocity[c],NND[c], ballAccn[c], goalD[c],angle[c]])
    else:
        unsuc.append([velocity[c],NND[c], ballAccn[c], goalD[c],angle[c]])
    
    pastFile = str(Apass['file'])
    
    c+=1
    
Xs = [velocity,NND, ballAccn, goalD, angle] #When plotting this will be in format x,y on the axis
Y = outcome
Xs = np.transpose(Xs)
suc = np.transpose(suc)
unsuc = np.transpose(unsuc)

# Binarize the output
Y = label_binarize(Y, classes=[0, 1])
n_classes = Y.shape[1]

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(Xs, Y, test_size = 0.25, random_state = 5)

## Feature Scaling
#from sklearn.preprocessing import StandardScaler
#sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 40, criterion = 'entropy', random_state = 3)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Compute ROC curve and ROC area for each class
from sklearn.metrics import roc_curve, auc
fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(len(y_test)):
    fpr[i], tpr[i], _ = roc_curve(y_test[:], y_pred[:])
    roc_auc[i] = auc(fpr[i], tpr[i])

    
plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[0])
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC) curve for the passes classifier')
plt.legend(loc="lower right")
plt.show()




# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
#
## Visualising the Training set results
#from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
#
#X_set, y_set = X_train, y_train
#X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 1),
#                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 1))
#plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
#             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
#plt.xlim(X1.min(), X1.max())
#plt.ylim(X2.min(), X2.max())
#for i, j in enumerate(np.unique(y_set)):
#    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
#                c = ListedColormap(('red', 'green'))(i), label = j)
#plt.title('Random Forest Classification (Training set)')
#plt.xlabel('Average Nearest Neighbour Distance Attack')
#plt.ylabel('Average Nearest Neighbour Distance Defense')
#plt.legend()
#plt.show()
#
#
## Visualising the Test set results
#from matplotlib.colors import ListedColormap
#X_set, y_set = X_test, y_test
#X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 1),
#                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 1))
#plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
#             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
#plt.xlim(X1.min(), X1.max())
#plt.ylim(X2.min(), X2.max())
#for i, j in enumerate(np.unique(y_set)):
#    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
#                c = ListedColormap(('red', 'green'))(i), label = j)
#plt.title('Random Forest Classification (Test set)')
#plt.xlabel('Average Nearest Neighbour Distance Attack')
#plt.ylabel('Average Nearest Neighbour Distance Defense')
#plt.legend()
#plt.show()
#
from sklearn.ensemble import ExtraTreesClassifier
# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)

forest.fit(Xs, Y)
importances = classifier.feature_importances_
std = np.std([tree.feature_importances_ for tree in classifier.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

xTags = []
for i in indices:
    if i == 0:
        xTags.append('Player Velocity')
    elif i ==1:
        xTags.append('Nearest Neighbour Distance')
    elif i ==2:
        xTags.append('Ball Acceleration after pass')
    elif i ==3: 
        xTags.append('Distance to the attacking goal')
    elif i ==4:
        xTags.append('Angle of pass relative to direction of play')

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances for successful passes.")
plt.bar(range(Xs.shape[1]), importances[indices]*100,
       color="r", yerr=std[indices], align="center")
plt.xticks(range(Xs.shape[1]), indices)
plt.xlabel('Features')
plt.ylabel('Importance of feature in classification (%)')
plt.xlim([-1, Xs.shape[1]])
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
X2 = np.transpose(Xs)
data = [
    go.Parcoords(
        dimensions = list([
            dict(range = [X2[0].min(),X2[0].max()],
                 label = 'Player Velocity (cm/frame)', values = suc[0]),
            dict(range = [X2[1].min(),X2[1].max()],
                 label = 'Player NND (cm)', values = suc[1]),
            dict(range = [X2[2].min(),X2[2].max()],
                 label = 'Ball Acceleration (cm/frame^2)', values = suc[2],
                 ticktext = ['text 1', 'text 2', 'text 3', 'text 4']),
            dict(range = [X2[3].min(),X2[3].max()],
                 label = 'Distance towards attacking goal (cm)', values = suc[3]),
             dict(range = [X2[4].min(),X2[4].max()],
                 label = 'Angle of pass to direction of play (radians)', values = suc[4])
        ])
    )
]
    
layout = go.Layout(
    title='Parralel axes plot for successful passes.',)
fig = go.Figure(data=data, layout=layout)


data2 = [
    go.Parcoords(
        dimensions = list([
            dict(range = [X2[0].min(),X2[0].max()],
                 label = 'Player Velocity (cm/frame)', values = unsuc[0]),
            dict(range = [X2[1].min(),X2[1].max()],
                 label = 'Player NND (cm)', values = unsuc[1]),
            dict(range = [X2[2].min(),X2[2].max()],
                 label = 'Ball Acceleration (cm/frame^2)', values = unsuc[2],
                 ticktext = ['text 1', 'text 2', 'text 3', 'text 4']),
            dict(range = [X2[3].min(),X2[3].max()],
                 label = 'Distance towards attacking goal (cm)', values = unsuc[3]),
             dict(range = [X2[4].min(),X2[4].max()],
                 label = 'Angle of pass to direction of play (radians)', values = unsuc[4])
        ])
    )
]
layout2 = go.Layout(
    title='Parralel axes plot for unsuccessful passes.',)

fig2 = go.Figure(data = data2, layout = layout2)





'''

