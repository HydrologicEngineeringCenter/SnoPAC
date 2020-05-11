import PlotPD
from javax.swing import JOptionPane
from collections import defaultdict
from javax.swing.table import DefaultTableModel
# from hec.io         import PairedDataContainer

def calcMeltRate(selectedEvents, eventsTable, meltRateTable, dssFile):
    # Error Checking Boolean
    breakTheLoop = False
    # Get Selected Paired Data.
    pdPaths = PlotPD.getPDPaths(selectedEvents, eventsTable, dssFile)
#     print pdPaths
    # Get user specified ATI from MeltRate Table.
    tableData = meltRateTable.getModel().getDataVector()
    atiBands = []
    for data in tableData:
        if data[0] is not None:
            try:
                atiBands.append(float(data[0]))
            except: 
                JOptionPane.showMessageDialog(None, "ATI values must be numeric.", "Meltrate Table Warning", JOptionPane.WARNING_MESSAGE)
    
    
    # Check for errors in ATI input.
    for k, v in enumerate(atiBands):
#         print 'atiBands[k]=',str(atiBands[k]), '  atiBands[k-1]=', str(atiBands[k-1])
        if k == 0 and v != 0:
            JOptionPane.showMessageDialog(None, "First ATI value must be equal to zero.", "Meltrate Table Warning", JOptionPane.WARNING_MESSAGE)
        elif k != 0 and ( atiBands[k] <= atiBands[k-1] ):
            JOptionPane.showMessageDialog(None, "ATI values must be ascending. Check row %d." % (k+1), "Meltrate Table Warning", JOptionPane.WARNING_MESSAGE)

    # To get the Meltrate, Calculate Slope for each Paired Data set. For each PD set, calculate an average slope at for each ATI band entered in the table. 
    meltRateList = []
    slopeDict = defaultdict(list)   
    for pd in pdPaths:       
        slopeList = []
        print "\npdPath: ", pd
        data = dssFile.get(pd[0])
        atiOrds_ugly = data.xOrdinates
        atiOrds = []
        # Round all ati values to 2 decimals.
        for a in atiOrds_ugly:
            atiOrds.append(round(float(a),2))
        
        # Check for error in ATI input, if max atiBand is beyond the data chosen, throw an error.
        if max(atiBands) > max(atiOrds):
            JOptionPane.showMessageDialog(None, "ATI Table exceeds max ATI = %04.3f in %s." % (max(atiOrds), str(pd)), "Meltrate Table Warning", JOptionPane.WARNING_MESSAGE)
            breakTheLoop = True
            
           
        meltOrds_ugly = data.yOrdinates
        # Fix y-ordinates to a single list instead of multi-curve capable array. Also round to 2 digits.
        meltOrds_ugly = meltOrds_ugly.tolist()
        meltOrds = []
        for m in meltOrds_ugly[0]:
            meltOrds.append(round(float(m),2))
        
        
        # Lookup via Linear Interpolation the Melt-Cum values at upper and lower ATI values.
        
        # x1 = atiOrd_below, a known value in atiOrds.
        # x2 = The ATI boundary value in Table we want to use to calculate Meltrate with.
        # x3 = atiOrd_above, a known value in atiOrds.
        # y1 = the melt associated with atiOrd_below, a known value in meltOrds.
        # y2 = the boundary melt we are solving for via linear interpolation.
        # y3 = the melt associated with atiOrd_above, a known value in meltOrds.
        
#         print 'atiOrds: ',  atiOrds
#         print 'meltOrds: ',  meltOrds
        
        # For each Paired Data set, add the max ATI value at the end of the atiBands list.
        # This value is removed before moving to the next Paired Dataset.
        atiBands.append(atiOrds[-1])            
        
        # Loop ATI Bands for The interpolation and slope calcs.
        for k, v in enumerate(atiBands):
            # Skip the first iteration.
            if k == 0:
                continue
           
            # Get the upper and lower ATI Band to calculate Meltrate on.
            lowerTableATI = float(atiBands[k-1])
            upperTableATI = float(atiBands[k])
#             print '\nlowerATI =', lowerTableATI
#             print 'upperTableATI =', upperTableATI
#             
        
            lowerTableAtiHit = False
            upperTableAtiHit = False
            
            for i, ordy in enumerate(atiOrds):
                if ordy >= lowerTableATI and lowerTableAtiHit ==  False:
#                     print 'ordy >= lowerTableATI at i, ordy: ', i,", ",ordy
                    lowerTableAtiHit = True
                    if i == 0:
                        atiOrd_below_lowerATI = atiOrds[i]
                        atiOrd_above_lowerATI = atiOrds[i]
                        meltOrd_below_lowerMelt = meltOrds[i]
                        meltOrd_above_lowerMelt = meltOrds[i]
                    else:
                        atiOrd_below_lowerATI = atiOrds[i-1]
                        atiOrd_above_lowerATI = atiOrds[i]
                        meltOrd_below_lowerMelt = meltOrds[i-1]
                        meltOrd_above_lowerMelt = meltOrds[i]
                    
                if ordy >= upperTableATI and upperTableAtiHit == False:
#                     print 'ordy >= upperTableATI at i, ordy: ', i,", ",ordy
                    upperTableAtiHit = True
                    if i == 0:
                        atiOrd_below_upperATI = atiOrds[i]
                        atiOrd_above_upperATI = atiOrds[i]
                        meltOrd_below_upperMelt = meltOrds[i]
                        meltOrd_above_upperMelt = meltOrds[i]
                    else:
                        atiOrd_below_upperATI = atiOrds[i-1]
                        atiOrd_above_upperATI = atiOrds[i]
                        meltOrd_below_upperMelt = meltOrds[i-1]
                        meltOrd_above_upperMelt = meltOrds[i]
                    
                    
                    
            # Interpolate the upper and lower MeltCum that occurs at the lowerTableATI and upperTableATI:
            # y2 = y1 + (x2 -x1)[(y3-y1)/(x3-x1)]

            # lowerMeltCum = (meltOrd_below_lowerMelt) + ((lowerTableATI - atiOrd_below_lowerATI) * ((meltOrd_above_lowerMelt - meltOrd_below_lowerMelt)/(atiOrd_above_lowerATI - atiOrd_below_lowerATI)))
            # upperMeltCum = (meltOrd_below_upperMelt) + ((upperTableATI - atiOrd_below_upperATI) * ((meltOrd_above_upperMelt - meltOrd_below_upperMelt)/(atiOrd_above_upperATI - atiOrd_below_upperATI)))
            
            # Interpolation equation broken into pieces to ensure not dividing by zero.
#             print 'meltOrd_above_upperMelt ', meltOrd_above_upperMelt
#             print 'meltOrd_below_upperMelt', meltOrd_below_upperMelt
#             print 'meltOrd_above_lowerMelt', meltOrd_above_lowerMelt
#             print 'meltOrd_below_lowerMelt', meltOrd_below_lowerMelt
#             
            
            l1 = meltOrd_above_lowerMelt - meltOrd_below_lowerMelt
            l2 = atiOrd_above_lowerATI - atiOrd_below_lowerATI
            if l2>0:
                l3 = l1/l2
            else:
                l3 = 0 
            l4 = lowerTableATI - l3
            l5 =l3*l4
            lowerMeltCum = meltOrd_below_lowerMelt + l5
             
            u1 = meltOrd_above_upperMelt - meltOrd_below_upperMelt
            u2 = atiOrd_above_upperATI - atiOrd_below_upperATI
            if u2>0:
                u3 = u1/u2
            else:
                u3 = 0 
            u4 = upperTableATI - u3
            u5 =u3*u4
            upperMeltCum = meltOrd_below_upperMelt + u5          

            print 'upperMeltCum = ', upperMeltCum
            print 'lowerMeltCum = ', lowerMeltCum
            
            # Calculate the Slope from upper and lower values.
            # slope = (y2 - y1) / (x2- x1)
            if upperTableATI - lowerTableATI == 0:
                slope = 0
            else:
                slope = (upperMeltCum - lowerMeltCum) / (upperTableATI - lowerTableATI)
            slope = round(slope, 4)
            slopeList.append(slope)
            print 'slope at ATI Band [%03.2f to %03.2f] = %03.5f' % (lowerTableATI, upperTableATI, slope)
            
#         print 'slopeList: ', slopeList
        
            slopeDict[k].append( slope )
#         print slopeDict
        
        # Remove Paired Dataset's max ATI value. Will be replaced with the next set's max value.
        atiBands = atiBands[:-1]
        
    slopes = sorted(slopeDict.items())
#     print 'slopes', slopes
    # For each row in the Melt Rate table, k, take an average of the slopes and append to the MeltRateList which will be added to the UI Table.
    # '{:.4f}'.format handles the float formatting to show four decimal places for the MeltRate.
    for k, s in slopes:
        averageSlope = sum(s)/float(len(s))
        meltRateList.append('{:.4f}'.format(averageSlope))
    
    # If errors were found in the PD loop do not populate the table.
    if breakTheLoop == True:
        return
    else:
        print 'meltRateList: ', meltRateList
        return meltRateList
    
def updateTable(meltRateTable, meltRateList, dm_meltRate):
    if meltRateList is not None:
        tableData = meltRateTable.getModel().getDataVector()
        atiBands = []
        updatedTableData = []
        #Get Table ATI values
        for data in tableData:
            if data[0] is not None:
                atiBands.append(float(data[0]))
        
        # Update Data Vector with ATI and Meltrate data
        for a, m in zip(atiBands, meltRateList):
            updatedTableData.append([a,m])
        
        # Append blank rows to have 100 rows.
        blankRows = 100 - len(atiBands)
        for i in range(blankRows):
            updatedTableData.append([None, None])
        
        # Delete Old Data to set new Data.
        dm_meltRate.setRowCount(0)
        
        # Set new Data.
        columns = ("ATI (Deg F-Day)", "Meltrate (Inches/Deg F-Day)")
        dm_meltRate.setDataVector(updatedTableData, columns)
        meltRateTable.repaint()
    else:
        print '\nMeltRates were not Computed.'
        