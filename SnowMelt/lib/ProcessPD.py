from datetime               import datetime
from OrderedDict27          import OrderedDict
from collections            import defaultdict
from hec.io         import PairedDataContainer
from hec.heclib.dss import HecDss
import CalcPD
from javax.swing import JOptionPane

dssFile = HecDss.open(r"C:\jy\SnowMelt\snotel_3v6.dss")
EoY = datetime.strptime('30Sep', '%d%b').date()

def getSpecifiedDates(startTextField, endTextField):
    try:
        pdStart = startTextField.getText()
        pdEnd = endTextField.getText()
        pdStartDate =  datetime.strptime(pdStart, '%d %b %Y').date()
        pdEndDate =  datetime.strptime(pdEnd, '%d %b %Y').date()
    except:
        JOptionPane.showMessageDialog(None, "Unable to Process Specified Dates.", "Optional Dates Error", JOptionPane.WARNING_MESSAGE)
        pdStart = None
        pdEnd = None
    return pdStart, pdEnd



def createWaterYearList(dList):
    wyLists = []
    # Check if first date is before Sep30 to get a partial Water Year.
    for dates in zip(dList):   
        for d in dates:
            wyList = []
#             print '\nd: ', d
            yb = d[0]
            dayMonthBeginning = yb[0:5]     
#             print '\nyb:', yb
            ye = d[-1]
#             print '\nye:', ye
            dayMonthEnd = ye[0:5]
            wyb = yb[5:9]
#             print '\nwyb: ',wyb
            wyb = int(wyb)
            wye = ye[5:9]
    #       print '\nwye:', wye
            wye = int(wye)
            dObjb = datetime.strptime(dayMonthBeginning, '%d%b').date()
            dObje = datetime.strptime(dayMonthEnd, '%d%b').date()
            if dObjb >= EoY:
                wyb +=1
            if dObje >= EoY:
                wye +=1 
            r = wye - wyb + 1
            for i in range(r):
                wy = wyb+i
                wyList.append(wy)
        wyLists.append(wyList)  
    return wyLists

def processPairedData(selectedLocationsList, dList, mList, aList, pdStart, pdEnd):
    
    wyLists = createWaterYearList(dList)
    
    
    #get max index from wyLists to use in pdcDict key loop
    maxWyIndexList=max(wyLists,key=len)
#     print '\nmaxWyIndexList=', maxWyIndexList
    
    #print '\npdcDict:', pdcDict
    
    n=0
    beeList =[]
    aaaList = []
    # Create aList and bList for Paired Data.
    for dates, a_and_b_parts in zip(dList, selectedLocationsList):
        bee = []
        aaa = []
    #   print len(dates)
        for d in dates:
#             print '\nab: ', a_and_b_parts
            aPart = a_and_b_parts.split("/")[1]
            b = a_and_b_parts.split("/")[2]
#             b = bList[n]
#             aPart = locDict[b]
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
    
    for a_and_b_parts in selectedLocationsList:
        aPart = a_and_b_parts.split("/")[1]
        b = a_and_b_parts.split("/")[2]
        
        for key, value in sorted(pdcDict.iteritems()):
    #       print key, value
    #       print key, int(key)+1
            
            # Initialize RAW Lists.
            aL_raw = []
            mL_raw = []
            # Init Specified Dates Lists.
            aL_specifiedDates = []
            mL_specifiedDates = []
           
            # Init Event Based Lists and Variables.
            aL_eventBased = []
            mL_eventBased = []
            eventStartDate = []
            eventEndDate = []
            zeroHit = False
            i = 0
            
            # Checks pdStart and pdEnd to see if before or after 30Sep (EoY) to give appropriate Year based on pdcDict key to pdStartDate and pdEndDate datetime objects.
            if pdStart and pdEnd is not None:
                pdStartDate =  datetime.strptime(pdStart, '%d %b %Y').date()
                pdEndDate =  datetime.strptime(pdEnd, '%d %b %Y').date() 
                daymoStart = pdStart[:-4]
                daymoEnd = pdEnd[:-4]
                daymoStart = daymoStart.replace(" ", "")
                daymoEnd = daymoEnd.replace(" ", "")
                pdStartDate = datetime.strptime(daymoStart, '%d%b').date() 
                pdEndDate =  datetime.strptime(daymoEnd, '%d%b').date()
                print 'pdStartDate', pdStartDate
                print 'EoY', EoY
                if pdStartDate <= EoY:
                    pdStartDate = pdStartDate.replace(year=int(key)+1)
                    print 'pdStartDate <= EoY', pdStartDate
                else:
                    pdStartDate = pdStartDate.replace(year=int(key))
                    print 'pdStartDate > EoY', pdStartDate
                if pdEndDate <= EoY:
                    pdEndDate = pdEndDate.replace(year=(int(key)+1))
                    print 'pdEndDate <= EoY', pdEndDate
                else:
                    pdEndDate = pdEndDate.replace(year=int(key))
                    print 'pdEndDate > EoY', pdEndDate
            
            
#             print '\npdStartDate: ', pdStartDate, ' pdEndDate: ', pdEndDate
            
            for vee in value:
                veeDateStr = vee[2][0:9]
                veeDate = datetime.strptime(veeDateStr, '%d%b%Y').date()
                
                # Raw PD Lists
                if vee[1] == b:
                    aL_raw.append(vee[4])
                    mL_raw.append(vee[3])
                
                # User Specified Dates PD Lists
                # Creates aL3 and mL3 limited to pdStart and pdEnd to be used by pdc3
                
#                 if pdStartDate and pdEndDate is not None:  
# #                     print '\nveeDate', veeDate 
# #                     print vee[1], b
# #                     print vee[1] == b
# #                     print veeDate >= pdStartDate, pdStartDate
# #                     print veeDate <= pdEndDate, pdStartDate
#                     if vee[1] == b and veeDate >= pdStartDate and veeDate <= pdEndDate:
#                         print 'if vee[1] == b and veeDate >= pdStartDate and veeDate <= pdEndDate:'
#                         print 'aL_specifiedDates.append(vee[4])', vee[4]
#                         print 'mL_specifiedDates.append(vee[4])', vee[3]
#                         aL_specifiedDates.append(vee[4])
#                         mL_specifiedDates.append(vee[3])
                
                # Event Based PD Lists.
                if vee[1] == b:
#                     print '\nvee[1]: ', vee[1]
#                     print '\nvee[4] = ATI value = : ', vee[4]
                    
                    # if ATI = 0 and zeroHit = False, create first dataset.
                    # Start a new data set by appending empty lists. 
                    # Add the zero values to the new list and append a new start date.
                    if vee[4] == 0 and zeroHit == False:
#                         print '\nvee[4] == 0 and zeroHit == False'
                        zeroHit = True 
                        aL_eventBased.append([])
#                         print '\n zero was hit, append blank lists and a new startDate', aL_eventBased
                        mL_eventBased.append([])
                        eventStartDate.append([])
#                         print '\neventStartDate: ', eventStartDate
                        aL_eventBased[i].append(vee[4])
                        mL_eventBased[i].append(vee[3])
                        eventStartDate[i] = veeDateStr
                     
                    # If ATI > 0 and zeroHit= True, stay on the current data set and append to the current list index, i.
                    elif vee[4] > 0 and zeroHit == True:
#                         print '\nATI > 0 and zeroHit = True'
#                         print '\ni: ', i
#                         print '\n zeroHit = True, append blank list to aL_eventBased: ', aL_eventBased
                        aL_eventBased[i].append(vee[4])
                        mL_eventBased[i].append(vee[3])
                    # Else zero hit within dataset. set zeroHit = False, add a new event end date value, and increment i for the next data. add data to new dataset.
                    elif vee[4] == 0 and zeroHit == True:
                        zeroHit = False
                        eventEndDate.append([])
                        eventEndDate[i] = veeDateStr
#                       print '\ni incremented, i = ', i 
                        i+=1
                        aL_eventBased.append([])
                        mL_eventBased.append([])
                        eventStartDate.append([])
                        
                        aL_eventBased[i].append(vee[4])
                        mL_eventBased[i].append(vee[3])
                        eventStartDate[i] = veeDateStr

 
                    # non-zero value in dataset.
                    elif vee[4] > 0  and zeroHit == False:
                        zeroHit = True
                        aL_eventBased[i].append(vee[4])
                        mL_eventBased[i].append(vee[3])                         
                else:
                    continue
                                 
            # Pop any Events that are single zero values, or the melt is constant. 
            for aL, mL, start, end in zip(aL_eventBased, mL_eventBased, eventStartDate, eventEndDate):
                    if max(aL) == 0 or max(mL)-min(mL)==0:
                        aL_eventBased.remove(aL)
                        mL_eventBased.remove(mL)
                        eventStartDate.remove(start)
                        eventEndDate.remove(end)
            
            try:
                # Raw uncorrected data written for each entire WY using f-part = YYYY-WY
#                 print '\naL_raw: ', aL_raw
                CalcPD.calcRawPD(aPart, b, key, value, aL_raw, mL_raw)
            except:
                print '\bFailed to write RAW Paired Data for %s/%s.' % (aPart,b)
                continue   
            
            try:
                # Data written into aL and ML lists broken apart every time ATI return to zero. Creates a per event PD with f - part = YYYY-StartDate:EndDate
                for aL, mL, start, end in zip(aL_eventBased, mL_eventBased, eventStartDate, eventEndDate):
                    CalcPD.calcEventBasedPD(aPart, b, key, value, aL, mL, start, end)
            except:
                print '\bFailed to write Event Paired Data for %s/%s.' % (aPart,b)
                continue
            
#             try:
#                 # User Specified Paired Data from pdStart date to pdEnd date written for each WY using f-part = YYYY-StartDate:EndDate-UserSpecified
#                 if pdStartDate and pdEndDate is not None:
#                     daymoStart = datetime.strftime(pdStartDate, '%d%b')
#                     daymoEnd = datetime.strftime(pdEndDate, '%d%b')
#                     print 'daymoStart', daymoStart
#                      
#                     CalcPD.calcSpecifiedDatePD(daymoStart, daymoEnd, aPart, b, key, value, aL_specifiedDates, mL_specifiedDates)
#             except:
#                 print '\bFailed to write Specified Date Paired Data for %s/%s.' % (aPart,b)
#                 continue