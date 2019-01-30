# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:11:40 2014

@author: 212334547
"""
import win32com

xl = win32com.client.gencache.EnsureDispatch('Excel.Application')
xl.Visible = True
wb = xl.Workbooks.Add()
ws = xl.ActiveSheet
ws.Range('A1').FormulaR1C1 = 'X'
ws.Range('B1').FormulaR1C1 = 'Y'
ws.Range('A2').FormulaR1C1 = 1
ws.Range('A3').FormulaR1C1 = 2
ws.Range('A4').FormulaR1C1 = 3
ws.Range('B2').FormulaR1C1 = 4
ws.Range('B3').FormulaR1C1 = 5
ws.Range('B4').FormulaR1C1 = 6
#ws.Range('A1:B4').Select()
ch = ws.Shapes.AddChart().Select()
xl.ActiveChart.ChartType = ch.xlXYScatterLines
xl.ActiveChart.SetSourceData(Source=ws.Range("A1:B4"))
#ch.Location(10,10) # something like this?