"""

Retrieve buoy data from web

&

Provide table configuration for buoy data

"""

import requests
import tkinter as tk
from tools.text_tools import *

buoy46042_url = "https://www.ndbc.noaa.gov/station_page.php?station=46042&uom=M&tz=STN"
buoy46092_url = "https://www.ndbc.noaa.gov/station_page.php?station=46092&uom=M&tz=STN"
buoys = (buoy46042_url, buoy46092_url)


def get_buoy_table( url ):
    # Open the url
    r = requests.get(url, stream = True )
    # Check if the webpage was retrieved successfully
    if r.status_code == 200:
        content = r.text
        
        # Find significant markers in webpage content, crop, then filter to list
        cut = content.find('Click on the graph icon in the table below to see a time series plot of the last five days of that observation.')
        end = content.find('Combined plot of Wind Speed, Gust, and Air Pressure')
        content = remove_html( content[cut+111:end] ).replace(' ', '').replace('\n', '').split('\t')
        content = list(filter(None, content))
        
        # Separate variable names from observations
        varnames = content[::2]
        varnames = [ rm_parentheses( varnames[i] ) for i in range(len(varnames)) ]
        obs = content[1::2]
        
        return varnames, obs


def populate_obs( vars_column, varsn, obsn ):
    obs_column = ['---' for i in range(len(vars_column))]
    for i in range(len(obsn)):
        for j in range(len(vars_column)):
            if varsn[i] == vars_column[j]:
                obs_column[j] = obsn[i]
                break
    return obs_column


def merge_buoy_data( ):
    '''
    Creates tabular list for buoy vars and data
    '''
    # Retrieve current provided data for both buoys
    vars1, obs1 = get_buoy_table( buoy46042_url )
    vars2, obs2 = get_buoy_table( buoy46092_url )
    # Create column for variables, even if referenced only once
    vars_column = vars1
    for var in vars2:
        if var in vars1:
            pass
        else:
            vars_column.append(var)
    obs1_column = populate_obs(vars_column, vars1, obs1)
    obs2_column = populate_obs(vars_column, vars2, obs2)
    # Populate data table
    data = [ ('NOAA NDBC Readings', 'NDBC 46042', 'MBARI 46092') ]
    for i in range(len(vars_column)):
        data.append( (vars_column[i], obs1_column[i], obs2_column[i]) )
            
    return data


class Table:
    def __init__(self, parent, data=merge_buoy_data()):
        
        # code for creating table
        for i in range(len(data)):
            for j in range(len(data[0])):
                
                if i == 0:
                    rowfont = ('Arial',16,'bold')
                else:
                    rowfont = ('Arial',16)
                    
                colwidth = 20 if j==0 else 15
                    
                self.e = tk.Entry(parent, width=colwidth, fg='blue', bg='gray66',
                                  font=rowfont)
                self.e.grid(row=i, column=j)
                datum = self.fix_data(data[i][j])
                self.e.insert(tk.END, datum)
                
    def fix_data( self, datum ):
        try:
            if '&deg;C' in datum:
                quant = float(datum[:-6]) * (9/5.) + 32.
                return "%0.1f\u00B0F" % quant
            if 'm/s' in datum:
                quant = float(datum[:-3]) * 2.23694
                return "%01d mph (%s)" % (quant, datum)
            return datum
        except:
            return datum
              

class BuoyTable( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__( self, parent )
        self.tab = Table( self )
                

if __name__ == "__main__":
    # root = tk.Tk()
    # t = BuoyTable(root)
    # root.mainloop()
    print(merge_buoy_data())