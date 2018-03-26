#!/usr/bin/env /proj/sot/ska/bin/python

#############################################################################################
#                                                                                           #  
#           create_this_month.py: create monthly script for the month                       #
#           author: t. isobe (tisobe@cfa.harvard.edu)                                       #
#                                                                                           #
#           last update: Mar 26, 2018                                                       #
#                                                                                           #
#############################################################################################

import os
import sys
import re
import time
#
#--- reading directory list
#
path = '/data/mta/Script/Python_script2.7/dir_list_py'

f    = open(path, 'r')
data = [line.strip() for line in f.readlines()]
f.close()

for ent in data:
    atemp = re.split(':', ent)
    var  = atemp[1].strip()
    line = atemp[0].strip()
    exec "%s = %s" %(var, line)

#
#--- append a path to a private folder to python directory
#
sys.path.append(mta_dir)

import mta_common_functions as mcf
import convertTimeFormat    as tcnv

#
#--- temp writing file name
#
rtail  = int(time.time())
zspace = '/tmp/zspace' + str(rtail)

dmon1 = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334] 
dmon2 = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335] 

#
#--- main path
#
dir_path = '/data/mta4/www/DAILY/mta_pcad/ACA/Script/'
out_path = '/data/mta4/www/DAILY/mta_pcad/ACA/'
outdir   = './Input/'

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

def extract_data(year, month):

    if tcnv.isLeapYear(year) == 1:
        mlist = dmon2
    else:
        mlist = dmon1

    yday1 = mlist[month-1] + 1
    year2 = year

    if month == 12:
        yday2 = 1
        year2 += 1
    else:
        ydat2 = mlist[month] + 1

    cyday1 = add_leading_zeros(yday1)
    cyday2 = add_leading_zeros(yday2)

    tstart = str(year)  + ':' + cyday1 + ':00:00:00'
    tstop  = str(year2) + ':' + cyday2 + ':00:00:00'

    out1 = run_arc5gl('retrieve', 'pcad', 'aca', '1', 'acacent',  tstart, tstop)
    out2 = run_arc5gl('retrieve', 'pcad', 'aca', '1', 'gsprops',  tstart, tstop)
    out3 = run_arc5gl('retrieve', 'pcad', 'aca', '1', 'fidprops', tstart, tstop)

    if not os.path.isdir(outdir):
        cmd = 'mkdir '  + outdir
        os.system(cmd)

    cmd = 'mv *fits* ' + outdir
    os.system(cmd)

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

def add_leading_zeros(val):

    cval = str(val)
    if val < 10:
        cval = '00' + cval
    elif val < 100:
        cval = '0'  + cval

    return cval

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

def run_arc5gl(operation, detector, subdetector, level, filetype, tstart, tstop):

    line = 'operation=' + str(operation) + '\n'
    line = line + 'dataset=flight\n'
    line = line + 'detector=' + str(detector) + '\n'
    if subdetector != "":
        line = line + 'subdetector=' + str(subdetector) + '\n'
    line = line + 'level=' + str(level) + '\n'
    line = line + 'filetype=' + str(filetype) + '\n'
    line = line + 'tstart='   + str(tstart)   + '\n'
    line = line + 'tstop='    + str(tstop)    + '\n'
    line = line + 'go\n'

    fo   = open(zspace, 'w')
    fo.write(line)
    fo.close()

    try:
        cmd = ' /proj/sot/ska/bin/arc5gl   -user isobe -script ' + zspace + '> ztemp_out'
        os.system(cmd)
    except:
        cmd = ' /proj/axaf/simul/bin/arc5gl -user isobe -script ' + zspace + '> ztemp_out'
        os.system(cmd)

    mcf.rm_file(zspace)
    
    f     = open('./ztemp_out', 'r')
    data  = [line.strip() for line in f.readlines()]
    f.close()

    data = data[2:]

    mcf.rm_file('./ztemp_out')

    return data

#-----------------------------------------------------------------------------------

if __name__ == "__main__":

    year  = int(float(sys.argv[1]))
    month = int(float(sys.argv[2]))
    extract_data(year, month)
