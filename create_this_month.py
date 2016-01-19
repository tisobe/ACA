#!/usr/bin/env /proj/sot/ska/bin/python

#############################################################################################
#                                                                                           #  
#           create_this_month.py: create monthly script for the month                       #
#           author: t. isobe (tisobe@cfa.harvard.edu)                                       #
#                                                                                           #
#           last update: Nov 16, 2015                                                       #
#                                                                                           #
#############################################################################################

import os
import sys
import re
import random
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
rtail  = int(10000 * random.random())       #---- put a romdom # tail so that it won't mix up with other scripts space
zspace = '/tmp/zspace' + str(rtail)
#
#--- main path
#
dir_path = '/data/mta4/www/DAILY/mta_pcad/ACA/Script/'
out_path = '/data/mta4/www/DAILY/mta_pcad/ACA/'

#-------------------------------------------------------------------------------------------
#-- create_this_montcreate_this_month: create ACA monthly script for the month           ---
#-------------------------------------------------------------------------------------------

def create_this_montcreate_this_month():
    """
    create ACA monthly script for the month
    input:  none, but read from ./Template
    outpu:  a file named .update_this_month
    """


    tlist = tcnv.currentTime()

    year  = str(tlist[0])
    syr   = year[2] + year[3]

    mon   = int(float(tlist[1]))
    smon  = str(tlist[1])
    if mon < 10:
        smon = '0' + smon
    lmon  = tcnv.changeMonthFormat(mon)
#
#--- format of: 2015_05
#
    yearmon = year + '_' + smon

#--- format of: MAY15
#
    umonyr  = lmon + syr
    umonyr  = umonyr.upper()
#
#--- format of: may15
#
    lmonyr  = umonyr.lower()


    file = dir_path + 'Template/update_temp'
    f    = open(file, 'r')
    data = f.read()
    f.close()

    data = data.replace('#YEAR_MON#', yearmon)
    data = data.replace('#UMONYR#',   umonyr)
    data = data.replace('#LMONYR#',   lmonyr)


    ofile = out_path + 'update_this_month'
    fo    = open(ofile, 'w')
    fo.write(data)
    fo.close()

    cmd = 'chmod 755 ' + ofile
    os.system(cmd)
#
#--- make output directory
#
    cmd = 'mkdir ' + out_path + '/' + umonyr
    os.system(cmd)
    cmd = 'mkdir ' + out_path + '/' + umonyr + '/Report'
    os.system(cmd)
    cmd = 'mkdir ' + out_path + '/' + umonyr + '/Data'
    os.system(cmd)

#-------------------------------------------------------------------------------------------

if  __name__ == "__main__":

    create_this_montcreate_this_month()




