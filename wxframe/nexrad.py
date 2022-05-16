"""

Retrieve NEXRAD frames from UW

"""

import shutil
import requests
import config.locs

name = 'NEXRAD'
cdir  = 1                                               # Correct direction for cycling
url  = "https://tempest.aos.wisc.edu/radar/"            # URL image host
loc  = config.locs.image_dir + "nexrad\\"               # Local image directory
lst  = ["us3comp%02d.gif"%i for i in range(21)[1:]]     # List of file names

def get_nexrad( parent ):
    parent.status_dialogue( 'UPDATING NEXRAD...' )
    parent.nexrad_update = True
    for img in lst:
        # Open the url
        r = requests.get( url+img, stream = True )
        # Check if the webpage was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True
            filename = loc + img
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
    parent.nexrad_update = False
    parent.rm_status_dialogue()

if __name__ == "__main__":
    get_nexrad()