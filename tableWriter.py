# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:53:38 2017

@author: user
"""

#loop through each filenames to store them, as the match id changes everytime and also 
import glob, os
import numpy as np
import dataExtraction as DE
from astropy.table import Table

fileDir = "./matchFiles"
os.chdir(fileDir)
matchIDs = [[] for i in range(4)] #array to store match filenames
c = 0


#loop through data files
for file in glob.glob("*.dat"):
    matchIDs[c].append(file)
    matchIDs[c+1].append(file.split('.')[0] + '_metadata.xml')
    matchIDs[c+2].append(glob.glob("*-"+file.split('.')[0]+"-eventdetails.xml")[0])
    matchIDs[c+3].append(glob.glob("*-f"+file.split('.')[0]+"-matchresults.xml")[0])


os.chdir(os.path.dirname(os.path.realpath(__file__)))

matchIDs = np.transpose(matchIDs)

##
allShots = Table([[],[],[],[],[]], names = ('team','player','eventID','frame','file'), dtype = ('i','i','i','i','i')) #new Table for shots
allPass = Table([[],[],[],[],[], []], names = ('team','player','outcome','frame','angle', 'file'), dtype = ('i','i','i','i','f', 'i')) #new Table for shots

for i in matchIDs:
    shotTbl, passTbl = DE.extract(i, fileDir)
    for row in shotTbl: #loop
        temp = []
        sc=0
        for col in row.colnames:
            temp.append(row[col])
            sc+=1
        #rearrange to be correct in allShots
        temp2 = np.zeros(len(temp)+1)
        temp2[0] = int(temp[3])#team
        temp2[1] = int(temp[0])#player
        temp2[2] = int(temp[1]) #EVent
        temp2[3] = int(temp[2])#frame
        temp2[4] = int(i[0].split('.')[0]) #file
        allShots.add_row(temp2)#store row
    
    for row in passTbl:
        temp = []
        sc = 0
        for col in row.colnames:
            temp.append(row[col])
            sc+=1
        
        temp2 = np.zeros(len(temp) +1)
        temp2[0] = int(temp[1])#team
        temp2[1] = int(temp[0])#player
        temp2[2] = int(temp[3]) #pass outcome 1 = success
        temp2[3] = int(temp[2])#frame
        temp2[4] = float(temp[4]) #angle.
        temp2[5] = int(i[0].split('.')[0]) #file
        allPass.add_row(temp2)
    c+=1

allShots.write('allShots.fits', overwrite = True)
allPass.write('allPasses.fits', overwrite = True)


#allShots = Table.read('allShots.fits')



    