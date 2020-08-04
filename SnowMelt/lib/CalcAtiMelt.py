'''
Created on Nov 22, 2019

@author: q0hecmbm
'''

from hec.heclib.dss         import HecDss
from hec.heclib.util        import HecTime
from hec.dssgui             import ListSelection
from hec.io                 import TimeSeriesContainer
from datetime               import datetime
from OrderedDict27          import OrderedDict
from collections            import defaultdict
from __builtin__            import max
from copy                   import deepcopy
import Locations

dssFile = Locations.dssFile
# from Locations              import getPaths, getList
# import UI

# mainWindow = ListSelection.getMainWindow()
# dssFileName = mainWindow.getDSSFilename()
# print "dssfile:", dssFileName
# dssFile = HecDss.open(dssFileName)
# 
# locDict, bList = getPaths(dssFile)
# locDict = Locations.locDict

# locList = getList(locDict)

# get SWE, Precip, and Temp, paths from UI
# UIgetter = UI.UI()
# swePaths, precipPaths, tempPaths = UIgetter.getPathsList()
#replace duplicate sList, tList, plist, dlist process with a single reusable function.

# def getPathsLists(swePaths, precipPaths, tempPaths):
#     global swePaths_calc, precipPaths_calc, tempPaths_calc
#     swePaths_calc, precipPaths_calc, tempPaths_calc = swePaths, precipPaths, tempPaths
# #     print swePaths_calc, precipPaths_calc, tempPaths_calc

def processPathsLists(swePaths, precipPaths, tempPaths):    
    
    # Get a sample list to Blank D-part paths from.
    swePD = []
    precipPD = []
    tempPD = []
    for p, q, r in zip(swePaths, precipPaths, tempPaths):
        str(p).split(",")
        str(q).split(",")
        str(r).split(",")
        print p
        swePD.append    (p[0])
        precipPD.append (q[0])
        tempPD.append   (r[0])
#     print '\nswePD: ', swePD
#     print '\npPD: ', precipPD
#     print '\ntPD: ', tempPD
 
    # Create a List for each location of paths with a Blank D part each Parameter.
    sP = []
    pP = []
    tP = []
    for p, q, r in zip(swePD, precipPD, tempPD):
        x = str(p).split("/")
        sP.append('/'+x[1]+'/'+x[2]+'/'+x[3]+'//'+x[5]+'/'+x[6]+'/')
        
        x = str(q).split("/")
        pP.append('/'+x[1]+'/'+x[2]+'/'+x[3]+'//'+x[5]+'/'+x[6]+'/')
        
        x = str(r).split("/")
        tP.append('/'+x[1]+'/'+x[2]+'/'+x[3]+'//'+x[5]+'/'+x[6]+'/')
#     print '\nsP: ', sP
#     print '\npP: ', pP
#     print '\ntP: ', tP
    
    #Get the data from the list of paths from the DSS File as TimeSeriesContainers. 
    sweData = []
    precipData = []
    tempData = []
    for p, q, r in zip(sP, pP, tP):
        s = dssFile.get(p, 1)
        sweData.append(s.values)
        
        p = dssFile.get(q, 1)
        precipData.append(p.values)
        
        t = dssFile.get(r, 1)
        tempData.append(t.values)
#         sweData = list(set(sweData))
#         precipData = list(set(precipData))
#         tempData = list(set(tempData))
#     print '\nsweData: ', len(sweData[0])
#     print '\nprecipData: ', len(precipData[0])
#     print '\ntempData: ', len(tempData[0])
     
    # Create strings from the list of TimeseriesContainers. 
    sD = []
    pD = []
    tD = []
    for p, q, r in zip(sweData, precipData, tempData):
        sD.append( str( p.tolist() )   )
        pD.append( str( q.tolist() )   )
        tD.append( str( r.tolist() )   )
    #print 'sD:', sD[0]
     
    # Take each list of values and append to a single list to make it easier to divide into Water Years instead of DSS record blocks. 
    # Also, round to two decimal places.
    sList = []
    pList = []
    tList = []
    for num in (sweData):
#         print '\nnum in sweData: ', num
        h = []
        for i, v  in enumerate(num):
            h.append(round(num[i],2)  )
        sList.append(h)
    
    for num in (precipData):
        h = []
        for i, v  in enumerate(num):
            h.append(round(num[i],2)  )
        pList.append(h)
        
    for num in (tempData):
        h = []
        for i, v  in enumerate(num):
            h.append(round(num[i],2)  )
        tList.append(h)
        
#     print '\nsList:', len(sList)
#     print '\npList:', len(pList)
#     print '\ntList:', len(tList)
    
    # Use just sP as a return for use in dList function (processPathsDatesList) to create Dates list since all lists should have equal length.
    SwePathsWithNoDParts = sP
    return SwePathsWithNoDParts, sList, pList, tList

  
def processPathsDatesList(sP):
    sT = []
#     print '\nsP: ', sP
    for p in sP:
        s = dssFile.get(p, 1)
        sT.append(s.times)
#     print '\nsT: ', sT
     
#     timesListHec = []
    t = HecTime()
    dList=[]
    for p in sT:
        iList =[]
        for i in p:
            t.set(i)
            h = t.date(4)
            iList.append( deepcopy (h) )
        dList.append( iList )
#     print '\ndList: ', dList
    return dList
    
 
# #for outerlist in zip(sweData, tData, pData):
# #   for innerlist in outerlist:
# #       print 'length of each list of Zipped Values: ', len(innerlist)
# #
# #for l in sweData:
# #   print 'length of each list of Zipped Values: ', len(l)      


def calcATIMelt(selectedList, sList, pList, tList, dList):      
    mList = []
    aList = []
#     print len(selectedList), len(sList), len(pList), len(tList), len(dList)
    for b, dates, precip, swe, temp in zip(selectedList, dList, pList, sList, tList):
#         print b, len(dates), len(swe), len(precip), len(temp)
        meltCum = []
        ati = []
        m = 0
        a = 0
        mc = 0
        s = 0
        swePrevious = 0
         
        #find each max SWE per water year
        # WaterYear = Oct 01 to Sep 30
        y = 0
        wy = []
        wyDict = defaultdict(list)
        zipVals = zip(dates, swe)
          
        zipDict = OrderedDict(zip(dates, zipVals))
#         print '\nsorted(zipDict): ', sorted(zipDict)
      
        for key,value in zipDict.iteritems():
            if key[0:5] != "30Sep":
                #Append to Wy[i]DatesList
                wyDict[y].append(value)
                  
            else:
                y+=1
#         print '\nwyDict:', wyDict
#         print'Water Years =', y+1 
        maxWYSWE = []       
        for k, v in sorted(wyDict.items()): 
            #print k, max(v,key=lambda item:item[1])
            maxWYSWE.append(max(v,key=lambda item:item[1]))
              
    #   print 'maxWYSWE:', maxWYSWE
          
        maxDatesStr = [n[0] for n in maxWYSWE]
#         print maxDatesStr
        maxDates = []
        for date in maxDatesStr:
            dateObj = datetime.strptime(date, '%d%b%Y').date()
            maxDates.append(dateObj)
    #   print maxDates
          
        dateObjects = []
        for d in dates:
            dateObj = datetime.strptime(d, '%d%b%Y').date()
            dateObjects.append(dateObj)
          
        maxSWE = [n[1] for n in maxWYSWE]
        e = 0
        maxSWEReached = False
      
    #   print zip(dates, precip, swe, temp)
        for d,o,p,s,t in zip(dates, dateObjects, precip, swe, temp):
    #       m = 0
    #       a = 0
    #       mc = 0
    #       swePrevious = 0
    #       s = 0
    #       maxSWEReached = False
            if d[0:5] == '30Sep':
                m = 0
                a = 0
                mc = 0
                swePrevious = 0
                s = 0
                maxSWEReached = False
                e+=1
                try:
                    print 'End of Water Year Reached, maxSWE updated to:', maxDates[e], maxSWE[e]
                except:
                    continue
                
            if (s > 0 or swePrevious > 0) and (t > 32):
                a += (int(t)-32)
                a = max(0, a)
    #           print b,d,a
    #           if a>0:
    #               print b, d, a
            else:
                a = 0 
            ati.append(a)
      
    #       print '\no:', o, 'e:', e
    #       print '\nmaxDates:', maxDates
              
            try:
                if o>=maxDates[e]:
                    maxSWEReached = True
            except:
                    continue
                          
        #     if p == 0 and a > 0 and (swePrevious - s)>0 and maxSWEReached is True:  
            if p == 0 and a > 0 and (swePrevious - s)>0: 
                m = (swePrevious - s)
                    
            else:
                m = 0   
                
            mc += m     
            meltCum.append(mc)  
      
    #       print b, d, 'm=', mc, 'a=', a, 's=', s, 'p=', p, 't=', t
    #       if m>0:
    #           print b, d, 'm=', mc, 'a=', a, 't=', t, 'SWEmax =', maxDates[e]
    #       print b, d, 'm=', mc
            swePrevious = s
        #print dates
        #print ati
    #   print b, meltCum
        mList.append(meltCum)
        aList.append(ati)
    return aList, mList

def writeAtiMelt(selectedList, dList, aList, mList):
# print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
# print '#Begin Creating ATI and Melt-CUM DSS paths'
# print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
    for ab, d,a,m in zip(selectedList, dList, aList, mList):
    
        aPart = ab.split("/")[1]
        b = ab.split("/")[2]
#         print 'aPart: ', aPart
        
        # ATI-MELT DSS path Created
        tsATI = TimeSeriesContainer()
        tsATI.watershed = aPart
        tsATI.location = b
        tsATI.parameter = 'ATI'
        # F-part will be 'CALC'
        tsATI.version = 'CALC'
        # Interval is hard coded as 1Day = 1440 minutes.
        tsATI.interval = 1440
        tsATI.fullName = '/%s/%s/%s//1DAY/%s/' % \
            (aPart, b, 'ATI', 'CALC')
     
        tsATI.values = a
        times = []
        hecTime = HecTime()
        for i, v in enumerate(d):
            hecTime.set(d[i])
            times.append(hecTime.value())
        tsATI.times = times
        tsATI.startTime = times[0]
        tsATI.endTime = times[-1]
        tsATI.numberValues = len(a)
        tsATI.units = 'DEGF-DAY'
        tsATI.type = 'INST-VAL'
        dssFile.put(tsATI)
     
        # MELT-CUM DSS path Created
        tsMelt= TimeSeriesContainer()
        tsMelt.watershed = aPart
        tsMelt.location = b
        tsMelt.parameter = 'MELT-CUM'
        tsMelt.version = 'CALC'
        # Interval and FullName are hard coded as 1Day = 1440 minutes.
        tsMelt.interval = 1440
        tsMelt.fullName = '/%s/%s/%s//1DAY/%s/' % \
            (aPart, b, 'MELT-CUM', 'CALC')
     
        tsMelt.values = m
        tsMelt.times = times
        tsMelt.startTime = times[0]
        tsMelt.endTime = times[-1]
        tsMelt.numberValues = len(m)
        tsMelt.units = 'IN'
        tsMelt.type = 'INST-VAL'
        dssFile.put(tsMelt)
# print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
# print '#End Creating ATI and Melt-CUM DSS paths'
# print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
  