"""

Retrieve images from the web

"""

import shutil
import requests
from tools.system_tools import img_dir
from PIL import Image, ImageTk, ImageGrab

#####################################
#                                   #
#   Saved URLs for updating plots   #
#                                   #
#####################################

# Pivotal Weather daily CONUS weather forecast images
ndfd_loc = "https://x-hv1.pivotalweather.com/maps/ndfd/latest/"
pw_conus_maxtemp_url = ndfd_loc + "ndfd_sfctmax.conus.png"
pw_conus_mintemp_url = ndfd_loc + "ndfd_sfctmin.conus.png"
pw_conus_24hrqpf_url = ndfd_loc + "ndfd_24hqpf.conus.png"
pw_conus_24hsnow_url = ndfd_loc + "ndfd_24hsnow.conus.png"
pw_conus_24hgust_url = ndfd_loc + "ndfd_24hgust.conus.png"
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
# Surfline coastal data
surfline_sst_url = "https://slcharts01.cdn-surfline.com/charts/cencal/monterey/nearshoresst/monterey_large_1_F.png"
surfline_wnd_url = "https://slcharts01.cdn-surfline.com/charts/cencal/monterey/nearshorewinds/monterey_large_1.png"
# NWS fire maps
nws_fire_outlook_url = "https://www.spc.noaa.gov/products/fire_wx/day1otlk_fire.gif"
nifc_fire_month_url  = "https://www.predictiveservices.nifc.gov/outlooks/month1_outlook.png"

# Local directory for downloaded images
# img_dir = config.locs.image_dir
# Each image data (source url, local dir+filename)
pw_conus_maxtemp = ( pw_conus_maxtemp_url, img_dir+"pw_conus_maxtemp.png" )
pw_conus_mintemp = ( pw_conus_mintemp_url, img_dir+"pw_conus_mintemp.png" )
pw_conus_24hrqpf = ( pw_conus_24hrqpf_url, img_dir+"pw_conus_24hrqpf.png" )
pw_conus_24hsnow = ( pw_conus_24hsnow_url, img_dir+"pw_conus_24hsnow.png" )
pw_conus_24hgust = ( pw_conus_24hgust_url, img_dir+"pw_conus_24hgust.png" )
ab_con_6hrprecip = ( ab_con_6hrprecip_url, img_dir+"ab_con_6hrprecip.png" )
ab_con_850thetae = ( ab_con_850thetae_url, img_dir+"ab_con_850thetae.png" )
ab_con_capeshear = ( ab_con_capeshear_url, img_dir+"ab_con_capeshear.png" )
ab_con_mslp_jets = ( ab_con_mslp_jets_url, img_dir+"ab_con_mslp_jets.png" )
ab_pac_mslp_anom = ( ab_pac_mslp_anom_url, img_dir+"ab_pac_mslp_anom.png" )
ab_pac_6hrprecip = ( ab_pac_6hrprecip_url, img_dir+"ab_pac_6hrprecip.png" )
ab_pac_850thetae = ( ab_pac_850thetae_url, img_dir+"ab_pac_850thetae.png" )
ab_pac_700wnd_pw = ( ab_pac_700wnd_pw_url, img_dir+"ab_pac_700wnd_pw.png" )
cdip_swell       = ( cdip_swell_url,       img_dir+"cdip_swell.png"       )
surfline_sst     = ( surfline_sst_url,     img_dir+"surfline_sst.png"     )
surfline_wnd     = ( surfline_wnd_url,     img_dir+"surfline_wnd.png"     )
nws_fire_outlook = ( nws_fire_outlook_url, img_dir+"nws_fire_outlook.png" )
nifc_fire_month  = ( nifc_fire_month_url,  img_dir+"nifc_fire_month.png"  )

# All image data
images = ( pw_conus_maxtemp, pw_conus_mintemp, pw_conus_24hrqpf,
           pw_conus_24hgust, ab_con_6hrprecip, ab_con_850thetae,
           ab_con_capeshear, ab_con_mslp_jets, ab_pac_mslp_anom,
           ab_pac_6hrprecip, ab_pac_850thetae, ab_pac_700wnd_pw,
           cdip_swell, surfline_sst, surfline_wnd, nws_fire_outlook,
           nifc_fire_month )


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
        
def get_imgs( ):
    # Retrieves all listed images
    for img in images:
        get_img( img[0], img[1] )
    for img in images[4:12]:
        crop_bentleys( img[1] )

def get_pws( ):
    for img in images[:4]:
        get_img( img[0], img[1] )

def get_bentleys( ):
    for img in images[4:12]:
        get_img( img[0], img[1] )
        crop_bentleys( img[1] )

def get_marine( ):
    for img in images[12:15]:
        get_img( img[0], img[1] )


if __name__ == "__main__":
    #get_img( pw_conus_maxtemp[0], img_dir+"test.png" )
    get_imgs()
