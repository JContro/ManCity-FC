#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:34:57 2017

This code contains a function that smoothes the data and returns a file that is smoothed
It will also plot some graphs to compare the original data and the smoothed one 

@author: Jack
"""
def smoothing(periods, balltbl, pltbl):
    
    from astropy.table import Table, Column
    import scipy.ndimage
    from matplotlib import pyplot as plt
    import numpy as np
    # Example string that opens the table that needs smoothing
    #TblString = 'tableTest.fits'
    T = pltbl
    #periods = Table.read('periodTableTest.fits')
    ball = balltbl #import ball
    p = {}          # initialise the player dictionary 
    #switch = False
    frames = T['Frames'][2:]
    frames = np.subtract(frames, 2)

    frames = frames[::15]
    frames = np.arange(frames.size)*15
    # Create a new astropy table that will contain all the smoothed data
    NewTable = Table([frames], names = ['Frames',], meta={'name': 'Smoothed Player Table'})
    ballSmooth = Table([frames], names = ['Frames',], meta={'name': 'Smoothed ball Table'})
    
    count = 0
    for col in T.colnames:
        count += 1
        print(count)
        
        #p['Frames'] = T['Frames'] # P contains the frames
        
        if col != 'Frames': # Exclude the frames because we don't want them

            p['r'] = T[col]                 # position
            v = T[col][1:] - T[col][:-1]    # velocity
            a = v[1:] - v[:-1]              # Acceleration
            p['r'] = p['r'][2:]              
            p['v'] = v[1:]                  # Add to the player dictionary
            p['a'] = a
            
            
            
            threshold = 120
            
           
            
    #        for i in range(len(p['a'])):           
    #            if p['a'][i]**2 > threshold:
    #                p['a'][i] = 0       # artificially set the accel and the vel to 0, because it's not a glitch
    #                p['v'][i-1] = 0     # i - 1 because of how the velocity is calculated (otherwise it does not get rid of the correct v)
    #                # Need to get rid of the half time glitches THIS WILL WORK ONLY IF THE GAME HAS NO SUPPLEMENTARY TIME
    #                if p['Frames'][i] in range(periods[0][1] - 5, periods[0][1] + 5): # Last 5 frames and first 5 of the half time shouldn't count
    #                    p['a'][i] = 0       # artificially set the accel and the vel to 0, because it's not a glitch
    #                    p['v'][i] = 0
    #                    # append these i's to change the a and vs later
    #                    HalfTmFrames.append(i)
    #                    
                        
                        
    #                else:
    #                    GlitchFrames.append(p['Frames'][i])      # We have all the glitch frames in one array
            
            # For loop to linearly interpolate the glitch frames
    #        for i in GlitchFrames:
                
    #            p['r'][i-3] = int((p['r'][i-4] + p['r'][i])/2) # This is not real interpolation, but  it should smooth enough
    #            p['r'][i-2] = int((p['r'][i-3] + p['r'][i])/2)
    #            p['r'][i-1] = int((p['r'][i-2] + p['r'][i])/2)
    #        # Recalculate the v and a with the new positions
    #        p['v'] = p['r'][1:] - p['r'][:-1]
    #        p['a'] = p['v'][1:] - p['v'][:-1]
    
            for i in range(periods[0][1] - 5, periods[0][1] + 5):           
                if p['a'][i]**2 > threshold:
                    p['a'][i] = 0       # artificially set the accel and the vel to 0, because it's not a glitch
                    p['v'][i-1] = 0     # i - 1 because of how the velocity is calculated (otherwise it does not get rid of the correct v)
            
            if np.isnan(p['r'][0]):
                isnan = ~np.isnan(p['a'])
                TempR = p['r'][isnan]
                TempA = p['a'][isnan]
                TempV = p['v'][isnan] 
                TempR = scipy.ndimage.uniform_filter1d(TempR, 15)
                TempV = scipy.ndimage.uniform_filter1d(TempV, 15)
                TempA = scipy.ndimage.uniform_filter1d(TempA, 15)
                
                Count= 0
                tempCount = 0
                
                for item in isnan:
                    if item == True:
                        p['r'][Count]= TempR[tempCount]
                        p['a'][Count] = TempA[tempCount]
                        p['v'][Count] = TempV[tempCount]
                        tempCount += 1
                    Count += 1
                
                p['r'] = p['r'][::15]
                p['v'] = p['v'][::15]
                p['a'] = p['a'][::15]
                posCol = Column(name = col, data = p['r'])
                vCol = Column(name = 'v'+col, data = p['v'])
                aCol = Column(name = 'a'+col, data =p['a'])
                NewTable.add_column(posCol)
                NewTable.add_column(vCol)
                NewTable.add_column(aCol)
               
                
            else:
                
                r_smooth = scipy.ndimage.uniform_filter1d(p['r'], 15)
                v_smooth = scipy.ndimage.uniform_filter1d(p['v'], 15)
                a_smooth = scipy.ndimage.uniform_filter1d(p['a'], 15)
                r_smooth = r_smooth[::15]
                v_smooth = v_smooth[::15]
                a_smooth = a_smooth[::15]

                #frames = np.arange(v_smooth.size)*15
                posCol = Column(name = col, data = r_smooth)
                vCol = Column(name = 'v'+col, data = v_smooth)
                aCol = Column(name = 'a'+col, data =a_smooth)
                NewTable.add_column(posCol)
                NewTable.add_column(vCol)
                NewTable.add_column(aCol)
#            
#            if switch:
#                
#                    # Take away all nan values for histogram
#                
#                
#                p['r'] = p['r'][~np.isnan(p['r'])]
#                      # Make the r v and a arrays the same length
#                p['a'] = p['a'][~np.isnan(p['a'])]
#                p['v'] = p['v'][~np.isnan(p['v'])] 
#                  # Same for velocity
#    #       
#                plt.figure()
#                plt.plot(p['r'])
#                plt.figure()
#                plt.plot(p['v'])
#                plt.figure()
#                plt.plot(p['a'])
#                plt.figure()
#                plt.hist(p['a'], bins = 80)
#                r_smooth = scipy.ndimage.uniform_filter1d(p['r'], 15)
#                v_smooth = scipy.ndimage.uniform_filter1d(p['v'], 15)
#                a_smooth = scipy.ndimage.uniform_filter1d(p['a'], 15)
#    #            plt.figure()
#    #            plt.plot(r_smooth)
#                r_smooth = r_smooth[::15]
#                v_smooth = v_smooth[::15]
#                a_smooth = a_smooth[::15]
#                p['a'] = p['a'][::15]
#                plt.figure()
#                plt.plot(a_smooth)
#                plt.figure()
#                plt.plot(p['a'])
#                plt.figure()
#                plt.hist(a_smooth, bins = 41)
#            switch = False
    
    #NewTable.write('SmoothedTable.fits', overwrite = True)
    
    #Now use similar algorithm as above to smooth the ball data. 
    count =0
    b = {}
    #ballSmooth = Table([frames], names = ['Frames',], meta={'name': 'Smoothed Player Table'})
    
    for col in ball.columns: #loop thru columns of ball data
        #Ball data: frames, x, y, z, 
        b['frames'] = T['Frames']
       # print(col)
    
        if count == 1 or count == 2 or count ==3: #x y or z
            b['r'] = ball[col]
            v = b['r'][1:] - b['r'][:-1]    # velocity
            a = v[1:] - v[:-1]              # Acceleration
            b['r'] = b['r'][2:]              
            b['v'] = v[1:]                  # Add to the player dictionary
            b['a'] = a
            
            for i in range(periods[0][1] - 5, periods[0][1] + 5):           
                if b['a'][i]**2 > threshold:
                    b['a'][i] = 0       # artificially set the accel and the vel to 0, because it's not a glitch
                    b['v'][i-1] = 0     # i - 1 because of how the velocity is calculated (otherwise it does not get rid of the correct v)
                    
#            plt.figure()
#            plt.plot(b['r'])
#            plt.figure()
#            plt.plot(b['v'])
#            plt.figure()
#            plt.plot(b['a'])
#            plt.figure()
#            plt.hist(b['a'], bins = 40)
           
            TempR = scipy.ndimage.uniform_filter1d(b['r'], 15)
            TempV = scipy.ndimage.uniform_filter1d(b['v'], 15)
            TempA = scipy.ndimage.uniform_filter1d(b['a'], 15)
            
            b['r'] = TempR[::15]
            b['v'] = TempV[::15]
            b['a'] = TempA[::15]
            posCol = Column(name = col, data = b['r'])
            vCol = Column(name = 'v'+col, data = b['v'])
            aCol = Column(name = 'a'+col, data =b['a'])
            ballSmooth.add_column(posCol)
            ballSmooth.add_column(vCol)
            ballSmooth.add_column(aCol)
#            print(count)
#            plt.figure()
#            plt.plot([1,2,3],[-1,3,4])
#            plt.figure()
#            plt.plot(b['r'])
#            plt.figure()
#            plt.plot(b['v'])
#            plt.figure()
#            plt.plot(b['a'])
#            plt.figure()
#            plt.hist(b['a'], bins = 40)
    
        elif count == 4:
            print('hi')
        elif count == 5:
            print('hey')
            
        count += 1
    
    
    return NewTable, ballSmooth    

