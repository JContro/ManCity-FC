def extract(fileNames, fileDir):
    
    import numpy as np
    import extractionFunctions as ef
    from astropy.table import Table
    
    
    periodStartFrame =[] 
    periodEndFrame =[]
    startFrameFlag = True
    frameNum =0 #save for later
    startFrame =0
    
    # import module for opening xml metadata files adn returning the startframes and end frames
    # remember to cancel the same text.
    periodStartFrame = ef.XML_metadata(fileNames[1], fileDir)[0] #metadata 
    periodEndFrame = ef.XML_metadata(fileNames[1], fileDir)[1]
    
    # Open the dat file with the position of all the players + ball
    matchTracData = ef.extractMatchData(fileNames[0], periodStartFrame, periodEndFrame, fileDir)
    i = 0
    
    ball = ef.ball_array(matchTracData, periodStartFrame, periodEndFrame)
    print(periodStartFrame)
    print(periodEndFrame)
    teams = ef.createTeamDictionary(matchTracData, periodStartFrame, periodEndFrame)
    
    #print(teams)
    
    ## #Try store data in an astroPy table. 
    #col1 = matchTracData[0] #FRAMES COLUMN]
    #col1 = [int(x) for x in col1] #make int
    #t = Table([col1], names = ('Frames',), dtype = ('i',))
    #for team in teams: #loop thru teams
    #    for player in teams[team]: #loop over each player
    #        count = 0
    #        x = np.empty(len(col1)) #empty array same length as frames == total game time
    #        y = np.empty(len(col1))
    #        x[:] = np.NaN #initialise to NaN - do this as some players are subbed on/off 
    #        y[:] = np.NaN#this means all players can have the same length arrays, thus making column calculations easier (ie less loops)
    #        playerNum = player
    #        for frame in teams[team].get(player): #loop over each frame element for that player 
    #            index = col1.index(frame[0]) #get the index the current frame is in the big frme array
    #            #store data
    #            x[index] = frame[1] #overwrite nan with the x 
    #            y[index] = frame[2] #same with y 
    #            count += 1
    #        #here we need to append the players to the data frame
    #        if team == 'home':
    #            teamInt = 1
    #            tempTable = Table([x,y], names = ('x:'+str(teamInt)+str(playerNum), 'y:'+str(teamInt)+str(playerNum)))
    #            t.add_columns(tempTable.columns.values())
    #        else: #away
    #            teamInt = 0
    #            tempTable = Table([x,y], names = ('x:'+str(teamInt)+str(playerNum), 'y:'+str(teamInt)+str(playerNum)))
    #            t.add_columns(tempTable.columns.values())
    
    tbl = ef.makeAstropyTable(matchTracData, teams, periodStartFrame, periodEndFrame)
    ballTbl = Table([ball[0], ball[1], ball[2], ball[3], ball[4], ball[5]], names =('frames', 'ball:x', 'ball:y', 'ball:z', 'ball:own', 'ball:status'), dtype = ('i','f','f','f','str','str'))
    
    # print(tbl[1])
    tbl.remove_row(-1)
    tbl.write('testTbl.fits', overwrite = True)
    ballTbl.write('testBall.fits', overwrite = True)
#   ballTbl.write('debugBall.fits', overwrite = True)
    
    c =0
    start =[]
    end = []
    for entry in periodStartFrame: #Shift the frames as its now zero shifted
        if c==0:#first half
            start.append(0)
            end.append(periodEndFrame[c]-entry)
        else:
            start.append(entry - periodStartFrame[0] - (entry - periodEndFrame[0])+1) 
            end.append(periodEndFrame[c] - periodStartFrame[0]-(entry-periodEndFrame[0])) 
        c+=1
        
    periods = Table([start, end], names = ('Start Frame', 'end frame'))
    print(periods)
    #periods.write('periodTableTest.fits', overwrite = True)
    import Smoothing3 as smoot
    playersSmoothDown,  ballSmoothDown = smoot.smoothing(periods, ballTbl, tbl)
    
    #ballSmoot = Table(tbl['Frames'], names = 'frames')
    #playersSmoot = Table(tbl['Frames'], names = 'frames')
    #import scipy.ndimage
    #ballSmoot['ball:x'] = scipy.ndimage.uniform_filter1d(ball['ball:x'],15)
    #ballSmoot['ball:y'] = scipy.ndimage.uniform_filter1d(ball['ball:y'],15)
    #ballSmoot['ball:z'] = scipy.ndimage.uniform_filter1d(ball['ball:z'],15)
    #ballSmoot['ball:status'] = ball['ball:status']
    #
    #
    #playersSmoot['ball:x'] = scipy.ndimage.uniform_filter1d(ball['ball:x'],15)
    #playersSmoot['ball:y'] = scipy.ndimage.uniform_filter1d(ball['ball:y'],15)
       
    import isolateShots2 as IS
    import isolatePassesFn as IP
    shotTbl = IS.isolateShots(periods, tbl, ballTbl, fileNames, fileDir)
    passTbl = IP.isolatePasses(periods, tbl, ballTbl, fileNames, fileDir)
    
    #for frame in shotTbl['frame']:
    #    print(frame)
    #    #convert to the index in the smoothed down tbl
    #    nfs.append(int(15*round(float(frame)/15))/15)
    #shotTbl['frame2'] = nfs
    import analyseFn as AN
    varbs = AN.getVars(periods, playersSmoothDown, ballSmoothDown, fileNames, fileDir)
    
    
    varbs.write('VarTable'+fileNames[0].split('.')[0]+'.fits', overwrite = True)
    playersSmoothDown.write('playerTable'+fileNames[0].split('.')[0]+'.fits', overwrite = True)
    ballSmoothDown.write('ballTbl'+fileNames[0].split('.')[0]+'.fits', overwrite = True)

    return shotTbl, passTbl
    
    #### now trying to calc Nearest Neighbour distances - will be its own FUNCtion 
    ##excludes extra time for now 
    #homeNND ={}
    #awayNND = {}
    #NNDs = {'home' : homeNND, 'away':awayNND}
    #for team in teams:#loop over each team home and away 
    #    for player in  teams[team]: #loop over each teams players
    #        for frame in player: #loop over each element of player
    #            currentFrame = frame[0] # current frame
    #            if (currentFrame >= periodStartFrame[0] and currentFrame<=periodEndFrame[0] 
    #                and team == 'home' or currentFrame >= periodStartFrame[1] and currentFrame<=periodEndFrame[1] 
    #                and team == 'away'): 
    #                    #if its home team and first half or away team and second half - shoot left (-x) to right(+x)
    #                    if frame[1] > 0: #if player is in attacking half or the pitch, calc NNDs
    #                        distances = calculateNND(frame, team, teams)
    #            elif (currentFrame >= periodStartFrame[0] and currentFrame<=periodEndFrame[0] 
    #                and team == 'away' or currentFrame >= periodStartFrame[1] and currentFrame<=periodEndFrame[1] 
    #                and team == 'home'):
                        #if away team and first half or home and second half - shooting righ (+x) t to left (-x)
    #fig = plt.figure()
    #ax = plt.axes()
    #x = []
    #y =[]
    #i =0 
    #while i <=100:
    #    x.append(teams['away'][33][i][1])
    #    y.append(teams['away'][33][i][2])
    #    i+=1
    #plt.plot(x,y)
    #
    #tempArr = []
    #people = [[] for i in range(26)]#array for allpeople on the pitch incl ref
    #home = [[] for i in range(11)]
    #away = [[] for i in range(11)]
    ##tracdata will now have all game play data in. 
    #
    
    #    subcount = 0
    #
    #    for c in playerArr:
    #        people[subcount].append(c)
    #        subcount += 1
    #        if subcount != len(playerArr)-1:
    #            tempArr.append(c.split(','))
    #        subcount +=1
    #        for j in tempArr:
    #            people[subcount].append(tempArr[subSubCount])
    #            subSubCount =+1
    #            subcount =+1 
    #players now has all people data in an array with dimensions 30xnumber of frames.
    #need to extract the two teams player data.
    #to be able to store the 
    #
    #
    #
    #Test animation 
    #fig = plt.figure()
    #ax = plt.axes()
    #point = ax.plot()
    #
    #def init():
    #    point.set_data()
    #    return point,
    #
    #def animate(frame):
    #    x = ball[0][frame]
    #    y = ball[1][frame]
    #    point.set_data(x,y)
    #    return point
    #
    #anim = animation.FuncAnimation(fig, animate, init_func = init,
    #                               frames = 10000, interval = 20, blit = True)
    #
    #anim.save('basic_animation.mp4', fps = 25)
    #plt.show
    #
    #
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection ='3d')
    #ax.plot_wireframe(ball[0][0:1000], ball[1][0:1000], ball[2][0:1000])
    #plt.xlabel('x pitch length')
    #plt.ylabel( 'y pitch width')
    #plt.show()
    #
