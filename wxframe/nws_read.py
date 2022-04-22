"""

Retrieve information from NWS website

"""

import requests

nws_url = "https://forecast.weather.gov/product.php?site=NWS&issuedby=MTR&product=AFD&format=CI&version=1&glossary=1&highlight=off"

def get_synopsis( url=nws_url ):
    # Open the url
    r = requests.get( url, stream = True )
    
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        content = r.text
        # Trim text down to synopsis only
        synopsis = content[ content.find(".SYNOPSIS.")+12 : content.find(".DISCUSSION.")-6 ]
        synopsis = remove_html(synopsis)
        marine   = content[ content.find(".MARINE.")+10 : content.find(".MTR WATCHES/WARNINGS/ADVISORIES.")-6 ]
        marine   = remove_html(marine)
    else:
        print(url)
        raise RuntimeWarning("Couldn't access webpage!")
        
    return synopsis, marine

def remove_html( string ):
    # Remove all html commands enclosed by <>
    new = ""
    text = True
    for i in string:
        if i == "<":
            text = False
        elif i == ">":
            text = True
        elif text:
            new = new + i
    return rm_text( new )

def rm_text( string ):
    return string.replace("-- End Changed Discussion --", "").replace("-- Changed Discussion --", "").replace("\n", " ")

if __name__ == "__main__":
    print( get_synopsis() )