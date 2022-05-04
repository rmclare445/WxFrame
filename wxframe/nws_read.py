"""

Retrieve information from NWS website

"""

import requests
from tools.text_tools import remove_html

nws_url  = "https://forecast.weather.gov/product.php?site=NWS&issuedby=MTR&product=AFD&format=CI&version=1&glossary=1&highlight=off"
noaa_url = "https://www.wrh.noaa.gov/mtr/getzfpzone.php?sid=mtr&zone=caz530"
dlh_url  = "https://forecast.weather.gov/product.php?site=DLH&issuedby=DLH&product=ZFP&format=txt&version=1&glossary=0"

def get_synopsis( url=nws_url ):
    # Open the url
    r = requests.get( url, stream = True )
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        content = r.text
        # Trim text down to synopsis only
        synopsis = content[ content.find(".SYNOPSIS.")+12 : content.find(".DISCUSSION.")-6 ]
        synopsis = rm_text( remove_html(synopsis) )
        marine   = content[ content.find(".MARINE.")+10 : content.find(".MTR WATCHES/WARNINGS/ADVISORIES.")-6 ]
        marine   = rm_text( remove_html(marine) )
    else:
        print(url)
        raise RuntimeWarning("Couldn't access webpage!")
        
    return synopsis, marine


def get_wrh( url=noaa_url ):
    # Open the url
    r = requests.get( url, stream = True )
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        #content = remove_html( r.text.replace("<br>", "\n") )
        content = r.text
        return content
    

# def get_dlh( url=dlh_url ):
#     # Open the url
#     r = requests.get( url, stream = True )
#     # Check if the webpage was retrieved successfully
#     if r.status_code == 200:
#         content = r.text[r.text.find('Carlton and South St. Louis-'):r.text.find('$$')]
#         return content


def rm_text( string ):
    return string.replace("-- End Changed Discussion --", "").replace("-- Changed Discussion --", "").replace("\n", " ")


if __name__ == "__main__":
    #print( get_synopsis() )
    print( get_wrh() )