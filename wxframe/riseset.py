"""

Retrieve sunrise/sunset data from web

"""

import requests
from nws_read import remove_html

srss_url = "https://sunrise-sunset.org/us/pacific-grove-ca"

def get_riseset( url=srss_url ):
    # Open the url
    r = requests.get( url, stream = True )
    
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        content = r.text
        # Trim text down to sunrise time only
        sunrise = content[ content.find('Sunrise time:')+14 : content.find('Sunrise time:')+40 ]
        sunrise = "0" + remove_html(sunrise)[:4]
        # Trim text down to sunset time only
        sunset  = content[ content.find('Sunset time:')+13 : content.find('Sunset time:')+40]
        sunset  = remove_html(sunset)[:4]
        # Convert sunset to 24 hour time
        sunset  = str(int(sunset[:1])+12)+sunset[1:4]
    else:
        print(url)
        raise RuntimeWarning("Couldn't access webpage!")
        
    return sunrise, sunset

if __name__ == "__main__":
    print( get_riseset() )