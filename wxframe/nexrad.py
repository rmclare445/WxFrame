"""

Retrieve NEXRAD frames from UW

"""

import shutil
import requests
import config.locs

nexrad_url = "https://tempest.aos.wisc.edu/radar/"
nexrad_loc = config.locs.image_dir + "nexrad\\"
nexrad_lst = ["us3comp%02d.gif"%i for i in range(21)[1:]]

def get_nexrad( ):
    for img in nexrad_lst:
        # Open the url
        r = requests.get( nexrad_url+img, stream = True )
        # Check if the webpage was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True
            filename = nexrad_loc + img
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

if __name__ == "__main__":
    get_nexrad()