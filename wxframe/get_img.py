"""

Retrieve images from the web

"""

import shutil
import requests
#import tkinter as tk
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
# Alicia Bentley maps (http://www.atmos.albany.edu/student/abentley/realtime.html)
#  CONUS Bentley maps
ab_con_loc = "http://www.atmos.albany.edu/student/abentley/realtime/images/northamer/"
ab_con_6hrprecip_url = ab_con_loc + "6hprecip/6hprecip_57.png"
ab_con_850thetae_url = ab_con_loc + "850_thetae/850_thetae_57.png"
ab_con_capeshear_url = ab_con_loc + "cape_shear/cape_shear_57.png"
ab_con_mslp_jets_url = ab_con_loc + "mslp_jet/mslp_jet_57.png"
#  Pacific Bentley maps
ab_pac_loc = "http://www.atmos.albany.edu/student/abentley/realtime/images/pacific/"
ab_pac_mslp_anom_url = ab_pac_loc + "mslp_anom/mslp_anom_57.png"
ab_pac_6hrprecip_url = ab_pac_loc + "6hprecip/6hprecip_57.png"
ab_pac_850thetae_url = ab_pac_loc + "850_thetae/850_thetae_57.png"
ab_pac_700wnd_pw_url = ab_pac_loc + "700wind_pw/700wind_pw_57.png"
# Coastal Data Information Program swell map
cdip_swell_url = "http://cdip.ucsd.edu/recent/model_images/monterey.png"
# NWS meteograms (home and place of interest)
home_meteogram_url = "https://forecast.weather.gov/meteograms/Plotter.php?lat=36.6285&lon=-121.9352&wfo=MTR&zcode=CAZ530&gset=18&gdiff=3&unit=0&tinfo=PY8&ahour=0&pcmd=11011111111110000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=&bw=&hrspan=48&pqpfhr=6&psnwhr=6"
poi_meteogram_url  = "https://forecast.weather.gov/meteograms/Plotter.php?lat=46.781&lon=-92.118&wfo=DLH&zcode=MNZ037&gset=15&gdiff=3&unit=0&tinfo=CY6&ahour=0&pcmd=11011111111110000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=&bw=&hrspan=48&pqpfhr=6&psnwhr=6"

# Local directory for downloaded images
img_dir = config.locs.image_dir
# Each image data (source url, local dir+filename)
pw_conus_maxtemp = ( pw_conus_maxtemp_url, img_dir+"pw_conus_maxtemp.png" )
pw_conus_mintemp = ( pw_conus_mintemp_url, img_dir+"pw_conus_mintemp.png" )
pw_conus_24hrqpf = ( pw_conus_24hrqpf_url, img_dir+"pw_conus_24hrqpf.png" )
pw_conus_24hsnow = ( pw_conus_24hsnow_url, img_dir+"pw_conus_24hsnow.png" )
ab_con_6hrprecip = ( ab_con_6hrprecip_url, img_dir+"ab_con_6hrprecip.png" )
ab_con_850thetae = ( ab_con_850thetae_url, img_dir+"ab_con_850thetae.png" )
ab_con_capeshear = ( ab_con_capeshear_url, img_dir+"ab_con_capeshear.png" )
ab_con_mslp_jets = ( ab_con_mslp_jets_url, img_dir+"ab_con_mslp_jets.png" )
ab_pac_mslp_anom = ( ab_pac_mslp_anom_url, img_dir+"ab_pac_mslp_anom.png" )
ab_pac_6hrprecip = ( ab_pac_6hrprecip_url, img_dir+"ab_pac_6hrprecip.png" )
ab_pac_850thetae = ( ab_pac_850thetae_url, img_dir+"ab_pac_850thetae.png" )
ab_pac_700wnd_pw = ( ab_pac_700wnd_pw_url, img_dir+"ab_pac_700wnd_pw.png" )
cdip_swell       = ( cdip_swell_url,       img_dir+"cdip_swell.png"       )
home_meteogram   = ( home_meteogram_url,   img_dir+"home_meteogram.png"   )
poi_meteogram    = ( poi_meteogram_url,    img_dir+"poi_meteogram.png"    )

# All image data
images = ( pw_conus_maxtemp, pw_conus_mintemp, pw_conus_24hrqpf,
           pw_conus_24hsnow, ab_con_6hrprecip, ab_con_850thetae,
           ab_con_capeshear, ab_con_mslp_jets, ab_pac_mslp_anom, 
           ab_pac_6hrprecip, ab_pac_850thetae, ab_pac_700wnd_pw,
           cdip_swell, home_meteogram, poi_meteogram  )


def get_img( url, filename ):
    try:
        r = requests.get( url, stream = True )
    except:
        return
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print(url)
        raise RuntimeWarning("Couldn't download image!")


def crop_bentleys( path, debug=False ):
    # Opens a image in RGB mode
    im = Image.open(path)
    # Crop specs for removing unnecessary vars from plot
    im1 = im.crop((100, 0, 1060, 791))
    # Debug mode for checking crop specs
    if debug:
        # Shows the image in image viewer
        im1.show()
    else:
        # Overwrite previous image
        im1.save(path)
    
def crop_meteogram( path=home_meteogram[1], debug=False ):
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
    # Retrieves all listed images
    for img in images:
        get_img( img[0], img[1] )
    # Crop images what need croppin
    crop_meteogram( home_meteogram[1] )
    crop_meteogram( poi_meteogram[1]  )
    for img in images[4:12]:
        crop_bentleys( img[1] )
        
# def show_img( path, xx=0, yy=0 ):
#     # Create a photoimage object of the image in the path
#     image = Image.open(path)
#     test = ImageTk.PhotoImage(image)
    
#     label = tk.Label(image=test)
#     label.image = test
    
#     # Position image
#     label.place(anchor='center', relx=xx, rely=yy)
#     #label.pack()


if __name__ == "__main__":
    #get_img( pw_conus_maxtemp[0], img_dir+"test.png" )
    #crop_meteogram( debug=False )
    #get_gif()
    crop_bentleys( ab_pac_mslp_anom[1], debug=True )