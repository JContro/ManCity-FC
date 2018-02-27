# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 11:01:09 2017

@author: user
"""
def getVars(periods, plTbl, ballTbl, fileNames, fileDir):
    from astropy.table import Table
    import numpy as np
    from xml.etree import ElementTree
    import os
    os.chdir(fileDir)
    
    
    data = plTbl
    ball = ballTbl
    #distances = Table([data['Frames']], names = ('Frames',), dtype = ('i',)) #New astropy table for the NND calculations
    colCount = 0
    cols = []
    NNDArr = []
    NND = Table([data['Frames']], names = ('Frames',), dtype = ('i',))
    bigTable = Table([data['Frames']], names = ('Frames',), dtype = ('i',))
    
    for col in data.columns:#loops thru column names where col == string name of each col
        cols.append(col) #Store column keys to use in next loop 
    distances = []
    
    for col in cols:#loop through stored keys
        rowCount = 0
        if colCount != 0 and (colCount-1)%3 ==0 and colCount%2!=0: #Not frames and every x
            NNDArr =[] #reset array as its for new player
            for row in data:
               # print(rowCount)
                #print(col)
                #if(colCount-1)%3 ==0 and colCount%2!=0: #IE every third column -> x columns
                #print(col)
                name1 = col.split(':') #array with [x, team num, player num]
    #            if(col == 'x:0:20'):
    #                print(rowCount)
    
                #makes sure colcount is ODD - thus will be the x never the y column
                #now here accesses every players x column, start doing NND calculation.
                colCountTwo = 1 # new count variable for nested loops.
                    #new count starts at 1 - First x coord of the table
                distances = []
                d2 =[]
    
                #print(distances)
                while colCountTwo < len(cols):#while second count is less than total columns number
                    if (colCountTwo != colCount) and (colCountTwo-1)%3 ==0 and colCountTwo%2!=0: #IE if the same player ISNT being accessed
                        #and make sure that the columns only access the x too
                       #print(colCountTwo)
                        name2 = cols[colCountTwo].split(':') #array with same above
                        if name1[1] != name2[1]: # not on same team
                            dx = data[col][rowCount] - data[cols[colCountTwo]][rowCount]
                            dy = data[cols[colCount+3]][rowCount] - data[cols[colCountTwo + 3]][rowCount]
                            distances.append(np.sqrt(dx**2 + dy**2))
                            
    
                        
                       #print(distances)
                    colCountTwo +=1 #Increment to access the next x 
                d2 = [x for x in distances if np.isnan(x) != True]
                if len(d2) == 0:#all nans
                    NNDArr.append(np.nan)
                else:
                    NNDArr.append(min(d2))
                rowCount += 1
        
            #end of rows
            NND['NND:'+ name1[1] +':' + name1[2]] = NNDArr
            bigTable['NND:'+ name1[1] +':' + name1[2]] = NNDArr
        colCount+=1
    
    import matplotlib.pyplot as plt
    
    hNNDAvg = []
    aNNDAvg = []
    hCloseNNDAvg = []
    aCloseNNDAvg = []
   
    rowCount = 0 
    for row in NND:
        colCount = 0
        hNND = []
        aNND =[]
        hCloseNND = []
        aCloseNND =[]
        
        hplayers  = [] #all players on the team
        aplayers  = [] #all players on the team
        #Now do for 5 attacking players
        sub = 0 #count
        
        for players in data[rowCount].colnames:# loop through players - store 5 most up front strings
            if sub != 0 and (sub-1)%3 ==0 and sub%2!=0: # every xs
                #print(sub)
                if players.split(':')[1] == '1': #home
                    hplayers.append([data[players][rowCount], int(players.split(':')[2])]) #store x coord, and shirt num
                    #print('1')
                else:
                    aplayers.append([data[players][rowCount], int(players.split(':')[2])]) #store x coord, and shirt num
                    #print('0')
            sub += 1
        #now have arrays of all players xcoords and their shirt number split to teams
       # print(hplayers)
        hplayers.sort(reverse = True) #sort in descending order, get 5 closest - sorts by the x coord
        htemp = hplayers[:5]
        aplayers.sort() #sort in ascending order, get 5 smallest (closest to -x goal) 
        atemp = aplayers[:5]
        for col in NND.columns:
                        
                if colCount != 0:
                    if col.split(':')[1] == '1': #home
                        hNND.append(NND[col][rowCount])
                        for item in htemp: # loop thru 2d list
                            if int(col.split(':')[2]) ==  item[1]: #in list
                                hCloseNND.append(NND[col][rowCount])
                    else:
                        aNND.append(NND[col][rowCount])
                        for item in atemp: # loop thru 2d list
                            if int(col.split(':')[2]) ==  item[1]: #in list
                                aCloseNND.append(NND[col][rowCount])
                                
                colCount += 1
        hNND = [x for x in hNND if np.isnan(x) != True]
        aNND = [x for x in aNND if np.isnan(x) != True]
        hCloseNND = [x for x in hCloseNND if np.isnan(x) != True]
        aCloseNND = [x for x in aCloseNND if np.isnan(x) != True] #remove nans
        
        hCloseNNDAvg.append(np.mean(hCloseNND))
        aCloseNNDAvg.append(np.mean(aCloseNND))
    
        hNNDAvg.append(np.mean(hNND))
        aNNDAvg.append(np.mean(aNND))
        
        rowCount += 1
    
    bigTable['1:NNDAvg'] = hNNDAvg
    bigTable['0:NNDAvg'] = aNNDAvg
    bigTable['1:CloseNNDAvg'] = hCloseNNDAvg
    bigTable['0:CloseNNDAvg'] = aCloseNNDAvg

    


    
    
#    plt.figure()
#    plt.plot(hNNDAvg)
#    plt.title('Home team (Brighton) average NND wrt frames')
#    plt.xlabel('frames')
#    plt.ylabel('NND (cm)')
#    plt.show()
#    plt.figure()
#    plt.plot(aNNDAvg)
#    plt.title('Away team (Man City) average NND wrt frames')
#    plt.xlabel('frames')
#    plt.ylabel('NND (cm)')
#    plt.show()
#    
    
        
    
    #    
                       # if len(distances.columns) > 1:
                            
    #                    for columns in distances.columns: #loop through NND
    #                       if columns != 'Frames':
    #                            nndName = columns.split(':')
    #                            
    #                            if((nndName[1]==name1[1] and nndName[2]==name1[2]
    #                                and nndName[3] == name2[1] and nndName[4] == name2[2])or 
    #                                (nndName[1]==name2[1] and nndName[2]==name2[2]
    #                                and nndName[3] == name1[1] and nndName[4] == name1[2])):
    #                                repeat = True # stops storing repeated NND values
    #                
    #                if repeat == False:
    #                #Then calculate the NND's
    #                #all column data
    #                    x1 = data[col] #first x coords
    #                    y1 = data[cols[colCount+1]]
    #                    x2 = data[cols[colCountTwo]]
    #                    y2 = data[cols[colCountTwo + 1]]
    #                    
    #                    distance = np.sqrt((x1 - x2)**2 + (y1-y2)**2) # WIll be column dataType
    #                    
    #                    #Have distance, but need to know what players its between 
    #                    #nomenclature: NND:player 1 team: player 1 number:player2team: player2 number
    #                    
    #                    newName = 'D:'+str(name1[1])+':'+str(name1[2])+':'+str(name2[1])+':'+str(name2[2]) +':'
    #                    distance.name = newName
    #                    distances.add_column(distance)
                        
                    
       # colCount+=1
    
    #Have the distances for each player to each other, now  get the
    #NND = Table([data['Frames']], names = ('Frames',), dtype = ('i',))
    #count = 0 
    #for col in cols: #loop over players in the table
    #    if count > 0 and (count -1) %2 ==0: #every x col
    #        name = col.split(':')
    #        
    #        strCheck = ':'+name[1] +':' + name[2] + ':'
    #        team = name[1]
    #        teamSt = ':' + team + ':'
    #        FrameDist = []
    #        NNDArr = []
    #        rowCount = 0
    #        for row in distances: #loop thru rows
    #            count2 = 0
    #            for distancecol in distances.columns: #over distances columns
    #                if count2 >0:
    #                    names = distancecol.split(':')
    #                    name1 = ':' + names[1] +':' + names[2] +':'
    #                    name2 = ':' + names[3] + ':' + names[4] + ':' 
    #                    print('yo')
    #                    if (strCheck in name1 or strCheck in name2) and (teamSt in name1 != teamSt  in name2) : #if this is a distance for said player
    #                        FrameDist.append(distances[distancecol][rowCount]) # store distances only for people in opposite 
    #                count2 += 1
    #            NNDArr.append(min(FrameDist))
    #            rowCount += 1
    #            
    #        NND['NND' + strCheck] = NNDArr
    #    count += 1
    #            
        
        
    
    
    # Now work out the distance of each player to the goal centre (Y = 0, x = +/- 0.5 * pitch size)
    with open(fileNames[1],'rt') as f:
            tree = ElementTree.parse(f)
            
    for node in tree.iter('match'):
            xSize = node.attrib.get('fPitchXSizeMeters') #in Metres
        
    xSize = float(xSize) * 100 #Convert to cm
    xSizeArr = np.zeros(len(data['Frames']))
    xSizeArr[:] = xSize
    for column in periods.columns:
        startFrames = periods[column]
        endFrames = periods[column]
    
    #firstHalf = tbl[startFrame[0]:endFrame[0]]
    #secondHalf = tbl[startFrame[1]:endFrame[1]]
    #extraT = False
    #
    #if len(startFrames) ==4: #extraTime
    #    XfirstHalf = tbl[startFrame[2]:endFrame[2]]
    #    XsecondHalf = tbl[startFrame[3]:endFrame[3]]
    
    
        
    #Loop through the players, calculating distance to attacking goal 
    colCount =0
    goalD = Table([data['Frames']], names = ('Frames',), dtype = ('i',))
    for col in cols:
        if colCount > 0 and (colCount-1)%3 ==0 and colCount%2 !=0: #IE every x column -> every 3rd which is oddd
            #now here accesses every players x column, start doing distance calculation.
            name = col.split(':')
            team = name[1]
            c =0
            x = data[col]
            y = data[cols[colCount +3]]
            
            RHdistance = np.sqrt((x - (0.5*xSizeArr))**2 + y**2)
            RHdistance.name = 'RHS:'+str(team) + ':' + str(name[2])
            RHangle = np.arctan(abs(y)/abs((-0.5*xSizeArr + x)))
            RHangle.name = 'RHSANG:' + str(team) + ':' + str(name[2])
            
            LHdistance = np.sqrt((x+0.5*xSizeArr)**2 + y**2) #to -x goal
            LHdistance.name = 'LHS:'+str(team) + ':' + str(name[2])
            LHangle = np.arctan(abs(y)/abs((0.5*xSizeArr + x)))
            LHangle.name = 'LHSANG:' + str(team) + ':' +str(name[2])
                
            goalD.add_columns([RHdistance,RHangle, LHdistance, LHangle])#ANGLE IN RADIANS
            bigTable.add_columns([RHdistance,RHangle, LHdistance, LHangle]) #distance each player to goal 
        colCount +=1
    
    #Number of players in the attacking half of the pitch
    #For the home team thats +x half
    #For the away team thats -x half
    nAttackPlayers = Table([data['Frames']],names = ('Frames',), dtype = ('i',))
    rowCount =0
    home =[] #Arrays to store the counts for each frame
    away =[]
    
    for row in data:
        nHomeP = 0
        nAwayP = 0 #counters for each team
        colCount = 0
        for col in cols: #loop through columns and rows - count up players in attacking half
        
            if colCount > 0 and (colCount -1)%3 == 0 and colCount%2 !=0 :#xCoords
                teamNum = col.split(':')[1] #team number
                
                if np.isnan(data[col][rowCount]) == False:
                    if teamNum == '1' and data[col][rowCount] > 0: #hom
                        nHomeP += 1
        
                    elif teamNum =='0' and data[col][rowCount]<0: #away
                        nAwayP += 1
            colCount +=1 
        
                
        home.append(nHomeP)
        away.append(nAwayP)
        rowCount += 1
    
    nAttackPlayers['Home team attacking players'] = home
    nAttackPlayers['Away team attacking players'] = away
    bigTable['1:nAtt'] = home
    bigTable['0:nAtt'] = away
    
    #Number of defending players between their goal and the ball 
    #So if home attacks to +x, the code will calculate number of players between the balls current
    #position and that goal
    ballD = Table([data['Frames']],names = ('Frames',), dtype = ('i',)) #Ball distance and angles
    goalWidthS = 7.32*100 #post to post in cm
    goalWidth  = np.zeros(len(data['Frames']))
    goalWidth[:] = goalWidthS
    
    LHDistance = np.sqrt((ball['ball:x']+0.5*xSizeArr)**2 + ball['ball:y']**2) #-x goal
    RHDistance = np.sqrt((ball['ball:x'] - (0.5*xSizeArr))**2 + ball['ball:y']**2)
    LHAngle = np.arctan(abs(ball['ball:y'])/abs((0.5*xSizeArr + ball['ball:x'])))
    RHAngle = np.arctan(abs(ball['ball:y'])/abs((-0.5*xSizeArr + ball['ball:x'])))
    ballD['ball:LHD'] = LHDistance
    ballD['ball:LHA'] = LHAngle
    ballD['ball:RHD'] = RHDistance
    ballD['ball:RHA'] = RHAngle
    bigTable['ball:LHD'] = LHDistance
    bigTable['ball:LHA'] = LHAngle
    bigTable['ball:RHD'] = RHDistance
    bigTable['ball:RHA'] = RHAngle    
    
    #now use this to work out the angle the goal gets 
    RHPoneD = np.sqrt((ball['ball:x']-0.5*xSizeArr)**2 + (ball['ball:y'] -0.5*goalWidth)**2)#distances to rh posts
    RHPtwoD = np.sqrt((ball['ball:x']-0.5*xSizeArr)**2 + (ball['ball:y']+0.5*goalWidth)**2)
    LHPoneD = np.sqrt((ball['ball:x']+0.5*xSizeArr)**2 + (ball['ball:y'] - 0.5*goalWidth)**2)#distances to lH posts
    LHPtwoD = np.sqrt((ball['ball:x']+0.5*xSizeArr)**2 + (ball['ball:y'] + 0.5*goalWidth)**2)
    
    RHFullA = np.arccos((RHPoneD**2 + RHPtwoD**2 - goalWidth**2)/(2*RHPoneD*RHPtwoD)) #cosine rule
    LHFullA = np.arccos((LHPoneD**2 + LHPtwoD**2 - goalWidth**2)/(2*LHPoneD*LHPtwoD)) #cosine rule
    bigTable['ball:RHFullA'] = RHFullA
    bigTable['ball:LHFullA'] = LHFullA
    
    #cosine rule to calculate the angle between Post 1 and ball and post2 and ball
    #Post one is defined as the post in the positive y part of field
    RHPoneA = np.arccos((RHPoneD**2 - ballD['ball:RHD']**2 + (0.5*goalWidth)**2)/(2*RHPoneD*0.5*goalWidth))
    RHPtwoA = np.arccos((RHPtwoD**2 - ballD['ball:RHD']**2 + (0.5*goalWidth)**2)/(2*RHPtwoD*0.5*goalWidth))
    
    LHPoneA = np.arccos((LHPoneD**2 - ballD['ball:LHD']**2 + (0.5*goalWidth)**2)/(2*LHPoneD*0.5*goalWidth))
    LHPtwoA = np.arccos((LHPtwoD**2 - ballD['ball:LHD']**2 + (0.5*goalWidth)**2)/(2*LHPtwoD*0.5*goalWidth))
    
    #we have  the angles between the goal line and the ball now
    #for a player to be in this area, the angle between 
    rowCount = 0
    AwayDefs =[]
    HomeDefs =[]
    hNan = []
    aNan =[]
    for row in data: #loop through data frame by frame
        colCount = 0
        nAwayDefs = 0 #Number of away players in goal defense region per frame
        nHomeDefs =0
        for col in data.columns:
             if colCount != 0 and (colCount-1)%3 ==0 and colCount%2!=0: #Not frames and every x
                 #loop through players row by row
                 #Work out their angles to their DEFENDING goalPosts to see if they are within the defensve region
                 
                 name = col.split(':')
                 
                 if name[1] == '1':#home attacks +x aka RH, DEFENDS TO LH
                     dName = 'LHS:'+name[1]+':'+name[2]
                     PoneD = np.sqrt((data[col][rowCount]-0.5*xSize)**2 + (data[cols[colCount+3]][rowCount] -0.5*goalWidthS)**2)
                     PtwoD = np.sqrt((data[col][rowCount]-0.5*xSize)**2 + (data[cols[colCount+3]][rowCount] +0.5*goalWidthS)**2)
                     angleOne = np.arccos((PoneD**2 + (0.5*goalWidthS)**2 - goalD[dName][rowCount]**2)/(goalWidthS*PoneD))
                     angleTwo = np.arccos((PtwoD**2 + (0.5*goalWidthS)**2 - goalD[dName][rowCount]**2)/(goalWidthS*PtwoD))
                     
                     if np.isnan(angleOne) == False and np.isnan(angleTwo) == False and angleOne <= LHPoneA[rowCount] and angleTwo <= LHPtwoA[rowCount]:
                         nHomeDefs +=1
                 else: #away attacks -x DEFENDS +x (RHS)
                     dName = 'RHS:'+name[1]+':'+name[2]
                     PoneD = np.sqrt((data[col][rowCount]+0.5*xSize)**2 + (data[cols[colCount+3]][rowCount] -0.5*goalWidthS)**2)
                     PtwoD = np.sqrt((data[col][rowCount]+0.5*xSize)**2 + (data[cols[colCount+3]][rowCount] +0.5*goalWidthS)**2)
                     angleOne = np.arccos((PoneD**2 + (0.5*goalWidthS)**2 - goalD[dName][rowCount]**2)/(goalWidthS*PoneD))
                     angleTwo = np.arccos((PtwoD**2 + (0.5*goalWidthS)**2 - goalD[dName][rowCount]**2)/(goalWidthS*PtwoD))
                     
                     if np.isnan(angleOne) == False and np.isnan(angleTwo) == False and angleOne <= RHPoneA[rowCount] and angleTwo <= RHPtwoA[rowCount]:
                         nAwayDefs +=1
             colCount+=1
        AwayDefs.append(nAwayDefs)
        HomeDefs.append(nHomeDefs)
        rowCount +=1
    
#    fig = plt.figure()
#    plt.plot(AwayDefs, 'r-')
#    plt.plot(HomeDefs, 'b-')
#    plt.show(fig)
    
    bigTable['1:nDefs'] = HomeDefs
    bigTable['0:nDefs'] = AwayDefs
    #Concatonate the tables. 
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    return bigTable
    
            
        