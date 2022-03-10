"""

Retrieve images from the web

"""

import shutil
import requests
import tkinter as tk
import config.locs
from PIL import Image, ImageTk

#####################################
#                                   #
#   Saved URLs for updating plots   #
#                                   #
#####################################

# Pivotal Weather daily CONUS weather forecast images
ndfd_loc = "https://maps8.pivotalweather.com/maps/ndfd/latest/"
pw_conus_maxtemp_url = ndfd_loc + "ndfd_sfctmax.conus.png"
pw_conus_mintemp_url = ndfd_loc + "ndfd_sfctmin.conus.png"
pw_conus_24hrqpf_url = ndfd_loc + "ndfd_24hqpf.conus.png"
pw_conus_24hsnow_url = ndfd_loc + "ndfd_24hsnow.conus.png"
# Coastal Data Information Program swell map
cdip_swell_url = "http://cdip.ucsd.edu/recent/model_images/monterey.png"
# NWS Pacific Grove meteogram
nws_meteogram_url = "https://forecast.weather.gov/meteograms/Plotter.php?lat=36.6285&lon=-121.9352&wfo=MTR&zcode=CAZ530&gset=18&gdiff=3&unit=0&tinfo=PY8&ahour=0&pcmd=11011111111110000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=&bw=&hrspan=48&pqpfhr=6&psnwhr=6"

#
img_dir = config.locs.image_dir
# Each image data (source url, local dir+filename)
pw_conus_maxtemp = ( pw_conus_maxtemp_url, img_dir+"pw_conus_maxtemp.png" )
pw_conus_mintemp = ( pw_conus_mintemp_url, img_dir+"pw_conus_mintemp.png" )
pw_conus_24hrqpf = ( pw_conus_24hrqpf_url, img_dir+"pw_conus_24hrqpf.png" )
pw_conus_24hsnow = ( pw_conus_24hsnow_url, img_dir+"pw_conus_24hsnow.png" )
cdip_swell       = ( cdip_swell_url,       img_dir+"cdip_swell.png" )
nws_meteogram    = ( nws_meteogram_url,    img_dir+"nws_meteogram.png" )

# All image data
images = ( pw_conus_maxtemp, pw_conus_mintemp, pw_conus_24hrqpf,
           pw_conus_24hsnow, cdip_swell, nws_meteogram )


def get_img( url, filename ):
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get( url, stream = True )
    
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
    
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
    else:
        print(url)
        raise RuntimeWarning("Couldn't download image!")
        
def crop_meteogram( path=nws_meteogram[1], debug=False ):
    # Opens a image in RGB mode
    im = Image.open(path)
    # Crop specs for removing unnecessary vars from plot
    im1 = im.crop((0, 0, 800, 420))
    # Debug mode for checking crop specs
    if debug:
        # Shows the image in image viewer
        im1.show()
    else:
        # Overwrite previous image
        im1.save(path)
        
def get_imgs( ):
    #
    for img in images:
        get_img( img[0], img[1] )
    
    crop_meteogram()
        
        
def show_img( path, xx=0, yy=0 ):
    # Create a photoimage object of the image in the path
    image = Image.open(path)
    test = ImageTk.PhotoImage(image)
    
    label = tk.Label(image=test)
    label.image = test
    
    # Position image
    label.place(anchor='center', relx=xx, rely=yy)
    #label.pack()


if __name__ == "__main__":
    #get_img( pw_conus_maxtemp[0], img_dir+"test.png" )
    crop_meteogram( debug=False )