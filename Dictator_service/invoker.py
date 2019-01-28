"""
@Author		:Furqan Khan
@Email		:furqankhan08@gmail.com
@Date 		:1/2/2017

Objective :
The purpose of this file /module /Class is to launch discovery process with gui mode .
Invoker.py is actually responsible for calling main_class_based_backip.py along with project_id and relevent details like host ,port and switch etc.This would start the nmap discovery process and a process will keep on
running in the background which shall do the discovery and save the details in the database table.
"""

import main_class_based_backup as main
import os
import ConfigParser
import time
import psutil
import subprocess
import sys


NmapScanObj=main.NmapScan()

targethosts=sys.argv[1]
path=sys.argv[2]
targetports=sys.argv[3]
scan_type=sys.argv[4]
switch=sys.argv[5]
project_id=sys.argv[6]
mode=sys.argv[7]
assessment_id=sys.argv[8]
app_id=sys.argv[9]
concurrent=sys.argv[10]

print "concurrent is :"+str(concurrent)

if concurrent=="0":
	conc=False
else:
	conc=True
print "Inside INVOKER.PY \n\n"
print (targethosts,path,targetports,scan_type,switch,project_id,mode,assessment_id,app_id,concurrent)
NmapScanObj.driver_main(targethosts,path,targetports,scan_type,switch,project_id,mode,assessment_id,app_id,conc)



		

