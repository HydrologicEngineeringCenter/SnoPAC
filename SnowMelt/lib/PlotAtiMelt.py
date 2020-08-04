from hec.heclib.dss         import HecDss
from Locations              import getPaths, getList
from hec.script import Plot, AxisMarker
from hec.dssgui     import ListSelection
import Locations


# global loctDict



# mainWindow = ListSelection.getMainWindow()
# dssFileName = mainWindow.getDSSFilename()
# dssFile = HecDss.open(dssFileName)
# 
# locDict, bList = getPaths(dssFile)
# locList = getList(locDict)
dssFile = Locations.dssFile

##3 Viewports
##Top: Temp, Melt- 32degree Marker Line
##Middle: Precip (hanging), SWE
##Bottom: ATI
def plotAtiMelt(selected):
    for a_and_b_parts in selected:
        # Make sure class level locDict and bList isnt being used to extend bList beyond the selected paths in the UI Locations Table.
#         print '\na_and_b_parts: ', a_and_b_parts

#         aPart = locDict[b]
        title = a_and_b_parts.replace("/", " ")
                
        sp = a_and_b_parts +"SWE/*/1DAY/SNOTEL/"
        sd = dssFile.get(sp,1)
     
        tp = a_and_b_parts +"TEMPERATURE-AIR-AVG/*/1DAY/SNOTEL/"
        td = dssFile.get(tp,1)
     
        pp = a_and_b_parts +"PRECIP-INC/*/1DAY/SNOTEL/"
        pd = dssFile.get(pp,1)
     
        ap = a_and_b_parts + "ATI/*/1DAY/CALC/"
        ad = dssFile.get(ap,1)
     
        mp = a_and_b_parts + "MELT-CUM/*/1DAY/CALC/"
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
        thePlot = Plot.newPlot(title)
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