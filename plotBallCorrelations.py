# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 12:01:44 2017

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 16:56:13 2017

Script to plot position, vel, acc for each player in x and Y, and their autoCorrelations

@author: user
"""
from astropy.table import Table, Column
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import scipy
import numpy as np

def createGraphs( Tbl, coords, data, pp):
    c =0
    titles =[]


    titles.append(coord + ' Coordinate vs Frames for the ball')
    titles.append('Autocorrelation of the ' + coord + ' coordinate for the ball')
    titles.append('Velocity in the ' + coord + ' direction for the ball')
    titles.append('Autocorrelation of the Velocity in the ' + coord + ' direction forthe ball')
    titles.append('Accelleration in the ' + coord + ' direction for the ball' )
    titles.append('Autocorrelation of the Accelleration in the ' + coord + ' direction for the ball')


    for column in Tbl.columns:
            print(c)
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            frames = data['frames'][:len(Tbl[column])]
            ax.plot(frames, Tbl[column])
            ax.set_title(titles[c])
            ax.set_xlabel('Frames')
            ax.set_ylabel(coord+' position value')
            
            pp.savefig()
            plt.close(fig)
             
            fig = plt.figure()

            ax2 = fig.add_subplot(1,1,1)
            #get autoCorrelation
            corr= scipy.correlate(Tbl[column], Tbl[column], mode = 'same')
            ax2.plot(corr[int(corr.size/2):]) #symmetric fn - just plot half
            ax2.set_title(titles[c+1])
            
            pp.savefig()
            plt.close(fig)
            #zoomed in
            fig = plt.figure()
            ax3 = fig.add_subplot(111)
            ax3.plot(corr[int(corr.size/2):]) #symmetric fn - just plot half
            ax3.set_title(titles[c+1])
            ax3.set_xlim(0, 1000)
            
            pp.savefig()
            plt.close(fig)
            
            fig = plt.figure()
            ax3 = fig.add_subplot(111)
            ax3.plot(corr[int(corr.size/2):]) #symmetric fn - just plot half
            ax3.set_title(titles[c+1])
            ax3.set_xlim(0, 200)
            #plt.plot()
            pp.savefig()
            plt.close(fig)
            c +=2
    #return fig
    

data = Table.read('ballTable.fits')#read in the data
colCount = 0
cols =[]
smoothed = False
for col in data.columns:#loops thru column names where col == string name of each col
    cols.append(col) #Store column keys to use in next loop 

if smoothed == False:
    pp = PdfPages('Ball Correlations NON Smoothed.pdf')

    for col in data.columns:
        if colCount >0 and colCount < 4: #misses the frames col and accesses every 2rd -> the position
            #get column
            thisCol = data[col]
            Tbl = Table([thisCol[2:]])
           # Tbl = Table([thisCol])
            v = thisCol[1:] - thisCol[:-1]#xi - x(i-1)
            a = v[1:] - v[:-1] #USE FOR NON SMOOted
            Tbl['v'] = v[1:]
            Tbl['a'] = a
    #        Tbl['a'] = data[cols[colCount+2]]
    #        Tbl['v'] = data[cols[colCount+1]
            
            if colCount ==1: #x coords
                coord = 'X '
                createGraphs(Tbl, coord, data,  pp)
            elif colCount ==2:
                coord = 'Y '
                createGraphs(Tbl,coord,data,  pp)
            elif colCount ==3:
                coord = 'Z'
                createGraphs(Tbl, coord, data, pp)

                
           
        colCount +=1 
    pp.close()
else:
    for col in data.columns:
        if colCount >0 and (colCount -1)%3 ==0: #misses the frames col and accesses every 3rd -> the position
        #get column
            thisCol = data[col]
            pp = PdfPages('XY Correlations NON Smoothed.pdf')

            Tbl = Table([thisCol])
       # Tbl = Table([thisCol])
           # v = thisCol[1:] - thisCol[:-1]#xi - x(i-1)
            #a = v[1:] - v[:-1] #USE FOR NON SMOOted
            #Tbl['v'] = v[1:]
            #Tbl['a'] = a
            Tbl['a'] = data[cols[colCount+2]]
            Tbl['v'] = data[cols[colCount+1]]
        
            i = np.nonzero(np.isnan(Tbl[col]))
            if len(i[0]) != 0 and i[0][0] == 0: #subbed on 
                Tbl = Tbl[i[0][0]:]
            elif(len(i[0]) != 0 and i[0][0] != 0):
                Tbl = Tbl[:i[0][0]]



        
            thisData =[]
            thisName = col.split(':')
            if thisName[1] ==1:
                thisData.append('Home')
            else:
                thisData.append('Away')
            thisData.append(thisName[2]) #array with team + shirt num
            
            if (colCount - 1)%3 ==0 and colCount%2 != 0: #x coords - odd cols
                x = True
                createGraphs(Tbl, x, data, thisData, pp)
            else:
                x = False
                createGraphs(Tbl,x,data, thisData, pp)
        
       
        colCount +=1 
    pp.close()
        
