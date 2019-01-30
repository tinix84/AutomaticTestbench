# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 17:19:58 2012

@author: tinix84
"""
import re
import json

import sys
sys.path.append('../lib/')
from lrf_histogram import *

def main():

    read_filename = '../Mx120508193220.txt'
    fid_rd = open(read_filename,'r')
    foo = fid_rd.read()
    stream = re.findall(r'[a-zA-Z0-9_\-\n\r<%\*]', foo)
    fid_rd.close()
    
    write_filename = '../m120508193220.mxj'
    fid_wr = open(write_filename,'wt')

    mx_cmd_info = MxCommand()
    mx_cmd_info = load_data_from_mxstream(mx_cmd_info, stream)
    json_string = json.dumps(mx_cmd_info['target'])
    print json_string
    fid_wr.write(json.dumps(mx_cmd_info['target']))
    fid_wr.close()
    
if __name__ == "__main__":
    main()