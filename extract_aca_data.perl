#!/usr/bin/perl

#--------------------------------------------------------------------------------
#   extract_aca_data.perl
#
#       this script extract data for ACA computation. 
#       make sure that you have a directory ./Input
#
#       author: t. isobe (tisobe@cfa.harvard.edu)
#       last update: Nov 17, 2015
#
#---------------------------------------------------------------------------------

$dare   = `cat /data/mta/MTA/data/.dare`;
$hakama = `cat /data/mta/MTA/data/.hakama`;
chomp $dare;
chomp $hakama;

#
#--- change following for your need
#
$year  = '15';                          #--- the year must be two digit format (e.g., 07, 15 etc)
$month = '12';                          #--- the month must be two digit format (e.g. 03, 10 etc)
$start = 1;                             #--- start date
$stop  = 31;                            #--- stop date

if($year < 90){
    $syear = '20'."$year";
}else{
    $syear = '19'."$year";
}

for($i = $start; $i <= $stop; $i++){
    $day = $i;
    if($i < 10){
        $day = "0$i";
    }

    $dir = "Input/"."$syear".'_'."$month"."_"."$day";
    system("mkdir $dir");

    extract($dir, $day);
}

#-------------------------------------------------------------------------------
#-- extract: extract data using arc4gl                                       ---
#-------------------------------------------------------------------------------

sub extract($dir, $day){

    $date = "$month"."/$day".'/'."$year";

    open(OUT, ">./aline" );
    print OUT "operation=retrieve\n";
    print OUT "dataset=flight\n";
    print OUT "detector=pcad\n";
    print OUT "subdetector=aca\n";
    print OUT "level=1\n";
    print OUT "filetype=acacent\n";
    print OUT 'tstart='."$date".",00:00:00\n";
    print OUT 'tstop='."$date".",23:59:59\n";
    print OUT "go\n";
    close(OUT);

    system("echo $hakama |arc4gl -U$dare -Sarcocc -ialine");

    open(OUT, ">./aline" );
    print OUT "operation=retrieve\n";
    print OUT "dataset=flight\n";
    print OUT "detector=pcad\n";
    print OUT "subdetector=aca\n";
    print OUT "level=1\n";
    print OUT "filetype=gsprops\n";
    print OUT 'tstart='."$date".",00:00:00\n";
    print OUT 'tstop='."$date".",23:59:59\n";
    print OUT "go\n";
    close(OUT);


    system("echo $hakama |arc4gl -U$dare -Sarcocc -ialine");

    open(OUT, ">./aline" );
    print OUT "operation=retrieve\n";
    print OUT "dataset=flight\n";
    print OUT "detector=pcad\n";
    print OUT "subdetector=aca\n";
    print OUT "level=1\n";
    print OUT "filetype=fidprops\n";
    print OUT 'tstart='."$date".",00:00:00\n";
    print OUT 'tstop='."$date".",23:59:59\n";
    print OUT "go\n";
    close(OUT);

    system("echo $hakama |arc4gl -U$dare -Sarcocc -ialine");

    system("gzip -d *fits.gz $dir");
    system("mv *fits $dir");
}

