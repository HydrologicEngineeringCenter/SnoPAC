'''
Created on Nov 15, 2019

@author: q0hecmbm
'''
import os
import sys
from datetime import datetime
from java.awt import Color, Font, Image
# from java.awt import Insets
from java.awt.event import MouseAdapter, MouseMotionAdapter, KeyEvent
from javax.imageio import ImageIO
from javax.swing import ImageIcon, JFrame, JPanel, JLabel, JTextField, JButton, KeyStroke, AbstractAction, JComponent
from javax.swing import JTable, JList, JScrollPane, JCheckBox, SwingConstants
# from javax.swing import InputMap, ActionMap, ListSelectionModel
from javax.swing.border import EmptyBorder, LineBorder
from javax.swing.table import DefaultTableModel
# from javax.swing import DefaultListModel
from java.io import File
# from java.util import Arrays, Collections

from hec.heclib.dss     import HecDss, HecDataManager
# from hec.util import CalendarField
def lib_dir_311():
    parent_dir = os.getcwd()
    global lib_dir
    lib_dir = os.path.join(parent_dir, 'HecDssVue\scripts\lib')
    global img_dir
    img_dir = os.path.join(parent_dir, 'HecDssVue\scripts\Images')
    print lib_dir
    sys.path.append(lib_dir)

def lib_dir_321():
    parent_dir = os.path.join(os.environ['APPDATA'], 'DSSVue', 'scripts')
    global lib_dir2
    lib_dir2 = os.path.join(parent_dir, 'lib')
    global img_dir2
    img_dir2 = os.path.join(parent_dir, 'Images')
    print lib_dir2
    sys.path.append(lib_dir2)

# Add lib directory to module search path for CWMS 3.2.1 and forward
lib_dir_321()
lib_dir_311()
# Add lib directory to module search path for CWMS 3.1.1 and forward
import Locations, CalcAtiMelt, PlotAtiMelt, ProcessPD, CalcPD, PlotPD, CalcMeltRate

now = datetime.now().strftime("%H-%M-%S")
HecDataManager.setMessageFile("_".join(["C:\\temp\\","Snow_PAC", now , ".log"]))
HecDataManager.setMessageLevel(5)

class UI:
    global dssFile
    dssFile = HecDss.open(r"C:\jy\SnowMelt\snotel_3v6.dss")
    global frame, lbl_close, list_locations, chckbxShowLocationPlot, eventsTable, dm_events, dm_meltRate
    global swePaths, precipPaths, tempPaths, bList, meltRateTable, startDateField, endDateField
    
    frame = JFrame("Snow PAC - Parameter Aggregator & Calculator")
#     frame.setUndecorated(True)  
    frame.setBackground(Color.WHITE)
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setBounds(100, 100, 1110, 775);
    
    contentPane = JPanel();
    contentPane.setBackground(Color.WHITE);
    contentPane.setBorder(EmptyBorder(5, 5, 5, 5));
    
    frame.setContentPane(contentPane);
    contentPane.setLayout(None);
    
    class MouseListener(MouseAdapter):
#       @Override
        def mousePressed(self, e):              
            global xx
            global xy
            xx = e.getX()
            xy = e.getY()

    class MouseMotionListener(MouseMotionAdapter):
#       @Override
        def mouseDragged(self, arg0):      
                x = arg0.getXOnScreen();
                y = arg0.getYOnScreen();
                frame.setLocation(x - xx, y - xy)
    
    mL = MouseListener()
    mML = MouseMotionListener()
    contentPane.addMouseListener(mL)
    contentPane.addMouseMotionListener(mML)
    
    if os.path.exists(img_dir + "/button.jpg"):
        btnIcon = ImageIcon(img_dir +"/button.jpg")
    else:
        btnIcon = ImageIcon(img_dir2 +"/button.jpg")
        
    
    scrollPane_events = JScrollPane()
    scrollPane_events.setBounds(270, 372, 403, 263)
    contentPane.add(scrollPane_events)
     
    scrollPane_locations = JScrollPane();
    scrollPane_locations.setBounds(270, 49, 403, 203);
    contentPane.add(scrollPane_locations);  
    
    class deleteAction(AbstractAction):
    
        def actionPerformed(self, deleteEvent):
            # Get selected Rows and reverse list. Removes each row in list one at a time.
            # List is Reversed using [::-1], so it doesn't mess up the ordering as it deletes through the loop.
            for row in meltRateTable.getSelectedRows()[::-1]:
                dm_meltRate.removeRow(row)
                dm_meltRate.insertRow(row, [None, None])

    scrollPane_table =  JScrollPane();
    scrollPane_table.setBounds(708, 49, 338, 586);
    contentPane.add(scrollPane_table);
    
    meltRateTable =  JTable();
    scrollPane_table.setViewportView(meltRateTable);
    scrollPane_table.setBorder(LineBorder(Color(1, 1, 1), 2, True))
    meltRateTable.setFont( Font("Tahoma", Font.PLAIN, 11));
    
    columns = ("ATI (Deg F-Day)", "Meltrate (Inches/Deg F-Day)")
    data = []
    datarows = 100
    data.append([0,None])
    for i in range(datarows):
            data.append([None, None])
    dm_meltRate = DefaultTableModel(data, columns)
    
    meltRateTable.setModel(dm_meltRate)
    
    meltRateTable.getColumnModel().getColumn(0).setPreferredWidth(154);
    meltRateTable.getColumnModel().getColumn(1).setResizable(False);
    meltRateTable.getColumnModel().getColumn(1).setPreferredWidth(154);
    meltRateTable.setCellSelectionEnabled(True);
    
#    Delete data from the table using the Delete Key.
#     meltRateTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

    inputMap = meltRateTable.getInputMap(JComponent.WHEN_FOCUSED);
    actionMap = meltRateTable.getActionMap();

    deleteActionStr = "delete";
    inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_DELETE, 0), deleteActionStr);
    actionMap.put(deleteActionStr, deleteAction())
                  
#     jLabelStartDate = JLabel()
#     jLabelStartDate.setText("Optional Start Date:")
#     jLabelStartDate.setToolTipText("Optional User Specified Date Range for Paired Data. If Specified, Will be Calculated for each Water Year.")
#     jLabelStartDate.setBounds(420, 263, 120, 20);
#     jLabelStartDate.setFont( Font("Tahoma", Font.PLAIN, 12))
#     contentPane.add(jLabelStartDate)
#     
#     startDateField = CalendarField();
#     jLabelStartDate.setLabelFor(startDateField);
#     startDateField.setMargin(Insets(0, 4, 0, 0));
#     startDateField.setBounds(540, 263, 118, 22);
#     startDateField.setFont(Font("Tahoma", Font.PLAIN, 12));
#     startDateField.setToolTipText("Optional User Specified Date Range for Paired Data. If Specified, Will be Calculated for each Water Year.")
#     contentPane.add(startDateField);
#     
#     jLabelEndDate = JLabel()
#     jLabelEndDate.setText("Optional End Date:")
#     jLabelEndDate.setToolTipText("Optional User Specified Date Range for Paired Data. If Specified, Will be Calculated for each Water Year.")
#     jLabelEndDate.setBounds(420, 293, 120, 20);
#     jLabelEndDate.setFont( Font("Tahoma", Font.PLAIN, 12))
#     contentPane.add(jLabelEndDate)
#     
#     endDateField = CalendarField();
#     jLabelEndDate.setLabelFor(endDateField);
#     endDateField.setMargin(Insets(0, 4, 0, 0));
#     endDateField.setBounds(540, 293, 118, 22);
#     endDateField.setFont(Font("Tahoma", Font.PLAIN, 12));
#     endDateField.setToolTipText("Optional User Specified Date Range for Paired Data. If Specified, Will be Calculated for each Water Year.")
#     contentPane.add(endDateField);

    def recalcBtnSelect(event):
        global swePaths, precipPaths, tempPaths
        selectedLocations = list_locations.getSelectedValuesList()
        swePaths, precipPaths, tempPaths = Locations.getSelectedLocations(selectedLocations)
        pathsNoDPart, sList, pList, tList = CalcAtiMelt.processPathsLists(swePaths, precipPaths, tempPaths)
        dList = CalcAtiMelt.processPathsDatesList(pathsNoDPart)
        aList, mList = CalcAtiMelt.calcATIMelt(selectedLocations, sList, pList, tList, dList)
        
        # Write Melt-Cum and ATI Locations to DSS.
        CalcAtiMelt.writeAtiMelt(selectedLocations, dList, aList, mList)
       
        # Plot Locations if checkbox.selected = True.
        if chckbxShowLocationPlot.selected is True:
#             print '\nPLOT TEAM ACTIVATE'
            PlotAtiMelt.plotAtiMelt(selectedLocations)
            
        # Use optional specified dates if fields are not blank.
#         if startDateField.getText() and endDateField.getText() is not None:
#             pdStart, pdEnd = ProcessPD.getSpecifiedDates(startDateField, endDateField)
#         else:
        pdStart = None
        pdEnd = None
            
        # Create Paired Data for Selected Locations.
        ProcessPD.processPairedData(selectedLocations, dList, mList, aList, pdStart, pdEnd)
        
        # Populate the UI Paired Data Table.
        CalcPD.updatePDTable(dssFile, eventsTable, dm_events)
        
        # Close the DSS File.
        dssFile.close()
        
    def plotPDBtnSelect(event):
        selected_Events = eventsTable.getSelectedRows()
#         print 'selected_Events: ', selected_Events
        # Sorting of the table by selecting the headers is doen by using: eventsTable.setAutoCreateRowSorter(True)
        # This sorts the table but does not update the table model.
        # To ensure sorting and selecting of resulting paths works properly, 
        # we must convert our selection using: eventsTable.convertRowIndexToModel(event)
        selectedEvents = []
        for event in selected_Events:
            selectedEvents.append(eventsTable.convertRowIndexToModel(event))
#         print 'selectedEvents: ', selectedEvents
        PlotPD.plotPD(eventsTable, selectedEvents, dssFile)
        dssFile.close()
    def calcMeltRateBtnSelect(event):
        selected_Events = eventsTable.getSelectedRows()
        selectedEvents = []
        for event in selected_Events:
            selectedEvents.append(eventsTable.convertRowIndexToModel(event))
        meltRateList = CalcMeltRate.calcMeltRate(selectedEvents, eventsTable, meltRateTable, dssFile)
        CalcMeltRate.updateTable(meltRateTable, meltRateList, dm_meltRate)
        dssFile.close()
    locDict, bList = Locations.getPaths(dssFile)
    locList = Locations.getList(locDict)
        
    list_locations = JList(locList);
    scrollPane_locations.setViewportView(list_locations);
    list_locations.setBorder(LineBorder(Color(0, 0, 0), 2, True))
    
    
    eventsTable =  JTable();
    scrollPane_events.setViewportView(eventsTable)
    scrollPane_events.setBorder(LineBorder(Color(1, 1, 1), 2, True))
    eventsTable.setFont( Font("Tahoma", Font.PLAIN, 11));
    
    locationsList, eventsList = Locations.getPairedData(dssFile)
    
    columns = ("Location", "Event")
    data = []
    for l, e in zip(locationsList, eventsList):
            data.append([l, e])
    dm_events = DefaultTableModel(data, columns)
    
    eventsTable.setModel(dm_events)
    eventsTable.setAutoCreateRowSorter(True)
    
    eventsTable.getColumnModel().getColumn(0).setPreferredWidth(154);
    eventsTable.getColumnModel().getColumn(1).setResizable(False);
    eventsTable.getColumnModel().getColumn(1).setPreferredWidth(154);
    eventsTable.setRowSelectionAllowed(True)
    
    inputPanel =  JPanel();
    inputPanel.setBorder( EmptyBorder(0, 0, 0, 0));
    inputPanel.setBackground( Color(255, 255, 255));
    inputPanel.setBounds(270, 11, 410, 27);
    contentPane.add(inputPanel);
    inputPanel.setLayout(None);
    inputPanel.setVisible(True);
    
    lbl_locations =  JLabel("DSS Locations that have PRECIP-INC, TEMPERATURE-AIR-AVG, and SWE. ");
    lbl_locations.setFont( Font("Tahoma", Font.PLAIN, 12));
    lbl_locations.setBounds(0, 11, 410, 15);
    inputPanel.add(lbl_locations);
    
    btnRecalc = JButton(btnIcon, actionPerformed=recalcBtnSelect);
    btnRecalc.setText("Calculate Paired Data")
    btnRecalc.setFont(Font("Tahoma", Font.BOLD, 12));
    btnRecalc.setForeground(Color.WHITE);
    btnRecalc.setBackground(Color.WHITE);
    btnRecalc.setBorderPainted(False); 
    btnRecalc.setContentAreaFilled(False); 
    btnRecalc.setFocusPainted(False); 
    btnRecalc.setOpaque(True);
    btnRecalc.setVerticalTextPosition(SwingConstants.CENTER);
    btnRecalc.setHorizontalTextPosition(SwingConstants.CENTER);
    btnRecalc.setBounds(382, 293, 165, 54);
    contentPane.add(btnRecalc);
    
    
    leftPanel = JPanel();
    leftPanel.setBackground(Color.DARK_GRAY);
    leftPanel.setBounds(0, 0, 250, 780);
    contentPane.add(leftPanel);
    leftPanel.setLayout(None);
     
    lbl_castle = JLabel("");
    lbl_castle.setBounds(110, 678, 40, 25);
    leftPanel.add(lbl_castle);
    
    try:
        i_corps = ImageIO.read(File(img_dir + "/CorpsCastle.png"));
    except:
        i_corps = ImageIO.read(File(img_dir2 + "/CorpsCastle.png"));
        
    corpsCastle = i_corps.getScaledInstance(lbl_castle.getWidth(), lbl_castle.getHeight(), Image.SCALE_SMOOTH);
     
    lbl_castle.setVerticalAlignment(SwingConstants.TOP);
    lbl_castle.setIcon(ImageIcon(corpsCastle));
     
    lbl_logo = JLabel("");
    lbl_logo.setBounds(18, 294, 218, 148);
    leftPanel.add(lbl_logo);
    
    try:
        snowLogo = ImageIO.read(File(img_dir + "/melted-snowman.png"));
    except:
        snowLogo = ImageIO.read(File(img_dir2 +"/melted-snowman.png"));
        
     
    dssLogo = snowLogo.getScaledInstance(lbl_logo.getWidth(), lbl_logo.getHeight(),
            Image.SCALE_SMOOTH);
 
    lbl_logo.setVerticalAlignment(SwingConstants.TOP);
    lbl_logo.setIcon(ImageIcon(dssLogo));    
     
    lbl_logo2 = JLabel("");
    lbl_logo2.setBounds(18, 11, 218, 148);
    leftPanel.add(lbl_logo2);
     
    try:
        snowPacLogo = ImageIO.read(File(img_dir +"/SnowPac.png"));
    except:
        snowPacLogo = ImageIO.read(File(img_dir2 +"/SnowPac.png"));
        
     
    snowPac = snowPacLogo.getScaledInstance(lbl_logo2.getWidth(), lbl_logo2.getHeight(),
            Image.SCALE_SMOOTH);
 
    lbl_logo2.setVerticalAlignment(SwingConstants.TOP);
    lbl_logo2.setIcon(ImageIcon(snowPac));
    
#     lbl_close = JLabel("X")
#     
#     class CloseClickListener(MouseAdapter):
# #       @Override
#         def mouseEntered(self):     
#             lbl_close.setBorder(LineBorder.createGrayLineBorder())
# #       @Override
#         def mouseExited(self):
#             lbl_close.setBorder(None)
# #       @Override
#         def mouseClicked(self):
#             lbl_close.setBorder(BorderFactory.createLineBorder(Color.red));
#             sys.exit();
     
#     cL = CloseClickListener()
#     lbl_close.addMouseListener(cL)
#     
#     lbl_close.setHorizontalAlignment(SwingConstants.CENTER);
#     lbl_close.setForeground(Color(241, 57, 83));
#     lbl_close.setFont(Font("Tahoma", Font.PLAIN, 18));
#     lbl_close.setBounds(1071, 0, 37, 27);
#     contentPane.add(lbl_close);
    
    lblPxf = JLabel("Base Temperature (F):");
    lblPxf.setToolTipText("The temperature at which melt will occur.");
    lblPxf.setFont(Font("Tahoma", Font.PLAIN, 12));
    lblPxf.setBounds(400, 263, 132, 15);
    contentPane.add(lblPxf);

    
    textField_8 = JTextField();
    textField_8.setFont(Font("Tahoma", Font.PLAIN, 12));
    textField_8.setToolTipText("The temperature at which melt will occur.");
    textField_8.setText("32.0");
    textField_8.setBounds(548, 263, 40, 20);
    contentPane.add(textField_8);
    textField_8.setColumns(10);
    
    chckbxShowLocationPlot =  JCheckBox("Plot Locations");
    chckbxShowLocationPlot.setToolTipText("Will plot the Temp, Precip, SWE, ATI, and Melt for each selected location.");
    chckbxShowLocationPlot.setSelected(True);
    chckbxShowLocationPlot.setBackground(Color.WHITE);
    chckbxShowLocationPlot.setFont( Font("Tahoma", Font.PLAIN, 12));
    chckbxShowLocationPlot.setBounds(547, 310, 120, 23);
    contentPane.add(chckbxShowLocationPlot);
    
    
    
    lblEvents =  JLabel("Paired Data");
    lblEvents.setBounds(270, 346, 72, 15);
    contentPane.add(lblEvents);
    lblEvents.setFont( Font("Tahoma", Font.PLAIN, 12));
     
#     lblAtiThreshold = JLabel("ATI Threshold:");
#     lblAtiThreshold.setToolTipText("Some Melt Events are small & can be ignored. The ATI Threshold is a value that must be reached for the event to be listed.");
#     lblAtiThreshold.setFont(Font("Tahoma", Font.PLAIN, 12));
#     lblAtiThreshold.setBounds(500, 610, 82, 15);
#     contentPane.add(lblAtiThreshold);
    
#     textField_9 = JTextField();
#     textField_9.setFont(Font("Tahoma", Font.PLAIN, 12));
#     textField_9.setText("0.0");
#     textField_9.setToolTipText("Some Melt Events are small & can be ignored. The ATI Threshold is a value that must be reached for the event to be listed.");
#     textField_9.setColumns(10);
#     textField_9.setBounds(600, 608, 60, 20);
#     contentPane.add(textField_9);   
    
    btnPlot = JButton(btnIcon, actionPerformed=plotPDBtnSelect);
    btnPlot.setText("Plot Paired Data")
    btnPlot.setFont(Font("Tahoma", Font.BOLD, 12));
    btnPlot.setForeground(Color.WHITE);
    btnPlot.setBackground(Color.WHITE);
    btnPlot.setBorderPainted(False); 
    btnPlot.setContentAreaFilled(False); 
    btnPlot.setFocusPainted(False); 
    btnPlot.setOpaque(False);
    btnPlot.setVerticalTextPosition(SwingConstants.CENTER);
    btnPlot.setHorizontalTextPosition(SwingConstants.CENTER);
    btnPlot.setBounds(385, 657, 163, 54);
    contentPane.add(btnPlot);
    
    lblAtimeltrateTable =  JLabel("ATI-Meltrate Table");
    lblAtimeltrateTable.setFont(Font("Tahoma", Font.PLAIN, 12));
    lblAtimeltrateTable.setBounds(708, 10, 410, 15);
    contentPane.add(lblAtimeltrateTable);
    
    lblAtimeltrateTable2 =  JLabel("The first ATI value should be 0. ATI values must be ascending.");
    lblAtimeltrateTable2.setFont(Font("Tahoma", Font.PLAIN, 11));
    lblAtimeltrateTable2.setBounds(708, 30, 410, 15);
    contentPane.add(lblAtimeltrateTable2);
    
    btnCalculateMeltrate =  JButton(btnIcon, actionPerformed=calcMeltRateBtnSelect);
    btnCalculateMeltrate.setText("Calculate Meltrate")
    btnCalculateMeltrate.setFont( Font("Tahoma", Font.BOLD, 12));
    btnCalculateMeltrate.setToolTipText("Calculate Meltrate for ATI values in the ATI-Meltrate Table. Calculation will performed on the Paired Data Records Selected in the Paired Data Table.")
    btnCalculateMeltrate.setForeground(Color.WHITE);
    btnCalculateMeltrate.setBackground(Color.WHITE);
    btnCalculateMeltrate.setBorderPainted(False); 
    btnCalculateMeltrate.setContentAreaFilled(False); 
    btnCalculateMeltrate.setFocusPainted(False); 
    btnCalculateMeltrate.setOpaque(False);
    btnCalculateMeltrate.setVerticalTextPosition(SwingConstants.CENTER);
    btnCalculateMeltrate.setHorizontalTextPosition(SwingConstants.CENTER);
    btnCalculateMeltrate.setBounds(792, 657, 163, 54);
    contentPane.add(btnCalculateMeltrate);                        
            
    
         
    
    
    frame.setVisible(True)
    dssFile.close()