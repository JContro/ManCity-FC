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
    
    # Use the ball_array ft from the extractionFunctions to get the ball array. It needs the data and the periods of the game (to get relevant data)
    ball = ef.ball_array(matchTracData, periodStartFrame, periodEndFrame)
    # Creates a Python Dictionary with the data
    teams = ef.createTeamDictionary(matchTracData, periodStartFrame, periodEndFrame)
    
    # Creates an astropy table with all the players coordinates from the files
    tbl = ef.makeAstropyTable(matchTracData, teams, periodStartFrame, periodEndFrame)
    # Create an astropy table with the ball array data
    ballTbl = Table([ball[0], ball[1], ball[2], ball[3], ball[4], ball[5]], names =('frames', 'ball:x', 'ball:y', 'ball:z', 'ball:own', 'ball:status'), dtype = ('i','f','f','f','str','str'))
    
    # print(tbl[1])
    tbl.remove_row(-1)
    tbl.write('testTbl.fits', overwrite = True)
    ballTbl.write('testBall.fits', overwrite = True)

    
    c =0
    start =[]
    end = []
    for entry in periodStartFrame: # Shift the frames as its now zero shifted
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
    
   
    import isolateShots2 as IS
    import isolatePassesFn as IP
    shotTbl = IS.isolateShots(periods, tbl, ballTbl, fileNames, fileDir)
    passTbl = IP.isolatePasses(periods, tbl, ballTbl, fileNames, fileDir)
    
   
    import analyseFn as AN
    varbs = AN.getVars(periods, playersSmoothDown, ballSmoothDown, fileNames, fileDir)
    
    
    varbs.write('VarTable'+fileNames[0].split('.')[0]+'.fits', overwrite = True)
    playersSmoothDown.write('playerTable'+fileNames[0].split('.')[0]+'.fits', overwrite = True)
    ballSmoothDown.write('ballTbl'+fileNames[0].split('.')[0]+'.fits', overwrite = True)

    return shotTbl, passTbl
    
   
