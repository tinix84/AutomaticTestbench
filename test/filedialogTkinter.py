# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 15:56:20 2013

@author: 212334547
"""

import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()
print file