# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:39:29 2017

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:27:29 2017

@author: user
"""

import corner
import glob
import numpy as np
from astropy.table import Table
import pandas as pd
from pandas.tools import plotting
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
#ndim, nsamples = 2, 25
#samples = np.random.randn(ndim * nsamples)
#print(samples)
#samples = samples.reshape([nsamples, ndim])
#print(samples)
#figure = corner.corner(samples)



passes = Table.read('allPasses.fits')
Udata = [[], [], [],[],[]] #un sysuccessful passes 5 vars - NND, Angle, Player velocity, accn magnitude, ball distance to goal
Sdata = [[], [], [],[],[]] #successful passes
pastFile = 0
for APass in passes: #loop through rows 
    
    file = APass['file']
    if pastFile ==0 or pastFile != file:#update tbls
        fileName = glob.glob("VarTable"+str(file)+".fits")[0]
        varbs = Table.read(fileName)
        
    if APass['team'] == 1: #home
        team = '1:'
    else:
        team = '0:'
    
    player = APass['player']
        
    if APass['outcome'] == 1: #successful pass
        Sdata[1].append(APass['angle'])
        Sdata[0].append(varbs['NND:'+team + str(player)][APass['frame']])
        Sdata[2].append()
    else:
        Udata[0].append(varbs[team+'NNDAvg'][APass['frame']])
        Udata[1].append(varbs['NND:'+team + str(player)][APass['frame']])
    
    pastFile = file

            #Sdata[1].append(varbs[])
#    if(shot['eventID'] == 16):#goal
#        if shot['team'] == 1: # home attacks +x
#            Gdata[0].append(varbs['1:CloseNNDAvg'][shot['frame']])
#            Gdata[1].append(varbs['1:nAtt'][shot['frame']])
#            Gdata[2].append(varbs['ball:RHD'][shot['frame']])
#        else:
#            Gdata[0].append(varbs['0:CloseNNDAvg'][shot['frame']])
#            Gdata[1].append(varbs['0:nAtt'][shot['frame']])
#            Gdata[2].append(varbs['ball:LHD'][shot['frame']])
#    else: #no goal
#        if shot['team'] == 1: # home attacks +x
#            Sdata[0].append(varbs['1:CloseNNDAvg'][shot['frame']])
#            Sdata[1].append(varbs['1:nAtt'][shot['frame']])
#            Sdata[2].append(varbs['ball:RHD'][shot['frame']])
#        else:
#            Sdata[0].append(varbs['0:CloseNNDAvg'][shot['frame']])
#            Sdata[1].append(varbs['0:nAtt'][shot['frame']])
#            Sdata[2].append(varbs['ball:LHD'][shot['frame']])
    

UdataF = pd.DataFrame({'AvgNND':Udata[0], 'playerNND':Udata[1]}) #convert to dataFrame
SdataF = pd.DataFrame({'AvgNND':Sdata[0], 'playerNND':Sdata[1]}) #convert to dataFrame
#
plotting.scatter_matrix(UdataF[['AvgNND','playerNND']])
plt.suptitle('Scatter matrix for unsuccesful passes, where avg nnd is for 5 most attcking players')
#pp = PdfPages('Test scatters for goals.pdf')
#pp.savefig()
#pp.close()
#
#
plotting.scatter_matrix(SdataF[['AvgNND','playerNND']])
plt.suptitle('Scatter matrix for succesful passes,  where avg nnd is for 5 most attcking players')
#pp = PdfPages('Test scatters for shots.pdf')
#pp.savefig()
#pp.close()
#
#plt.figure()
#plt.scatter(GdataF['nAttackers'], GdataF['AvgNND'])
#plt.xlabel('nAttackers')
#plt.ylabel('AvgNND of 5 closest to goal')
#plt.title('relationship for goals')
#plt.show()
#
#plt.figure()
#plt.scatter(SdataF['nAttackers'], SdataF['AvgNND'])
#plt.title('relationship for shots')
#plt.xlabel('nAttackers')
#plt.ylabel('AvgNND of 5 closest to goal')
#plt.show()


