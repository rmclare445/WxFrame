'''

Retrieve GOES-West fire temperature imagery from NOAA NESDIS

'''

import os, glob
import shutil
import requests
from datetime import datetime
from tools.system_tools import img_dir, sep

name = 'West Coast Fire'
cdir = 1                            # Correct direction for cycling
url  = "https://cdn.star.nesdis.noaa.gov/GOES17/ABI/SECTOR/psw/FireTemperature/"
loc  = img_dir + "cafire" + sep     # Local image directory


def get_localfiles( ):
    raw_lst = sorted( glob.glob( loc+"*" ) )
    return [fn[len(loc):] for fn in raw_lst]


def get_filenames( interval=3 ):
    ''' Generate filenames for nesdis images, interval may be 1 for 10 min,
         2 for 20 min, or 3 for half-hour. NOTE: If you change the interval, 
         you should clear the img/cafire directory because it will not 
         necessarily overwrite old images.
    '''
    now = datetime.now().timetuple()

    dtg_yd = "%04d%03d" % (now.tm_year, now.tm_yday)
    dtg_mins = ["%s1" % i for i in range(6)][::interval]

    # Create datetime group list for past 24 hours
    dtgs = []
    # Yesterday
    for hr in range(now.tm_hour,24):
        dtgs = dtgs + [str(int(dtg_yd)-1)+("%02d"%hr)+minute for minute in dtg_mins]
    # Today
    for hr in range(0,now.tm_hour):
        dtgs = dtgs + [dtg_yd+("%02d"%hr)+minute for minute in dtg_mins]

    # Append file group suffix
    return [dtg+"_GOES17-ABI-psw-FireTemperature-1200x1200.jpg" for dtg in dtgs]


def get_nesdis( ):

    lst = get_filenames( )
    local_names = get_localfiles()
    
    # Remove images not in new list
    for img in list( set(local_names) - set(lst) ):
        os.remove( loc + img )
    
    # Get images not already in directory
    for img in list( set(lst) - set(local_names) ):
        # Open the url
        r = requests.get( url+img, stream = True )
        # Check if the webpage was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True
            filename = loc + img
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)


if __name__ == "__main__":
    get_nesdis()