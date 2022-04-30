"""

Retrieve satellite imagery from GOES-17

"""

import shutil
import requests
import config.locs

goes_url = "https://whirlwind.aos.wisc.edu/~wxp/goes17/vis_color/westcoast/"
goes_loc = config.locs.image_dir + "wc_goes\\"
goes_lst = ["latest_westcoast_%s.jpg"%i for i in range(73)[1:]]

def get_goes( ):
    for img in goes_lst:
        # Open the url
        r = requests.get( goes_url+img, stream = True )
        # Check if the webpage was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True
            filename = goes_loc + img
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

if __name__ == "__main__":
    get_goes()

