from hec.heclib.dss     import HecDss
# from hec.heclib.util    import HecTime
# from hec.io             import TimeSeriesContainer
# from datetime           import datetime
# from OrderedDict27      import OrderedDict
# from collections        import defaultdict
# from __builtin__        import max
# from copy               import deepcopy

global dssFile 
dssFile = HecDss.open(r"C:\jy\SnowMelt\snotel_3v6.dss")
# class Locations():
def getPaths(dssFile):
# Get A and B-parts that have C-parts of PRECIP-INC, SWE, TEMPERATURE-AIR-AVG
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
    locList = c1.intersection(At)
    
#         print '\n#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'
#         print '# B-Parts that have all the required data (Precip, SWE, & Temp)  =', bList
#         print '#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#'

    locDict={}
    for b in bList:
        ws = dssFile.getCatalogedPathnames("/*/"+b+"/*/*/*/*/")
        for bee in ws:
            splitter = bee.split('/')
            locDict[b] = splitter[1]
#         print '\n Aparts for each B-part:', locDict
    return locDict, bList

def getList(locDict):
    # Converting into list of tuples for JList to use
    locList = [("/"+str(v)+"/"+str(k)+"/") for k, v in locDict.items()]
    
#     locList = [str(r) for r in locList]
#     print locList
    
    return locList    

locDict, bList = getPaths(dssFile)
locList = getList(locDict)
# print locList
# for i, v in enumerate(locList):
#     for x,y in enumerate(locList):
#         print locList[i][x]
def getSelectedLocations(listLocations):
        # Get Selected Location.
#         print list_locations.getSelectedValuesList()
        # Get DSS pathnames based on Selection.
        swePaths = []
        tempPaths = []
        precipPaths = []
        for a_and_b_parts in listLocations:
#             print a_and_b_parts + "SWE/*/*/*/"
#             print dssFile.getCatalogedPathnames(a_and_b_parts + "SWE/*/*/*/")
            swePaths.append(dssFile.getCatalogedPathnames(a_and_b_parts + "SWE/*/*/*/"))
            precipPaths.append(dssFile.getCatalogedPathnames(a_and_b_parts + "PRECIP-INC/*/*/*/"))
            tempPaths.append(dssFile.getCatalogedPathnames(a_and_b_parts + "TEMPERATURE-AIR-AVG/*/*/*/"))
        return swePaths, precipPaths, tempPaths
    
def getPairedData(dssFile):
    pdPaths = dssFile.getCatalogedPathnames("/*/*/ATI-Melt/*/*/*/")
    
    # Remove Full Water Year Paired Data Paths from List to be added to the UI. 
    for i in xrange(len(pdPaths)-1,-1,-1):
        splitter = pdPaths[i].split("/")
        f = splitter[6]
        if len(f) == 7:
            del pdPaths[i]  
        
    lList = []
    eList = []
    for path in pdPaths:
        splitter = path.split("/")
        a = splitter[1]
        b = splitter[2]
        f = splitter[6]
#         print a
#         print b
        lList.append( a+"/"+b )
        eList.append( f )
    return lList, eList