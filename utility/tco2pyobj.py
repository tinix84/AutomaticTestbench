# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 08:00:59 2012

@author: tricc
"""
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
        #print cmd_list
        for item in cmd_list:
            #print item
            cmd_group[item]=VTXTermCmdNode()
            pattern_cmd_capt="CmdCapt"+item[3:]+"="
            pattern_cmd_syntax=item+"="
            print pattern_cmd_syntax
            pattern_cmd_term1="CmdTerm1"+item[3:]+"="
            pattern_cmd_term2="CmdTerm2"+item[3:]+"="
            full_row=re.findall(pattern_cmd_capt+".*", stream)
            cmd_group[item].set_name(re.sub(pattern_cmd_capt,"",full_row[0]))
            #print pattern_cmd_capt
            #print cmd_group[item].name
            full_row=re.findall(pattern_cmd_syntax+".*", stream)
            try:
                cmd_group[item].set_syntax(re.sub(pattern_cmd_syntax,"",full_row[0]))
            except IndexError:
                cmd_group[item].set_syntax(None)
            full_row=re.findall(pattern_cmd_term1+".*", stream)
            cmd_group[item].set_enableLF(re.sub(pattern_cmd_term1,"", full_row[0]))
            full_row=re.findall(pattern_cmd_term2+".*", stream)
            cmd_group[item].set_enableCR(re.sub(pattern_cmd_term2,"", full_row[0]))
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
        if status == "True":
            self.enableLF = True

    def set_enableCR(self, status):
        if status == "True":
            self.enableCR = True


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


def tco2pyobj(read_filename):

    fid_rd = open(read_filename,'r')
    stream = fid_rd.read()
    fid_rd.close()
    tco_tree=VTXTermCmdTree(stream)
    return tco_tree

if __name__ == '__main__':
    filename = "./Term-ModB12.tco"
    tco_tree=tco2pyobj(filename)
