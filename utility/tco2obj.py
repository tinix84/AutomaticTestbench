# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 08:00:59 2012

@author: tricc
"""
import numpy as np
import re

class VTXTermCmdGroupNode(object):
    def __init__(self, cmd_group_name, stream):
        self.name=cmd_group_name
        self.cmd_group=self.create_cmd_group_node(cmd_group_name, stream)

    def set_name(self, cmd_group_name):
        self.name = cmd_group_name

    def create_cmd_group_node(self, cmd_group_name, stream):
        cmd_group={}
        suffix=re.sub("Tab","",cmd_group_name)
        pattern_cmd="Cmd"+suffix+"[0-9]+"
        cmd_list = re.findall(pattern_cmd, stream)
        print cmd_list
        for item in cmd_list:
            print item
            cmd_group[item]=VTXTermCmdNode()
            pattern_cmd_capt=item[0:3]+"Capt"+item[3:5]+"="
            pattern_cmd_syntax=pattern_cmd+"=>"
            pattern_cmd_term1=item[0:3]+"Term1"+item[3:5]+"="
            pattern_cmd_term2=item[0:3]+"Term2"+item[3:5]+"="
            full_row=re.findall(pattern_cmd_capt+".*", stream)
            cmd_group[item].set_name(re.sub(pattern_cmd_capt,"",full_row[0]))
            full_row=re.findall(pattern_cmd_syntax+".*", stream)
            cmd_group[item].set_syntax(re.sub(pattern_cmd_syntax,"",full_row[0]))
            full_row=re.findall(pattern_cmd_term1+".*", stream)
            cmd_group[item].set_enableLF(re.findall(pattern_cmd_term1+".*", full_row[0]))
            full_row=re.findall(pattern_cmd_term2+".*", stream)
            cmd_group[item].set_enableCR(re.findall(pattern_cmd_term2+".*", full_row[0]))
        return cmd_group

class VTXTermCmdNode(object):
    def __init__(self):
        self.name=None
        self.syntax=None
        self.enableLF=False
        self.enableCR=False

    def set_name(self, name):
        self.name = name

    def set_syntax(self, syntax):
        self.syntax = syntax

    def set_enableLF(self, status):
        self.enableLF = status

    def set_enableCR(self, status):
        self.enableCR = status

class VTXTermCmdTree(object):
    def __init__(self, stream):
        #number of tabs in file
        self.cmd_tree = {}
        tab_list=re.findall(r"Tab\w*=\w*", stream)
        for item in tab_list:
            tab_name=re.sub("Tab\w*=","",item)
            index=re.sub("=\w*","",item)
            self.cmd_tree[index]=VTXTermCmdGroupNode(index, stream)
            self.cmd_tree[index].set_name(tab_name)


    def get_name_VTXTermCmdGroupNode(self):
        pass
    def get_name_VTXTermCmdNode(self):
        pass

def tco2pyobj(read_filename):

    fid_rd = open(read_filename,'r')
    stream = fid_rd.read()
    fid_rd.close()
    tco_tree=VTXTermCmdTree(stream)
    return tco_tree

if __name__ == '__main__':
    filename = "./Term-ModB12.tco"
    tco_tree=tco2pyobj(filename)
