# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:43:44 2017

@author: user
"""

def XML_metadata(dataName, fileDir):
    from xml.etree import ElementTree
    import os
    os.chdir(fileDir)

    periodStartFrame =[] 
    periodEndFrame =[]

    # Open XML file to get the initial and final frames fot the games
    with open(dataName,'rt') as f:
        tree = ElementTree.parse(f)
        
    for node in tree.iter('period'):
        start = node.attrib.get('iStartFrame')
        end = node.attrib.get('iEndFrame')
        
        if int(end)!=0: #ie the period did happen
            periodStartFrame.append(int(start))
            periodEndFrame.append(int(end))
            
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

            
    return periodStartFrame, periodEndFrame

"""
Created on Tue Oct 17 16:21:57 2017
Function to extract match tracking data as a 2d array 
the term will be strings set out like this:
[[FRAME NUMBER],[player1 data, player2,.....player N], [BALL DATA]]

The function will take in the file name for the tracking data GAMEID.dat
and the arrays holding the start and end frames for each period 
@author: user
"""

def extractMatchData(fileName, periodStartFrame, periodEndFrame, fileDir):
    import os
    os.chdir(fileDir)

    tracData = [[] for i in range(3)] #This array will store the 'chunk' data from
                                    # the .DAT file - excluding frame number
    with open(fileName) as f: 
        for line in f:
            item = line.rstrip() #strip off any whitespace
            item = item.lower()
            
             #if it is within a period, store the tracking data.
            lineArr = item.split(':')
            tracData[0].append(lineArr[0]) # frame number(int) 
            tracData[1].append(lineArr[1]) # players information (string)
            tracData[2].append(lineArr[2]) # ball information (string)

    matchTracData = [[] for i in range(3) ]
    i = 0

    for i in range(len(tracData[0])):
        for j in range(len(periodStartFrame)):
            frameNum = int(tracData[0][i])
            if frameNum >= periodStartFrame[j] and frameNum <= periodEndFrame[j]:
                matchTracData[0].append(tracData[0][i])
                matchTracData[1].append(tracData[1][i])
                matchTracData[2].append(tracData[2][i])
                
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    return matchTracData


"""

"""

def ball_array(matchTracData, periodStartFrame, periodEndFrame):
    ball = [[] for i in range(6)] #number of items we need from ball x,y,
    count = 0
    col1 = matchTracData [0]
    col1 = [int(x) for x in col1] #make int

    p1s = periodStartFrame[0]
    p2s = periodStartFrame[1]
    p1e = periodEndFrame[0]
    p2e = periodEndFrame[0]
    for entry in col1: 
        if entry >= periodStartFrame[0] and entry <= periodEndFrame[0]:#if in first half
            col1[count] = entry - periodStartFrame[0]
        else :#second half
            col1[count] = entry - periodStartFrame[0] -(periodStartFrame[1]-periodEndFrame[0]) -1
        count +=1
        
    p2eShift = p2e - p1s - (p2s - p1e) +1
    p1eShift = p1e - p1s
    p2sShift = p1eShift + 1
    p1sShift = 0

    count = 0
    for i in matchTracData[2]:
        ballArr = i.split(';')
        ballArr = ballArr[0] # get rid of the second term in the array (it's empty due to format)
        ballArr = ballArr.split(',')
        subcount =0
        ballcount =0
        for c in ballArr:# ball will be [frames], [x], [y], [home], [alive/dead]
            if subcount==0:
                ball[ballcount].append(col1[count]) #frames
                ballcount +=1
                if count >= p2sShift: #second half 
                    temp = -float(c)
                    ball[ballcount].append(temp) # invert the x 
                else:
                    temp = float(c)
                    ball[ballcount].append(temp) # x
                ballcount +=1
            elif subcount == 1:
                if count >= p2sShift: #second half 
                    temp = -float(c)

                    ball[ballcount].append(temp) # invert y 
                else:
                    temp = float(c)

                    ball[ballcount].append(temp) # y
                
                ballcount += 1
            elif subcount ==2:
                temp = float(c)

                ball[ballcount].append(temp) #z
                ballcount +=1
            elif subcount <= 5 and subcount >=4: #owning team and alive dead
                ball[ballcount].append(c)
                ballcount +=1
            subcount +=1
                
#	       if subcount <= 5 and subcount >= 4: #ignore the 'set away' or 'whistle' optional tag (7th tag)
#	            #if last two terms -> strings   
#	            ball[subcount].append(c)
#	            subcount = subcount +1
#	        elif subcount < 4:
#	            temp = float(c)
#	            ball[subcount].append(temp)
#	            subcount = subcount +1 
#            elif subcount==1 or subcount ==2:
#                if count <
        count += 1
    return ball

"""
Created on Tue Oct 17 16:04:31 2017
Function that takes in matchTracData and the period Start and end frames
to return a dictionary for home and away teams, with each team having their own dictionary.
The team dictionaries will have keys equal to the players shirt number. 
The data for each key will be a series of arrays: [frame num, x,y,velocity]

If a player is subbed on later in the game, the first frame is = to the first frame 
after he is subbed on -> not all are the same length! 
If a plaer is subbed off, the last frame number will be equal to the frame where he is subbed off
therefore != last frame number of the game.
@author: user
"""
def createTeamDictionary(matchTracData, periodStartFrame, periodEndFrame):
    #Creating a dictionary to contain all the player information
    homePlayers = {}
    awayPlayers = {}
    teams = {'home' : homePlayers, 'away' : awayPlayers}
    startFrame = int(matchTracData[0][0])
    currentFrame = startFrame 
    for i in matchTracData[1]:
        playerArr = i.split(';') #each players data. Last term is empty string after last ;
        playerArr.remove('') # Remove the last empty element in the list
       # nOfPlayers = len(playerArr) 
        for c in playerArr:
            playerData = c.split(',')
            playerTeam = int(playerData[0])
            playerInfo = [] # This list will contain frame number, x, y, vel
            if currentFrame == periodEndFrame[0]+1: #NEEDS EDITING TO MAKE APPLICABLE FOR EXTRA TIME
                #then its first half over -> 
                currentFrame = periodStartFrame[1]
            
            if playerTeam == 0: # 0 = away team
                playerInfo.append(currentFrame)  # frame
                playerInfo.append(float(playerData[3])) # x
                playerInfo.append(float(playerData[4])) # y 
                playerInfo.append(float(playerData[5])) # vel
                playerNo = int(playerData[2])
                if playerNo not in awayPlayers:
                    awayPlayers[playerNo] = [playerInfo] # the player array
                else :
                    awayPlayers[playerNo].append(playerInfo)
            elif playerTeam == 1:
                playerInfo.append(currentFrame)  # frame
                playerInfo.append(float(playerData[3])) # x
                playerInfo.append(float(playerData[4])) # y 
                playerInfo.append(float(playerData[5])) # vel
                playerNo = int(playerData[2])
                if playerNo not in homePlayers:
                    homePlayers[playerNo] = [playerInfo] # the player array
                else :
                    homePlayers[playerNo].append(playerInfo)
        currentFrame += 1       
        
    return teams

def createDic(matchTracData):
    Numbers = { 1 : [4,5,6], 2 : [7,8,9]}
    Letters = {} 
    blah = {'one' : Numbers , 'away' : Letters}
    
    
    return blah




def makeAstropyTable(matchTracData, teams, periodStartFrame, periodEndFrame):
    
    from astropy.table import Table
    import numpy as np
    
    col1 = matchTracData[0] #FRAMES COLUMN]
    col1 = [int(x) for x in col1] #make int
    count =0
    
    p1s = periodStartFrame[0]
    p2s = periodStartFrame[1]
    p1e = periodEndFrame[0]
    p2e = periodEndFrame[1]
    
    print(p1s)
    print(p2s)
    
    for entry in col1: 
        if entry >= periodStartFrame[0] and entry <= periodEndFrame[0]:#if in first half
            col1[count] = entry - periodStartFrame[0]
        else :#second half
            col1[count] = entry - periodStartFrame[0] -(periodStartFrame[1]-periodEndFrame[0]) -1
        #print(col1[count])
        count +=1
    
    p2eShift = p2e - p1s - (p2s - p1e) +1
    p1eShift = p1e - p1s
    p2sShift = p1eShift + 1
    p1sShift = 0
    
    t = Table([col1], names = ('Frames',), dtype = ('i',))
    
    for team in teams: #loop through teams
        for player in teams[team]: #loop over each player
            count = 0
            x = np.empty(len(col1)) #empty array same length as frames == total game time
            y = np.empty(len(col1))
            x[:] = np.NaN #initialise to NaN - do this as some players are subbed on/off 
            y[:] = np.NaN#this means all players can have the same length arrays, thus making column calculations easier (ie less loops)
            playerNum = player
            for frame in teams[team].get(player): #loop over each frame element for that player 
                #index = col1.index(frame[0]) #get the index the current frame is in the big frme array
                #store data
                
                if frame[0] >= periodStartFrame[0] and frame[0] <= periodEndFrame[0]:#if in first half
                    index = frame[0] - periodStartFrame[0]
                    #print('hey')
                    
                    x[index] = frame[1] #overwrite nan with the x 
                    y[index] = frame[2] #same with y 
                else :#second half
                    index = frame[0] - periodStartFrame[0] - (periodStartFrame[1] - periodEndFrame[0] ) -1
                    #print('ho')
                    #Fix the coordinates so that away team and home team ALWAYS attack in same direction
                    x[index] = -frame[1]
                    y[index] = - frame[2]
                    
#                x[index] = frame[1] #overwrite nan with the x 
#                y[index] = frame[2] #same with y 
                count += 1
               #if count % 1000 == 0:
                #    print(count)
                #print('It works')
            #here we need to append the players to the data frame
            if team == 'home':
                teamInt = 1
                tempTable = Table([x,y], names = ('x:'+str(teamInt)+':'+str(playerNum), 'y:'+str(teamInt)+':'+str(playerNum)), dtype=('f','f'))
                t.add_columns(tempTable.columns.values())
            else: #away
                teamInt = 0
                tempTable = Table([x,y], names = ('x:'+str(teamInt)+':'+str(playerNum), 'y:'+str(teamInt)+':'+str(playerNum)))
                t.add_columns(tempTable.columns.values())
                
    return t


