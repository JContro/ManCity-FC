# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 15:49:50 2017

@author: user
"""


def isolatePasses(periods, pl, ball, fileNames, fileDir):
    
    from astropy.table import Table, Column
    from xml.etree import ElementTree as et
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    
#    ball = Table.read('testBall.fits')
#    players = Table.read('testTbl.fits')
    
#    fileNames = ['918894.dat', '918894_metadata.xml','f24-8-2017-918894-eventdetails.xml','srml-8-2017-f918894-matchresults.xml' ]
#    fileDir = "./matchFiles"
    os.chdir(fileDir)
    
    players = pl
    
    with open(fileNames[2],'rt') as f:
        tree = et.parse(f)
    
    root = tree.getroot()# takes us to 'games' tag
    shots = [[] for i in range(9)]
    teams = [] #array to store the team ids of home and away
    
    
    for game in root:
        startTime = game.attrib.get('period_1_start').split('T')[1].split(':')
        teams.append(int(game.attrib.get("away_team_id"))) #away ==0 and home ==1 like OPTA contention
        teams.append(int(game.attrib.get('home_team_id')))
        for event in game:
            evID = event.attrib.get('type_id') #stores opta event id
            qID = []
            outcome = event.attrib.get('outcome') #1= good,0 = bad
            x = event.attrib.get('x')
            y = event.attrib.get('y')
            
            if evID == '1': #pass
                cn = 0
                for qualifier in event: #loop through qualifiers 
                    qID.append(qualifier.attrib.get('qualifier_id'))
                    if qID[cn] == '213':
                        angle = float(qualifier.attrib.get('value'))
                        angle = angle - np.pi #shift by 180 degrees
                    cn +=1
                    
                if '279' not in qID and '6' not in qID and '5' not in qID:  #Not kick off, corner, free kick
                    shots[0].append(int(event.attrib.get('player_id'))) # Player that kicked the ball
                    shots[1].append(float(x)) #x
                    shots[2].append(float(y)) #y
                    shots[3].append(int(event.attrib.get('period_id')))
                    shots[4].append(outcome)
                    shots[6].append(int(event.attrib.get('team_id'))) #store what team did the shot etc
                    timeStamp = event.attrib.get('timestamp')
                    time = timeStamp.split('T')[1] #time part
                    shots[5].append(time)
                    shots[8].append(angle) #angle of pass
                        
    #Have the min, sec of goal - now convert that to a frame number.
    with open(fileNames[1], 'rt') as f:
        tree2 = et.parse(f)
    
    #periods = Table.read('periodTableTest.fits')
    #print(periods)
    #root2 = tree2.getroot()
    startFs = []
    endFs = []
    
    for node in tree2.iter('period'):
            start = node.attrib.get('iStartFrame')
            end = node.attrib.get('iEndFrame')
            
            if int(end)!=0: #ie the period did happen
               startFs.append(int(start))
               endFs.append(int(end))
    
       # goalTimeDiff = [[] for i in shots[5]]
    goalF = []
    c = 0
    for shotT in shots[5]:
        shotT = shotT.split(':')
        hourDiff = float(shotT[0])-float(startTime[0])
        minDiff = float(shotT[1]) - float(startTime[1])
        secDiff = float(shotT[2]) -float(startTime[2])
        
        totalDiff = (hourDiff*60*60 + minDiff*60 + secDiff)*25 #diff between start and end in frames
        frame = int(totalDiff)
        
        if shots[3][c] == 2: #second half
            goalF.append(frame - (startFs[1] - endFs[0]))
        else:
            goalF.append(frame)
        
        c+=1
    #print(goalF)
    
    
    
    for i in goalF:
        shots[7].append(i)
    
    with open(fileNames[3],'rt') as f:
        tree3 = et.parse(f)
        
    #c=0
    #for player in shots[0]: #loop through player id's
    #    if shots[6][c] == 
        
        
        
    #shots2 = np.transpose(shots)    # transpose the array to invert columns and rows. Each row is now an event
    
    shots2 = [[]for i in range(7)] #Just want the player ID and frame
    shots2[0] = shots[0] #player ID
    shots2[1] = shots[6] #teamID
    shots2[3] = shots[7] #estimated frame
    shots2[2] = shots[4] #outcome
    shots2[4] = shots[1] #x
    shots2[5] = shots[2] #y
    shots2[6] = shots[8] #angle
    shots2 = np.transpose(shots2)
    shotC= 0
    shots3 =[]
    shots2 = shots2.astype(float)
    
    for shot in shots2:
        player = shot[0]
        if int(shots2[shotC][1]) == teams[0]: #away loop through 
           counter = 1
        else: #home
            counter = 0 #first in the xml doc
        c = 0
        for node in tree3.iter('TeamData'):
                for node2 in node.iter('PlayerLineUp'):
                    if c == counter:
                        for playerData in node2.iter('MatchPlayer'):
                            thisPlayer = int(playerData.attrib.get('PlayerRef').split('p')[1])
                            if player == thisPlayer:
                                #print(thisPlayer)
                                #print(int(playerData.attrib.get('ShirtNumber')))
                               # print(shotC)
                              #  print(shots2[shotC])
                                a = int(playerData.attrib.get('ShirtNumber'))
                                shotz = np.append(shots2[shotC],a)
                                shots3.append(shotz)
                    c+=1 #increment team 
        shotC+=1
                    
                    
    #Have shots and Frame estimate. Now need to use pattern recognition to pinpoint 
    #the exact frame area the shot takes place.
    #Loop through goal frames
    
    #ball = Table.read('ballTable.fits')
    #players = Table.read('tableTest.fits')
    
    for node in tree2.iter('match'):
            xSize = node.attrib.get('fPitchXSizeMeters') #in Metres
            ySize = node.attrib.get('fPitchYSizeMeters')
        
    xSize = float(xSize) * 100 #Convert to cm
    ySize = float(ySize) *100
    #goalH = 2.438*100 #in cm
    
    #X and Y is in a PERCENTAGE as if the team IN POSSESION are attacking left to right 
    #so it is correct for the home team (1) who attack -x to +x and false for the away team (0) who attack +x to -x 
    shotC = 0 
    
    for APass in shots3: #loop thru shots 3 
        if int(APass[1]) == teams[0]: #away team - shft the coordinates
            xPerc = (100 - APass[4])/100
            yPerc = (100 - APass[5])/100
        else: 
            xPerc = APass[4]/100
            yPerc = APass[5]/100 #stays the same for the home team as they attack -x to +x
        
        xNew = xSize*xPerc - 0.5*xSize #- .5*sxize to shift origin to the centre point
        yNew = ySize*yPerc - 0.5*ySize
        
        shots3[shotC][4] = xNew
        shots3[shotC][5] = yNew
        shotC +=1

    
    
    
    
    shotC = 0
    shotT = Table()
    shotT['playerNum']= []
    shotT['team'] =[]
    shotT['frame']  = []
    shotT['outcome']=[]
    shotT['angle'] = []
    
    for shot in shots3: #loop through the frames. Estimated Frame number == shots2[1]
        estFrame = int(shot[3])
        #ballCount = estFrame #countVar for 
        firstFrame = True
        c= 0
        
        if shot[1] ==teams[0]: #away team # = 0
            name = ':0:'+str(int(shot[7]))
        else:
            name = ':1:'+str(int(shot[7]))
            
        if(estFrame + 25*3 >= len(players)): #shorten max
            newMax =len(players)
            newMin = estFrame - 25*8
            t = len(players) - estFrame -1
            b = 25*8 +1 #includes estFrame
            EFpos = b +1
            locTest = np.zeros(b + t, dtype = bool) 
            dTest = np.zeros(b+t, dtype = bool)
            rVelTest = np.zeros(b+t, dtype = bool)
            AJump = np.zeros(b+t, dtype = bool)
    
    
        elif(estFrame - 25*8 < 0):
            newMax = estFrame + 25*3 +1
            newMin = 0
            t = 25*3 + 1 #includes estFrame
            b = estFrame 
            EFpos = estFrame +1
            locTest = np.zeros(b + t, dtype = bool) 
            dTest = np.zeros(b+t, dtype = bool)
            rVelTest = np.zeros(b+t, dtype = bool)
            AJump = np.zeros(b+t, dtype = bool)
            
        else: #nothing cropped
            newMax = estFrame +25*3 +1 #top range not inclusive
            newMin = estFrame - 25*8
            tot = 25*3 + 25*8 +1
            EFpos = 25*8
            locTest = np.zeros(tot, dtype = bool)
            dTest = np.zeros(tot, dtype = bool)
            rVelTest = np.zeros(tot, dtype = bool)
            AJump = np.zeros(tot, dtype = bool)
    
        
        distance = []
        radVel = []
        prevAMag = []
        thisAMag =[]
    
        
        for i in range(newMin, newMax):#loop for 5 secs either side of the estimated frame
            #25*5 before est frame, 25*5 after, 1 in middle = 251    
            #try to detect the frames where the ball is in the region 
            
            #TEST DISTANCE TO X,Y Given
            ballX = ball['ball:x'][i]
            ballY = ball['ball:y'][i]
            
            if (ballX - shot[4])**2 + (ballY - shot[5])**2 < 400**2: #in 3m radius to the ball
                locTest[c] = True
                
            if firstFrame == True: #wont have previous frame stored
                prevAccns = [] #array that stores values of the previous frames x , y , z accns
                for j in range(1,3):
                    prevAccns.append(ball[i-1][j]-2*ball[i-2][j] + ball[i-3][j]) #using a = vi - vi-1
                prevAMag.append(np.linalg.norm(prevAccns)) #magnitude
                firstFrame = False
                
            thisVel = []
            thisPos = []
            thisAccn = []
            for j in range(1,3):
                thisPos.append(ball[i][j])
                thisVel.append(ball[i][j] - ball[i-1][j]) 
                thisAccn.append(ball[i][j] - 2*ball[i-1][j] + ball[i-2][j])
    
            thisAMag.append( np.linalg.norm(thisAccn))
    
       
                        
            playerPos = []
            playerVel = []
            playerVel.append(players['x'+name][i]-players['x'+name][i-1])
            playerVel.append(players['y'+name][i]-players['y'+name][i-1])
            playerPos.append(players['x'+name][i])
            playerPos.append(players['y'+name][i])
            
            rv = np.subtract(thisVel, playerVel)
            rp = np.subtract(thisPos, playerPos)
            rp2 = rp/np.linalg.norm(rp)
            radVel.append(np.dot(rv,rp2))
            
            if c!=0:
                if((radVel[c] - radVel[c-1])>20 and radVel[c]>0):#positive jump in rad vel
                        rVelTest[c-1] = True #c-1 as we want it true for the KICK frame
            
            
            #Test distance 
            distance.append(np.sqrt((ballX-playerPos[0])**2+(ballY-playerPos[1])**2))
         
            if c !=0:
                    if distance[c-1] <= 100 and distance[c]-distance[c-1] >0 :
                        dTest[c-1] = True
                        
             #AJUMP test
          #accn magnitudes
            threshold = 20
            if(thisAMag[c] - prevAMag[c-1] >= threshold): #tehres a jump
                AJump[c-1] = True #jump occurs
                
                
                
            c+=1
            prevAMag = thisAMag
    
           
            
            #Ball table: ind 1 = x, ind 2 = y, ind 3 = z
        dInd = np.where(dTest == True)
        locInd = np.where(locTest == True)
        rvInd = np.where(rVelTest == True)
        ajInd = np.where(AJump == True)
        inter = np.intersect1d(dInd, locInd)
        inter2 = np.intersect1d(inter, rvInd)
        inter3 = np.intersect1d(inter2, ajInd)
        
        if len(inter) ==1:
            f = estFrame + (inter[0] - EFpos)
            #shots3[shotC]=np.append(shots3[shotC], int(15*round(float(f)/15))/15)
            shots3[shotC]=np.append(shots3[shotC], int(15*round(float(f)/15))/15) #downsize the frame here
            shotT.add_row([shots3[shotC][7], int(name.split(':')[1]), shots3[shotC][8], shots3[shotC][2], shots3[shotC][6]])
        elif len(inter) > 1 and len(inter2)==1: #good
            f = estFrame + (inter2[0] - EFpos)
            shots3[shotC]=np.append(shots3[shotC], int(15*round(float(f)/15))/15)
            shotT.add_row([shots3[shotC][7], int(name.split(':')[1]), shots3[shotC][8], shots3[shotC][2], shots3[shotC][6]])
        elif len(inter2) >1 and len(inter3) ==1:
            f = estFrame + (inter2[0] - EFpos)
            shots3[shotC]=np.append(shots3[shotC], int(15*round(float(f)/15))/15)
            shotT.add_row([shots3[shotC][7], int(name.split(':')[1]), shots3[shotC][8], shots3[shotC][2], shots3[shotC][6]])
            
        shotC +=1
        
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    return shotT
    
    #    for frame in shotT['frame']:
    #shotT is what needs to be returned. 