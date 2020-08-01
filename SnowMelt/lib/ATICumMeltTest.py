# from __future__ import with_statement
from datetime import datetime
from collections import defaultdict
from __builtin__ import max

from copy import deepcopy
from hec.io          import TimeSeriesContainer
from hec.io         import PairedDataContainer
from hec.script import Plot, AxisMarker
from hec.heclib.dss import HecDss
from hec.dssgui import ListSelection
from hec.heclib.util import HecTime
from OrderedDict27 import OrderedDict


'''
Created on Aug 31, 2017
Updated on Jul 16, 2019

@author: q0hecmbm

Tested using DSSVue from CWMS 3.1.1

Assumptions:
C-parts required = SWE, PRECIP-INC, TEMPERATURE-AIR-AVG. 
E-Part = 1DAY.  !For all required data, daily data is required!:  SWE, PRECIP-INC, TEMPERATURE-AIR-AVG.
Daily data at time = 24:00.
Melt-Cum not Calculated at 32 Degrees, and only at temps greater than 32.
Melt-Cum calculated before SWE max occurs for any given Water Year ---> This may be toggled by switching off the comment: #     if p == 0 and a > 0 and (swePrevious - s)>0 and maxSWEReached is True: # and commenting out the one line below.
No Missing Data. (The script has no checks for these kinds of errors and results may be misleading)
'''

# User Specified Start and End Dates for WY Melt Period Where Melt-ATI Paired Data will be computed
# Stored in FPart = WYxxxx-Start:EndDate

pdStart = '01APR'
pdEnd = '30JUN'



print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin DSS Data Retrieval'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

mainWindow = ListSelection.getMainWindow()
dssFileName = mainWindow.getDSSFilename()
print "dssfile:", dssFileName
dssFile = HecDss.open(dssFileName)

# #Get A and B-parts that have C-parts of PRECIP-INC, SWE, TEMPERATURE-AIR-AVG
bp = []
bs = []
bt = []
Ap = []
As = []
At = []
splitter = []
 
p = dssFile.getCatalogedPathnames("/*/*/PRECIP-INC/*/*/*/")
s = dssFile.getCatalogedPathnames("/*/*/SWE/*/*/*/")
t = dssFile.getCatalogedPathnames("/*/*/TEMPERATURE-AIR-AVG/*/*/*/")
 
for bees in p:
    splitter = bees.split('/')
    bp.append(splitter[2])
 
 
splitter = []
 
for bees in s:
    splitter = bees.split('/')
    bs.append(splitter[2])
 
splitter = []
 
for bees in t:
    splitter = bees.split('/')
    bt.append(splitter[2])
 
#print '\nbp:', type(bp)
 
bp = list(set(bp))
bs = list(set(bs))
bt = list(set(bt))
 
 
c1 = set(bp).intersection(bs)
bList = c1.intersection(bt)
wsList = c1.intersection(At)
 
print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '# B-Parts that have all the required data (Precip, SWE, & Temp)  =',bList
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
 
locDict={}
for b in bList:
    ws = dssFile.getCatalogedPathnames("/*/"+b+"/*/*/*/*/")
    for bee in ws:
        splitter = bee.split('/')
        locDict[b] = splitter[1]
print '\n Aparts for each B-part:', locDict

swePaths = []
tempPaths = []
precipPaths = []
#Get Data for bList for SWE, Precip, and Temp
for b in bList:
    swePaths.append(dssFile.getCatalogedPathnames("/*/"+b+"/SWE/*/*/*/"))
for b in bList:
    precipPaths.append(dssFile.getCatalogedPathnames("/*/"+b+"/PRECIP-INC/*/*/*/"))
for b in bList:
    tempPaths.append(dssFile.getCatalogedPathnames("/*/"+b+"/TEMPERATURE-AIR-AVG/*/*/*/"))
print '\nswePaths[0]: ', swePaths[0]

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Process all SWE Data to sList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'


swePD = []
for p in swePaths:
    str(p).split(",")
    swePD.append(p[0])
print '\nswePD: ', swePD

sP =[]
for p in swePD:
    x = str(p).split("/")
    sP.append('/'+x[1]+'/'+x[2]+'/'+x[3]+'//'+x[5]+'/'+x[6]+'/')
#print '\nsP: ', len(sP)

sweData = []
for p in sP:
    s = dssFile.get(p, 1)
    sweData.append(s.values)
#sweData = list(set(sweData))
#print '\nsweData: ', len(sweData[0])

sD = []
for p in sweData:
    sD.append( str( p.tolist() )   )
#print 'sD:', sD[0]

sList = []
for num in (sweData):
    h = []
    for i, v  in enumerate(num):
        h.append(round(num[i],2)  )
    sList.append(h)
# print '\nsList:', sList

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Process all SWE Data to sList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Process all Temp Data to tList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

tPD = []
for p in tempPaths:
    str(p).split(",")
    tPD.append(p[0])
#'\ntPD: ', tPD

tP =[]
for p in tPD:
    x = str(p).split("/")
    tP.append('/'+x[1]+'/'+x[2]+'/'+x[3]+'//'+x[5]+'/'+x[6]+'/')
#print '\ntP: ', tP

tData = []
for p in tP:
    t = dssFile.get(p, 1)
    tData.append(t.values)
#tData = list(set(tData))
#print '\ntData: ', len(tData[0])

tD = []
for p in tData:
    tD.append( str( p.tolist() )   )
#print 'tD:', tD[0]

tList = []
for num in (tData):
    h = []
    for i, v  in enumerate(num):
        h.append(round(num[i],2)  )
    tList.append(h)
#print '\ntList:', tList

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Process all Temp Data to tList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'


print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Process all Precip Data to pList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

#print 'precipPaths:', precipPaths
 
pPD = []
for p in precipPaths:
    str(p).split(",")
    pPD.append(p[0])
#print '\npPD: ', pPD

pP =[]
for p in pPD:
    x = str(p).split("/")
    pP.append('/'+x[1]+'/'+x[2]+'/'+x[3]+'//'+x[5]+'/'+x[6]+'/')
#print '\npP: ', pP


pData = []
for p in pP:
    x = dssFile.get(p, 1)
    pData.append(x.values)
#pData = list( set(pData) )
#print '\npData: ', len(pData[0])

pD = []
for p in pData:
    pD.append( str( p.tolist() )   )
#print 'pD:', pD[0]

pList = []
for num in (pData):
    h = []
    for i, v  in enumerate(num):
        h.append(round(num[i],2)  )
    pList.append(h)
#print '\npList:', pList

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Process all Precip Data to pList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'


print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Process Dates to tList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '\nsP: ', sP
sT = []
for p in sP:
    s = dssFile.get(p, 1)
    sT.append(s.times)
# print 'sT:', sT

timesListHec = []
t = HecTime()
dList=[]
for p in sT:
#     print '\np: ', p
    iList =[]
    for i in p:
#         print '\ni: ', i
        t.set(i)
#       h = t.dateAndTime(4)
        h = t.date(4)
        iList.append( deepcopy (h) )
    dList.append( iList )
print '\ndList: ', dList


print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Process Dates to tList'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

#for outerlist in zip(sweData, tData, pData):
#   for innerlist in outerlist:
#       print 'length of each list of Zipped Values: ', len(innerlist)
#
#for l in sweData:
#   print 'length of each list of Zipped Values: ', len(l)      



print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End DSS Data Retrieval'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'


print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Calculations'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

mList = []
aList = []
print len(bList), len(sList), len(pList), len(tList), len(dList)
for b, dates, precip, swe, temp in zip(bList, dList, pList, sList, tList):
    print b, len(dates), len(swe), len(precip), len(temp)
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
#   print sorted(zipDict)

    for key,value in zipDict.iteritems():
        if key[0:5] != "30Sep":
            #Append to Wy[i]DatesList
            wyDict[y].append(value)
            
        else:
            y+=1
#   print '\nwyDict:', wyDict
    print'Water Years =', y+1 
    maxWYSWE = []       
    for k, v in sorted(wyDict.items()): 
        #print k, max(v,key=lambda item:item[1])
        maxWYSWE.append(max(v,key=lambda item:item[1]))
        
#   print 'maxWYSWE:', maxWYSWE
    
    maxDatesStr = [n[0] for n in maxWYSWE]
    print maxDatesStr
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
print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Calculations'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Creating ATI and Melt-CUM DSS paths'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
for b, d,a,m in zip(bList, dList, aList, mList):
#locDict contains a-parts with b used as the key
    aPart = locDict[b]
#   print aPart
#   print a
#F-part will be 'CALC'

#ATI-MELT DSS path Created
    tsATI = TimeSeriesContainer()
    tsATI.watershed = aPart
    tsATI.location = b
    tsATI.parameter = 'ATI'
    tsATI.version = 'CALC'
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

    #MELT-CUM DSS path Created
    tsMelt= TimeSeriesContainer()
    tsMelt.watershed = aPart
    tsMelt.location = b
    tsMelt.parameter = 'MELT-CUM'
    tsMelt.version = 'CALC'
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
print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Creating ATI and Melt-CUM DSS paths'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Creating Melt-CUM vs ATI paired data paths for each year. F-part used to identify year.'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

bList = list(bList)
#print bList
wyLists = []
#Check if first date is before Sep30 to get a partial Water Year
for dates  in zip(dList):   
    for d in dates:
        wyList = []
        yb = d[0]
        dayMonthBeginning = yb[0:5]     
        print '\nyb:', yb
        ye = d[-1]
        dayMonthEnd = ye[0:5]
        wyb = yb[5:9]
        print '\nwyb:',wyb
        wyb = int(wyb)
        wye = ye[5:9]
        print '\nwye:', wye
        wye = int(wye)
        dObjb = datetime.strptime(dayMonthBeginning, '%d%b').date()
        dObje = datetime.strptime(dayMonthEnd, '%d%b').date()
        EoY = datetime.strptime('30Sep', '%d%b').date()
        if dObjb >= EoY:
            wyb +=1
        if dObje >= EoY:
            wye +=1 
        r = wye - wyb + 1
        for i in range(r):
            wy = wyb+i
            wyList.append(wy)
    wyLists.append(wyList)  
print wyLists

#get max index from wyLists to use in pdcDict key loop
maxWyIndexList=max(wyLists,key=len)
print '\nmaxWyIndexList=', maxWyIndexList

#print '\npdcDict:', pdcDict

n=0
beeList =[]
aaaList = []

for dates in dList:
    bee = []
    aaa = []
#   print len(dates)
    for d in dates:
        b = bList[n]
        aPart = locDict[b]
        bee.append(b)
        aaa.append(aPart)
#   print '\nbees:', len(aaa)
    beeList.append(bee)
    aaaList.append(aaa)
    n+=1

#print beeList
pdcDict = defaultdict(list)
#print '\nwyL:', wyLists[0]

            
for aParts, bParts, dates, melt, ati in zip(aaaList, beeList, dList, mList, aList):
    i=0
    #   print '\n', len(aParts), len(bParts), len(dates), len(swe), len(ati)
    pzip = zip( aParts, bParts, dates,melt, ati)
    pDict = OrderedDict(zip(dates, pzip))
    for key,value in pDict.iteritems():
        k = key[5:9]
        if key[0:5] != "30Sep" :
#           print wyL[i]
            try:
#               pdcDict[maxWyIndexList[i]].append(value)
                pdcDict[k].append(value)
#               pdcDict[wyLists[0][i]].append(value)
            except:
#               i+=1
                continue
#       else:
#           i+=1


#print '\npdcDict:', sorted(pdcDict)
#print '\npdcDict:', sorted(pdcDict.values())

# create Paired Data Lists: aL = ati list and mL = melt-cum list.
# aL and mL are the RAW data in the paired data records with F-part = YYYY-RAW

# Creates aL3 and mL3 limited to pdStart and pdEnd to be used by pdc3
# Checks pdStart and pdEnd to see if before or after 30Sep (EoY) to give appropriate Year based on pdcDict key to pdStartDate and pdEndDate datetime objects.

pdStartDate =  datetime.strptime(pdStart, '%d%b').date()
pdEndDate =  datetime.strptime(pdEnd, '%d%b').date()

for b in bList:
    aPart = locDict[b]
    i=0
    for key, value in sorted(pdcDict.iteritems()):
#       print key, value
#       print key, int(key)+1
        aL = []
        mL = []
        aL3 = []
        mL3 = []
        if pdStartDate <= EoY:
            pdStartDate = pdStartDate.replace(year=int(key)+1)
        else:
            pdStartDate = pdStartDate.replace(year=int(key))
        if pdEndDate <= EoY:
            pdEndDate = pdEndDate.replace(year=(int(key)+1))
        else:
            pdEndDate = pdEndDate.replace(year=int(key))
        print '\npdStartDate: ', pdStartDate, ' pdEndDate: ', pdEndDate
        for vee in value:
            veeDateStr = vee[2][0:9]
            veeDate = datetime.strptime(veeDateStr, '%d%b%Y').date()
            if vee[1] == b:
                aL.append(vee[4])
                mL.append(vee[3])
            if vee[1] == b and veeDate >= pdStartDate and veeDate <= pdEndDate:
                aL3.append(vee[4])
                mL3.append(vee[3])
        print '\nlen(aL & mL):',b, len(aL), len(mL)
        print 'len(aL3 & mL3):',b, len(aL3), len(mL3)
#       print aL
#       print mL


# This portion of the code needs to be updated to:

# In the Future, we will add paired data for multiple storms identified on the F-part as: YYYY-#, where # equals the event order. 
# I.E.: A WY with 3 events would have Paired Data records YYYY-1, YYYY-2, and YYYY-3. In addtion to YYYY-Raw and YYYY-Max, where YYYY-Max would be a duplicate of one of the max of the three events.
        if  len(mL) == 0:
            continue
        else:
            amTup = zip(aL,mL)
            ac=[]
            mc=[]
            ac.append(aL[0])
            mc.append(mL[0])
            
##The following code is now an obsolete Method.###
# Corrected Paired Data set to ac and mc. Data is being corrected to ensure values can only increase and never decrease, this eliminates any possibility of a looped rating.
#           for k,v in enumerate(amTup):    
#               try:
#                   maxx = max(aL[0:k])                 
#                   if aL[k] > aL[k-1] and aL[k] >= maxx:
#                       ac.append(aL[k])
#                       mc.append(mL[k])
#               except:
#                   continue
##################################


    

# Corrected Paired Data to ensure that only Max Event is used for each WY. 

        maxAti = max(aL)
        maxMelt = max(mL)
        #get index of max
        #iterate backwards til no longer descending and append lists
        #reverse order
        index_maxAti = max(xrange(len(aL)), key=aL.__getitem__)
        index_maxMelt = max(xrange(len(mL)), key=mL.__getitem__)
        print 'Max ATI =', maxAti, 'at Index =', index_maxAti
        print 'Max Melt =', maxMelt, 'at Index =', index_maxMelt
        
        print 'len(ac) & mc:', len(ac), len(mc)
        try:
            pdc = PairedDataContainer()
            pdc.watershed = aPart
            pdc.location = b
#           pdc.version =str( wyLists[0][i] )
#           pdc.version =str(maxWyIndexList[i])
            pdc.version =str(key)
            pdc.fullName =  '/%s/%s/%s///%s/' % \
                (aPart, b, 'ATI-MELT',key)
#               (aPart, b, 'ATI-MELT',maxWyIndexList[i])
            print pdc.fullName
            pdc.xOrdinates = ac
            pdc.yOrdinates = [mc]
            pdc.numberCurves = 1
            pdc.numberOrdinates = len(ac)
            pdc.labelsUsed = False
            pdc.xunits = 'DEGF-DAY'
            pdc.yunits = 'IN'
            pdc.xtype = "INST-VAL"
            pdc.ytype = "INST-VAL"
            pdc.xparameter = 'ATI'
            pdc.yparameter = 'MELT'
            pdc.date = value[0][2]
            dssFile.put(pdc)
#           i+=1
        except:
#           i+=1
            continue
            
#Raw uncorrected data written for each WY using f-part = YYYY-RAW
        try:
            pdc2 = PairedDataContainer()
            pdc2.watershed = aPart
            pdc2.location = b
#           pdc.version =str( wyLists[0][i] )
#           pdc.version =str(maxWyIndexList[i])
            pdc2.version =str(key) + '-RAW'
            pdc2.fullName =  '/%s/%s/%s///%s/' % \
                (aPart, b, 'ATI-MELT',str(key) + '-RAW')
#               (aPart, b, 'ATI-MELT',maxWyIndexList[i])
            print pdc2.fullName
            pdc2.xOrdinates = aL
            pdc2.yOrdinates = [mL]
            pdc2.numberCurves = 1
            pdc2.numberOrdinates = len(aL)
            pdc2.labelsUsed = False
            pdc2.xunits = 'DEGF-DAY'
            pdc2.yunits = 'IN'
            pdc2.xtype = "INST-VAL"
            pdc2.ytype = "INST-VAL"
            pdc2.xparameter = 'ATI'
            pdc2.yparameter = 'MELT'
            pdc2.date = value[0][2]
            dssFile.put(pdc2)
#           i+=1
        except:
#           i+=1
            continue

#Raw uncorrected data from pdStart date to pdEnd date written for each WY using f-part = YYYY-StartDate:EndDate
        
        try:
            pdc3 = PairedDataContainer()
            pdc3.watershed = aPart
            pdc3.location = b
#           pdc.version =str( wyLists[0][i] )
#           pdc.version =str(maxWyIndexList[i])
            pdc3.version =str(key) + '-' + pdStart + ':' + pdEnd
            pdc3.fullName =  '/%s/%s/%s///%s/' % \
                (aPart, b, 'ATI-MELT',str(key) + '-' + pdStart + ':' + pdEnd)
#               (aPart, b, 'ATI-MELT',maxWyIndexList[i])
            print pdc3.fullName
            pdc3.xOrdinates = aL3
            pdc3.yOrdinates = [mL3]
            pdc3.numberCurves = 1
            pdc3.numberOrdinates = len(aL3)
            pdc3.labelsUsed = False
            pdc3.xunits = 'DEGF-DAY'
            pdc3.yunits = 'IN'
            pdc3.xtype = "INST-VAL"
            pdc3.ytype = "INST-VAL"
            pdc3.xparameter = 'ATI'
            pdc3.yparameter = 'MELT'
            pdc3.date = value[0][2]
            dssFile.put(pdc3)
#           i+=1
        except:
#           i+=1
            continue

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Creating SWE vs ATI paired data paths for each year. F-part used to identify year.'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Plotting SWE, ATI, Precip, Temp paths for each location.'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

##3 Viewports
##Top: Temp, Melt- 32degree Marker Line
##Middle: Precip (hanging), SWE
##Bottom: ATI
#st = dList[0][0]
#start = st.strip()
#print start
#et = dList[0][-1]
#end = et.strip()
#startTime = HecTime(start[0:9])
#
#endTime = HecTime(end[0:9])
#dssFile.setTimeWindow(str(startTime), str(endTime))
#print dssFile.getStartTime()
for b in bList:
    aPart = locDict[b]
    
    sp = "/" + aPart +"/"+ b +"/SWE/*/1DAY/SNOTEL/"
    sd = dssFile.get(sp,1)

    tp = "/" + aPart +"/"+ b +"/TEMPERATURE-AIR-AVG/*/1DAY/SNOTEL/"
    td = dssFile.get(tp,1)

    pp = "/" + aPart +"/"+ b +"/PRECIP-INC/*/1DAY/SNOTEL/"
    pd = dssFile.get(pp,1)

    ap = "/" + aPart +"/"+ b +"/ATI/*/1DAY/CALC/"
    ad = dssFile.get(ap,1)

    mp = "/" + aPart +"/"+ b +"/MELT-CUM/*/1DAY/CALC/"
    md = dssFile.get(mp,1)
#   print sd,td,pd,ad,md
    
    
    layout = Plot.newPlotLayout()
    
#   thePlot.setPlotTitleVisible(Constants.TRUE)
#   thePlot.setPlotTitleText("Outlet Releases")
    #thePlot.getPlotTitle().setFont("Arial Black")
#   thePlot.getPlotTitle().setFontSize(18)

    
    topView = layout.addViewport()
    midView = layout.addViewport()
    btmView = layout.addViewport()

    

    topView.addCurve("Y1", td)
    topView.addCurve("Y2", md)

    midView.addCurve("Y1", pd)
    midView.addCurve("Y2", sd)

    btmView.addCurve("Y1", ad)
    thePlot = Plot.newPlot(b)
    thePlot.configurePlotLayout(layout)
    thePlot.showPlot()
    view1 = thePlot.getViewport(pd)
    axis = view1.getAxis("Y1")
    axis.setReversed(False)
    
    markerTemp = AxisMarker()
    markerTemp.axis = "Y"
    markerTemp.value = "32"
    view=thePlot.getViewport(td)
    view.addAxisMarker(markerTemp)
print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#Begin Plotting SWE, ATI, Precip, Temp paths for each location.'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
    



dssFile.close()
print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
print '#End Script.################################################################End Script.#####################################################################End Script.#'
print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
