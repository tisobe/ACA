#!/usr/bin/env /proj/sot/ska/bin/python

#############################################################################################
#                                                                                           #  
#   process_data_for_the_month.py: extract and process aca data for the given year/month    #
#                                                                                           #
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
#--- extract_data: extract needed data for the given year/month                   --
#-----------------------------------------------------------------------------------

def extract_data(year, month):
    """
    extract needed data for the given year/month
    input:  year    --- year
            month   --- month
    output: <outdir>/<fits data>
    """

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
    else:
        cmd = 'rm -f '  + outdir + '/*fits*'

    os.system(cmd)

    cmd = 'mv *fits* ' + outdir
    os.system(cmd)

#-----------------------------------------------------------------------------------
#-- add_leading_zeros: adding leading zero to adjust digit                        --
#-----------------------------------------------------------------------------------

def add_leading_zeros(val):
    """
    adding leading zero to adjust digit
    input:   val    --- value (int/float)
    output: cval    --- adjusted value in string format
    """

    cval = str(val)
    if val < 10:
        cval = '00' + cval
    elif val < 100:
        cval = '0'  + cval

    return cval

#-----------------------------------------------------------------------------------
#-- run_arc5gl: extract data from archive using arc5gl                           ---
#-----------------------------------------------------------------------------------

def run_arc5gl(operation, detector, subdetector, level, filetype, tstart, tstop):
    """
    extract data from archive using arc5gl
    input:  operation   --- retrive/browse
            detector    --- detector
            subdetector --- sub detector name; defalut: '' (none)
            level       --- level
            filetype    --- filetype
            tstart      --- starting time
            tstop       --- stopping time
    ouptut: extracted fits file
            data        --- a list of fits file extracted
    """

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

#-------------------------------------------------------------------------------------------
#-- create_this_montcreate_this_month: create ACA monthly script for the month           ---
#-------------------------------------------------------------------------------------------

def create_this_montcreate_this_month(year, mon):
    """
    create ACA monthly script for the month
    input:  year    --- year
            mon     --- mon
    outpu:  a file named .update_this_month
    """

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


    ofile = './update_this_month'
    fo    = open(ofile, 'w')
    fo.write(data)
    fo.close()

    cmd = 'chmod 755 ' + ofile
    os.system(cmd)
#
#--- make output directory
#
    out = out_path + '/' + umonyr + '/'
    if not os.path.isdir(out):
        cmd = 'mkdir ' + out
        os.system(cmd)

    out = out + '/Report/'
    if not os.path.isdir(out):
        cmd = 'mkdir ' + out
        os.system(cmd)

    out = out + '/Data/'
    if not os.path.isdir(out):
        cmd = 'mkdir ' + out
        os.system(cmd)


#-----------------------------------------------------------------------------------

if __name__ == "__main__":

    year  = int(float(sys.argv[1]))
    month = int(float(sys.argv[2]))

    extract_data(year, month)

    create_this_montcreate_this_month(year, month)

    os.system('update')

#    for year in range(2016, 2019):
#        for month in range(1, 13):
#            if year == 2016 and month < 2:
#                continue
#            if year == 2018 and month > 2:
#                break
#
#            extract_data(year, month)
#
#            create_this_montcreate_this_month(year, month)
#
#            os.system('update')


