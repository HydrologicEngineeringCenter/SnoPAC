from hec.script import Plot

def getPDPaths(selectedEvents, eventsTable, dssFile):
    a_and_b_parts = []
    f_parts = []
    pdPaths = []
    
#     row = eventsTable.getSelectedRow();
    for row in selectedEvents:
        a_and_b_parts.append(eventsTable.getModel().getValueAt(row, 0))
        f_parts.append(eventsTable.getModel().getValueAt(row, 1))
#     print a_and_b_parts
#     print f_parts
    for ab, f in zip(a_and_b_parts, f_parts):
        pdPaths.append(dssFile.getCatalogedPathnames("/" + ab + "/ATI-Melt/*/*/" + f + "/"))
    return pdPaths

def plotPD(eventsTable, selectedEvents, dssFile):
    pdPaths = getPDPaths(selectedEvents, eventsTable, dssFile)
    
    layout = Plot.newPlotLayout()
    topView = layout.addViewport()
    
    data = []
    for path in pdPaths:
#         print path
        data = dssFile.get(path[0],1)
        topView.addCurve("Y1", data)
     
    title = "ATI vs Melt-Cum Paired Data"     
    thePlot = Plot.newPlot(title)
    thePlot.configurePlotLayout(layout)
    thePlot.showPlot()