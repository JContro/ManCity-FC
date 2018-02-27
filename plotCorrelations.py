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

def createGraphs( Tbl, x, data, colData, pp):
    c =0
    titles =[]

    if x == True:
        colData.append('X')
    else:
        colData.append('Y')
        
    titles.append(colData[2] + ' Coordinate vs Frames for player ' + colData[1]+ ' for the ' + colData[0] + 'team')
    titles.append('Autocorrelation of the ' + colData[2] + ' coordinate for player ' + colData[1]+ ' for the ' + colData[0] + 'team')
    titles.append('Velocity in the ' + colData[2] + ' direction for player ' + colData[1]+ ' for the ' + colData[0] + 'team')
    titles.append('Autocorrelation of the Velocity in the ' + colData[2] + ' direction for player ' + colData[1]+ ' for the ' + colData[0] + 'team')
    titles.append('Accelleration in the ' + colData[2] + ' direction for player ' + colData[1] + ' for the ' + colData[0] + ' team' )
    titles.append('Autocorrelation of the Accelleration in the ' + colData[2] + ' direction for player ' + colData[1]+ ' for the ' + colData[0] + 'team')


    for column in Tbl.columns:
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            frames = data['Frames'][:len(Tbl[column])]
            ax.plot(frames, Tbl[column])
            ax.set_title(titles[c])
            ax.set_xlabel('Frames')
            ax.set_ylabel(colData[2]+' position value')
            
            pp.savefig()
            plt.close(fig)
             
            fig = plt.figure()

            ax2 = fig.add_subplot(1,1,1)
            #get autoCorrelation
            corr= scipy.correlate(Tbl[column][:70000], Tbl[column][:70000], mode = 'same')
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
            
            pp.savefig()
            plt.close(fig)
            #plt.plot()
            fig = plt.figure()
            ax2 = fig.add_subplot(111)
            corr= scipy.correlate(Tbl[column][:70000], Tbl[column][:70000], mode = 'same')
            ax2.plot(corr[int(corr.size/2):]) #symmetric fn - just plot half
            ax2.set_title(titles[c+1] +'first half')
            
            pp.savefig()
            plt.close(fig)
            
            #zoomed in
            fig = plt.figure()
            ax3 = fig.add_subplot(111)
            ax3.plot(corr[int(corr.size/2):]) #symmetric fn - just plot half
            ax3.set_title(titles[c+1] +' First half')
            ax3.set_xlim(0, 1000)
            
            pp.savefig()
            plt.close(fig)
            
            fig = plt.figure()
            ax3 = fig.add_subplot(111)
            ax3.plot(corr[int(corr.size/2):]) #symmetric fn - just plot half
            ax3.set_title(titles[c+1] + ' first half')
            ax3.set_xlim(0, 200)
            
            pp.savefig()
            plt.close(fig)
            #plt.plot()
            c += 2
            
            
    #return fig
    

data = Table.read('tableTest.fits')#read in the data
colCount = 0
cols =[]
smoothed = False
for col in data.columns:#loops thru column names where col == string name of each col
    cols.append(col) #Store column keys to use in next loop 

if smoothed == False:
    pp = PdfPages('XY Correlations NON Smoothed.pdf')

    for col in data.columns:
        if colCount >0 : #misses the frames col and accesses every 3rd -> the position
            #get column
            thisCol = data[col]

            Tbl = Table([thisCol[2:]])
           # Tbl = Table([thisCol])
            v = thisCol[1:] - thisCol[:-1]#xi - x(i-1)
            a = v[1:] - v[:-1] #USE FOR NON SMOOted
            Tbl['v'] = v[1:]
            Tbl['a'] = a
    #        Tbl['a'] = data[cols[colCount+2]]
    #        Tbl['v'] = data[cols[colCount+1]]
            
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
            
            if (colCount - 1)%2 ==0: #x coords
                x = True
                createGraphs(Tbl, x, data, thisData, pp)
            else:
                x = False
                createGraphs(Tbl,x,data, thisData, pp)
            
           
        colCount +=1 
    pp.close()
else:
    pp = PdfPages('XY Correlations Smoothed.pdf')

    for col in data.columns:
        if colCount >0 and (colCount -1)%3 ==0: #misses the frames col and accesses every 3rd -> the position
        #get column
            thisCol = data[col]
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
        
