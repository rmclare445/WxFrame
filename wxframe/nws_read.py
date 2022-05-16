"""

Retrieve information from NWS website

"""

import requests
from tools.text_tools import remove_html, cap_first

nws_url  = "https://forecast.weather.gov/product.php?site=NWS&issuedby=MTR&product=AFD&format=CI&version=1&glossary=1&highlight=off"
noaa_url = "https://www.wrh.noaa.gov/mtr/getzfpzone.php?sid=mtr&zone=caz530"

def get_synopsis( url=nws_url ):
    # Open the url
    r = requests.get( url, stream = True )
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        content = r.text
        # Trim text down to synopsis only
        synopsis = content[ content.find(".SYNOPSIS.")+12 : content.find(".DISCUSSION.")-6 ]
        synopsis = rm_text( remove_html(synopsis) )
        return cap_first( synopsis )
    else:
        print(url)
        raise RuntimeWarning("Couldn't access webpage!")
        
        
def get_marine( url=nws_url ):
    r = requests.get( url, stream = True )
    if r.status_code == 200:
        content = r.text
        # Trim text down to marine synopsis only
        marine   = content[ content.find(".MARINE.")+10 : content.find(".MTR WATCHES/WARNINGS/ADVISORIES.")-6 ]
        return cap_first( rm_text( remove_html( marine ) ) )


def get_discussion( url=nws_url ):
    r = requests.get( url, stream = True )
    if r.status_code == 200:
        content = r.text
        pd = content.find(".PREV DISCUSSION.")-6
        av = content.find(".AVIATION.")-6
        if min(pd, av) > 0:
            end = min(pd, av)
        else:
            end = max(pd, av)
        discuss  = content[ content.find(".DISCUSSION.")+14 : end ]
        discuss  = remove_html(discuss)
        # Remove newlines, retain paragraph breaks
        discuss = discuss.replace("\n\n", "walrus")
        discuss = rm_text( discuss )
        discuss = discuss.replace("walrus", "\n\n")
        
        return cap_first( discuss )


def get_wrh( url=noaa_url ):
    # Open the url
    r = requests.get( url, stream = True )
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        #content = remove_html( r.text.replace("<br>", "\n") )
        content = r.text
        return content


def rm_text( string ):
    return string.replace("-- End Changed Discussion --", "").replace("-- Changed Discussion --", "").replace("\n", " ")


if __name__ == "__main__":
    print( len(get_discussion()) )