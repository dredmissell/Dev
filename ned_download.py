###--  Name:    ned_download.py
###--- Purpose: Automatically downloads staged 1 ArcSecond (30m) NED tiles from USGS Tiled Distribution System
###--  Author, Ed Bissell, 3/5/2013, modified to run on Linux


import urllib2
import urllib
import sys,os
import glob
import zipfile
import shutil
import errno, stat
import logging
from BeautifulSoup import BeautifulSoup
import ftplib
import socket


zip_nhd_path = os.path.join("F:/NHD/Raw_HU4s")
def download_nhd_zips ():
    ftpurl = "rockyftp.cr.usgs.gov"
    nhdurl = "vdelivery/Datasets/Staged/Hydrography/NHD/HU4/HighResolution/Shape/"
    print "Connecting...."
    ftp = ftplib.FTP(ftpurl, "anonymous")
    ##ftp.set_pasv(False)
    ftp.cwd(nhdurl)
    print "Connected...."
    files = ftp.nlst('*.zip')
    for file in files:
        print "Downloading " + file + ".................."
        outfile = None
        outfile = open(zip_nhd_path + os.sep + file, "wb")
        ftp.retrbinary("RETR " + file, outfile.write)
        outfile.close()

    # # this range should catch CONUS
    # for x in xrange(93, 66, -1):  ## 99, 64, -1 change from 125 to 99 and add 0 below
    # #for x in xrange(93, 66, -1): ## 99, 64, -1 change from 125 to 99 and add 0 below
    #     for y in xrange(51, 24, -1):  ## 51, 24, -1
    #         try:
    #             url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/NHD/HU4/HighResolution/Shape/NHD_H_n%sw0%s.zip" % (y, x)
    #             # works for full url
    #             #url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1/IMG/USGS_NED_1_n%sw%s_IMG.zip" % (y, x)
    #             tile = "n%sw%s.zip" % (y, x)
    #             dest = os.path.join(zip_path, tile)
    #             ##if os.path.isfile(dest) or os.path.isfile(os.path.join(hpcc_path, tile)):
    #             if os.path.isfile(dest):
    #                 print "/n%sw%s.zip Already Downloaded" % (y, x)
    #             else:
    #
    #                 print "Downloading " + url
    #
    #                 ###########################
    #                 opener = urllib.URLopener()
    #                 opener.retrieve(url, dest)
    #                 ###########################
    #
    #                 print "Downloaded " + tile
    #         except IOError as e:
    #             print "I/O error({0}): {1}".format(e.errno, e.strerror)
    #             print "Skipped " + tile

download_nhd_zips()

# ###############################################################################################################################################


zip_path = os.path.join("F:/NED/RAW_TILES_9_2016/")
# extract_path = os.path.join("c:/ned/extract2/")
# hpcc_path = os.path.join("Z:\\NED")
def download_zips ():
    # this range should catch CONUS
    for x in xrange(93, 66, -1):  ## 99, 64, -1 change from 125 to 99 and add 0 below
    #for x in xrange(93, 66, -1): ## 99, 64, -1 change from 125 to 99 and add 0 below
        for y in xrange(51, 24, -1):  ## 51, 24, -1
            try:
                url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1/IMG/n%sw0%s.zip" % (y, x)
                # works for full url
                #url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1/IMG/USGS_NED_1_n%sw%s_IMG.zip" % (y, x)
                tile = "n%sw%s.zip" % (y, x)
                dest = os.path.join(zip_path, tile)
                ##if os.path.isfile(dest) or os.path.isfile(os.path.join(hpcc_path, tile)):
                if os.path.isfile(dest):
                    print "/n%sw%s.zip Already Downloaded" % (y, x)
                else:

                    print "Downloading " + url

                    ###########################
                    opener = urllib.URLopener()
                    opener.retrieve(url, dest)
                    ###########################

                    print "Downloaded " + tile
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                print "Skipped " + tile

#download_zips()




  ###doesn't really work as expected just extract with 7zip
def unzip_files ():


    for zip_file in glob.iglob(zip_path + "*.zip"):        
        print zip_file
        print os.path.basename(zip_file)[1:6]
        with zipfile.ZipFile(zip_file, 'r') as zip:            
            for f in zip.infolist():
                test = f.filename
                name_index = f.filename.startswith('\grd')
                print f.filename
                if name_index:
                    continue
                dest = os.path.join(extract_path, f.filename)

                if dest.endswith('/'):
                    if os.path.isdir(dest):
                        shutil.rmtree(dest, ignore_errors=False, onerror=handleRemoveReadonly)  
                    os.makedirs(dest)
                else:
                    try:
                        with open(dest, 'wb') as fout:
                            fout.write(zip.read(f))
                    except IOError as e:
                        print "I/O error({0}): {1}".format(e.errno, e.strerror)
                        print "Skipped " + dest

##unzip_files()


###doesn't really work as expected just extract with 7zip
def unzip():

    logger = logging.getLogger()
    hdlr = logging.FileHandler('badzips.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)

    for zip_file in glob.iglob(zip_path + "*.zip"):     
        print zip_file    
        basename = os.path.basename(zip_file)[0:6]
        basenamePath = extract_path + basename[:4] + "0" + basename[4:]
        zipDir = "grd" + basename[:4] + "0" + basename[4:] + "_13"
        print basenamePath
        isZip = zipfile.is_zipfile(zip_file)
        gridExists = os.path.isdir(basenamePath)
        if not(gridExists):
            if isZip:  #skip it if it is bad zip
                with zipfile.ZipFile(zip_file) as zf:
                    for member in zf.infolist():
                        # Path traversal defense copied from
                        # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
                        words = member.filename.split('/')
                        path = extract_path
                        for word in words[:-1]:
                            if word.startswith(zipDir):
                                #drive, word = os.path.splitdrive(word)
                                #head, word = os.path.split(word)
                                #if word in (os.curdir, os.pardir, ''): continue
                                ##path = os.path.join(path, word)
                                zf.extract(member, path)

            else:
                logger.error(zip_file + 'was bad')
        else: 
            print("Output zip file " + zip_file + "already exists")
##unzip()
















