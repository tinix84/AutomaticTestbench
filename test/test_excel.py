import win32com.client as win32

excel=win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible=True
wb=excel.Workbooks.Open(r"c:\Temp\test.xlsx", False, True)
excel.Visible = True

# store default worksheet object so we can delete it later
ws = wb.Worksheets(1)
ws.Cells(1,1).Value = "Cell A1"
ws.Cells(1,1).Offset(2,4).Value = "Cell D2"
ws.Range("A2").Value = "Cell A2"
ws.Range("A3:B4").Value = "A3:B4"
ws.Range("A6:B7,A9:B10").Value = "A6:B7,A9:B10"
# command like SaveAs takes the root directory the Document of the current user
wb.SaveAs('ranges_and_offsets.xlsx')
#excel.Application.Quit()
