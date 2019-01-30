# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:18:53 2014

@author: 212334547
"""

keyword_list=['WASHER', 'SCREW']
all_text  = "test_string"
print any # so we can see where it comes from
mkgen = lambda: (word in all_text for word in keyword_list)
print list(mkgen()) # to see what we have

if any(mkgen()):
    print "any: some of the strings found in str"
else:
    print "any: no strings found in str"

if (True in mkgen()):
    print "in: some of the strings found in str"
else:
    print "in: no strings found in str"