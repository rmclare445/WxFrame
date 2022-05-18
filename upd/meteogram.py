# Will need shebang here
"""

Retrieve most recent NOAA meteogram data for Pacific Grove, plot it

"""

import requests
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

noaa_xml_url = "https://forecast.weather.gov/MapClick.php?lat=36.6175&lon=-121.921&FcstType=digitalDWML"


def retrieve_noaa_xml( url=noaa_xml_url ):
    response = requests.get( url )
    open("noaa_meteo.xml", "wb").write(response.content)
    
    tree = ET.parse("noaa_meteo.xml")
    root = tree.getroot()
    
    init = root.find('head').find('product').find('creation-date').text
    
    time = root.find('data').find('time-layout')
    data = list( root.find('data').find('parameters') )
    
    return { 'init': init,
             'time': [t.text for t in time.findall('start-valid-time')],
             'temp': fix_data( [t.text for t in data[7].findall('value')] ), 
             'dwpt': fix_data( [t.text for t in data[0].findall('value')] ),
             'hidx': fix_data( [t.text for t in data[1].findall('value')] ),
             'wspd': fix_data( [t.text for t in data[2].findall('value')] ),
             'wdir': fix_data( [t.text for t in data[6].findall('value')] ),
             'gust': fix_data( [t.text for t in data[8].findall('value')] ),
             'rhum': fix_data( [t.text for t in data[5].findall('value')] ),
             'prcp': fix_data( [t.text for t in data[4].findall('value')] ),
             'ccvr': fix_data( [t.text for t in data[3].findall('value')] ) }


def fix_data( data ):
    # Parse integer values from NaNs
    for i, value in enumerate(data):
        data[i] = int(value) if value else float('nan')
    return data


def plot_meteogram( data_dict ):
    
    times = data_dict['time']
    time = []
    for t in times:
        hr = int(t[11:13])
        meridiem = 'am' if hr < 12 or hr == 0 else 'pm'
        hr = hr if hr <= 12 else hr-12
        time.append( str(hr)+meridiem )
        
    plt.style.use('dark_background')
    
    fig, axs = plt.subplots(3, 1, figsize=(24,5), dpi=100, sharex=True)
    fig.subplots_adjust(hspace=0)
    axs[0].set_title('Pacific Grove Point Forecast - NOAA', loc='left', fontweight='bold')
    
    # Plot thick lines at midnight
    for i, t in enumerate(time):
        if t == '0am':
            axs[0].plot((i,i), (-100,200), 'w-', linewidth=0.7)
            axs[1].plot((i,i), (-100,200), 'w-', linewidth=0.7)
            axs[2].plot((i,i), (-100,200), 'w-', linewidth=0.7)
            date = times[i][5:7]+"/"+times[i][8:10]
            axs[0].text( i+.75, 72, date, weight='light' )
    
    axs[0].plot(range(len(times)), data_dict['temp'], 'r-', marker='.')
    axs[0].plot(range(len(times)), data_dict['dwpt'], color='yellowgreen', marker='.')
    axs[0].plot(range(len(times)), data_dict['hidx'], color='gold', marker='.')
    start, end = (30, 80)
    axs[0].yaxis.set_ticks(np.arange(start, end, 10))
    axs[0].set_ylim((31, 78))
    axs[0].tick_params(axis="y", direction="in", pad=-22, labelright=True)
    axs[0].grid(True, linewidth=.25)
    
    # Calculate u, v components of wind to render wind barbs
    u = [-abs(data_dict['wspd'][i])*np.sin(np.deg2rad(data_dict['wdir'][i])) for i in range(len(times))]
    v = [-abs(data_dict['wspd'][i])*np.cos(np.deg2rad(data_dict['wdir'][i])) for i in range(len(times))]
    # Add wind barbs
    axs[1].barbs( range(len(times)), data_dict['wspd'], u, v, length=6, linewidth=0.6,
                  sizes=dict(spacing=0.2, height=0.3, width=0.2), zorder=2.5, barbcolor='dodgerblue' )
    axs[1].plot(range(len(times)), data_dict['wspd'], color='plum', marker='.')
    axs[1].plot(range(len(times)), data_dict['gust'], color='fuchsia', marker='.')
    start, end = (-10,40)
    axs[1].yaxis.set_ticks(np.arange(start, end, 10))
    axs[1].set_ylim((-5, 38))
    axs[1].tick_params(axis="y",direction="in", pad=-22, labelright=True)
    axs[1].grid(True, linewidth=.25)

    axs[2].plot(range(len(times)), data_dict['prcp'], color='gold', marker='.')
    axs[2].plot(range(len(times)), data_dict['ccvr'], color='skyblue', marker='.')
    axs[2].plot(range(len(times)), data_dict['rhum'], color='mediumspringgreen', marker='.')
    start, end = (0,120)
    axs[2].yaxis.set_ticks(np.arange(start, end, 20))
    axs[2].set_ylim((-1, 115))
    axs[2].tick_params(axis="y",direction="in", pad=-22, labelright=True)
    axs[2].grid(True, linewidth=.25)
    
    axs[2].xaxis.set_ticks(range(len(time))[::3])
    axs[2].set_xticklabels(time[::3], rotation=30, fontsize=9)
    axs[2].xaxis.set_ticks(range(len(times)))
    axs[2].set_xlim((-3.5, len(times)+2.5))
    
    xpt = 80
    ypt = 81
    axs[0].text( xpt, ypt, 'Temperature', color='r', weight='bold' )
    axs[0].text( xpt+13, ypt, 'Dew Point', color='yellowgreen', weight='bold' )
    axs[0].text( xpt+24, ypt, 'Wind Speed', color='plum', weight='bold' )
    axs[0].text( xpt+36, ypt, 'Gust', color='fuchsia', weight='bold' )
    axs[0].text( xpt+43, ypt, 'Relative Humidity', color='mediumspringgreen', weight='bold' )
    axs[0].text( xpt+60, ypt, 'Sky Cover', color='skyblue', weight='bold' )
    axs[0].text( xpt+71, ypt, 'Chance of Precipitation', color='gold', weight='bold' )
    
    plt.savefig('test_plot.png')

    
if __name__ == "__main__":
    # print( retrieve_noaa_xml() )
    plot_meteogram( retrieve_noaa_xml() )