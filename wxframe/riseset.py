"""

Retrieve sunrise/sunset data from web

## Takes too long, should replace with requests-based functions

"""

from selenium import webdriver

driverpath = "<path to geckodriver>"


def open_webdriver( ):
    options = webdriver.firefox.options.Options()
    options.add_argument('--headless')
    return webdriver.Firefox(executable_path=driverpath, options=options)


def get_riseset( ):
    try:
        #
        driver = open_webdriver()
        driver.get("https://sunrise-sunset.org/us/pacific-grove-ca")
    
        #
        today = driver.find_element_by_id('today')
        sunrise = today.find_element_by_class_name('sunrise').find_element_by_class_name('time')
        sunrise_str = "0"+sunrise.text[:4]
    
        #
        sunset  = today.find_element_by_class_name('sunset').find_element_by_class_name('time')
        sunset_str = sunset.text[:4]
        sunset_str = str(int(sunset.text[:1])+12)+sunset.text[1:4]
        
        driver.close()
        
        return sunrise_str, sunset_str
    except:
        return "NaN", "NaN"


    
if __name__ == "__main__":
    print( get_riseset() )