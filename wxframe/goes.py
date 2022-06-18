"""

Retrieve satellite imagery from GOES-17

"""

import shutil
import requests
from tools.system_tools import img_dir, sep

name = 'GOES West Coast'
cdir = -1                               # Cycling direction
url  = "https://whirlwind.aos.wisc.edu/~wxp/goes17/vis_color/westcoast/"
loc  = img_dir + "wc_goes" + sep
lst  = ["latest_westcoast_%s.jpg"%i for i in range(73)[1:]]

def get_goes( parent ):
    #parent.status_dialogue( 'UPDATING GOES...' )
    parent.goes_update = True
    for img in lst:
        # Open the url
        r = requests.get( url+img, stream = True )
        # Check if the webpage was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True
            filename = loc + img
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
    parent.goes_update = False
    #parent.rm_status_dialogue()

if __name__ == "__main__":
    get_goes()

