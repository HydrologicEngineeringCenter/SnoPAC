from hec.io         import PairedDataContainer
from hec.heclib.dss import HecDss
from datetime               import datetime
import Locations

dssFile = HecDss.open(r"C:\jy\SnowMelt\snotel_3v6.dss")

# EoY = datetime.strptime('30Sep', '%d%b').date()

def calcRawPD(aPart, b, key, value, aL, mL):
    pdc = PairedDataContainer()
    pdc.watershed = aPart
    pdc.location = b
    pdc.version =str(key) + '-WY'
    pdc.fullName =  '/%s/%s/%s///%s/' % \
        (aPart, b, 'ATI-MELT',str(key) + '-WY')
    print pdc.fullName
    pdc.xOrdinates = aL
    pdc.yOrdinates = [mL]
    pdc.numberCurves = 1
    pdc.numberOrdinates = len(aL)
    pdc.labelsUsed = False
    pdc.xunits = 'DEGF-DAY'
    pdc.yunits = 'IN'
    pdc.xtype = "INST-VAL"
    pdc.ytype = "INST-VAL"
    pdc.xparameter = 'ATI'
    pdc.yparameter = 'MELT'
    pdc.date = value[0][2]
    dssFile.put(pdc)


def calcSpecifiedDatePD(pdStart, pdEnd, aPart, b, key, value, aL_specifiedDates, mL_specifiedDates):
    pdc = PairedDataContainer()
    pdc.watershed = aPart
    pdc.location = b
    pdc.version =str(key) + '-' + pdStart + ':' + pdEnd + "-UserSpecified"
    pdc.fullName =  '/%s/%s/%s///%s/' % \
        (aPart, b, 'ATI-MELT',str(key) + '-' + pdStart + ':' + pdEnd + "-U")
    print pdc.fullName
    pdc.xOrdinates = aL_specifiedDates
    pdc.yOrdinates = [mL_specifiedDates]
    pdc.numberCurves = 1
    pdc.numberOrdinates = len(aL_specifiedDates)
    pdc.labelsUsed = False
    pdc.xunits = 'DEGF-DAY'
    pdc.yunits = 'IN'
    pdc.xtype = "INST-VAL"
    pdc.ytype = "INST-VAL"
    pdc.xparameter = 'ATI'
    pdc.yparameter = 'MELT'
    pdc.date = value[0][2]
    dssFile.put(pdc)

def calcEventBasedPD(aPart, b, key, value, aL_eventBased, mL_eventBased, eventStart, eventEnd):
    dayStart = eventStart[0:2]
    monthStart = eventStart[2:5]
    dayEnd = eventEnd[0:2]
    monthEnd = eventEnd[2:5]
    pdc = PairedDataContainer()
    pdc.watershed = aPart
    pdc.location = b
    pdc.version =str(key) + '-' + monthStart + dayStart + ':' + monthEnd + dayEnd
    pdc.fullName =  '/%s/%s/%s///%s/' % \
        (aPart, b, 'ATI-MELT',str(key) + '-' + monthStart + dayStart + ':' + monthEnd + dayEnd)
    print pdc.fullName
    pdc.xOrdinates = aL_eventBased
    pdc.yOrdinates = [mL_eventBased]
    pdc.numberCurves = 1
    pdc.numberOrdinates = len(aL_eventBased)
    pdc.labelsUsed = False
    pdc.xunits = 'DEGF-DAY'
    pdc.yunits = 'IN'
    pdc.xtype = "INST-VAL"
    pdc.ytype = "INST-VAL"
    pdc.xparameter = 'ATI'
    pdc.yparameter = 'MELT'
    pdc.date = value[0][2]
    dssFile.put(pdc)
    
def updatePDTable(dssFile, eventsTable, dm_events):
    locationsList, eventsList = Locations.getPairedData(dssFile)
    columns = ("Location", "Event")
    data = []
    dm_events.setRowCount(0)
    for l, e in zip(locationsList, eventsList):
        data.append([l, e])
    dm_events.setDataVector(data, columns)
    eventsTable.repaint()