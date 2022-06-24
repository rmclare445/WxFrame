'''

Read timeseries data and plot temperature, showing when furnace is on

'''

import os, platform, datetime
import numpy as np
import matplotlib.pyplot as plt

# Dumb hack -- get rid of ASAP
sep = "\\" if platform.system() == 'Windows' else "/"
repo = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
img_dir = repo + sep + "img" + sep
upd_dir = repo + sep + "upd" + sep


def read_data( line ):
    data = line.replace("\n","").replace(" ","").split(",")
    dd = {}
    date = data[0]
    time = data[1]
    hr, mn, sc = int(time[:2]), int(time[3:5]), int(time[6:])
    if sc >= 30:
        mn+=1
    if mn == 60:
        mn = 0
        hr+=1
    if hr == 24:
        hr = 0
    date = date + " %02d:%02d" % (hr, mn)
    time = "%02d:%02d" % (hr, mn)
    dd['time'] = time
    dd['date'] = datetime.datetime.strptime(date, "%Y%m%d %H:%M")
    dd['temp'] = float(data[2])
    humd = int(data[3])
    dtmp = ( (dd['temp']-32)/1.8 - ((100 - (humd))/5.) ) * 1.8 + 32
    dd['humd'] = humd
    dd['dtmp'] = dtmp
    dd['stat'] = data[4] == "T"
    dd['ttmp'] = data[5]
    return dd


def get_series( path=upd_dir+"log.indoor" ):
    with open(path, "r") as f:
        content = f.readlines()
    nlines = len(content)
    dates, times, temps, humds, dtmps, stats, ttmps = [], [], [], [], [], [], []
    for line in content:
        data = read_data( line )
        dates.append(data['date'])
        times.append(data['time'])
        temps.append(data['temp'])
        humds.append(data['humd'])
        dtmps.append(data['dtmp'])
        stats.append(data['stat'])
        ttmps.append(data['ttmp'])
    return { 'dates':dates, 'times':times, 'temps':temps, 'humds':humds,
             'dtmps':dtmps, 'stats':stats, 'ttmps':ttmps }


def plot_series( data_dict=get_series() ):

    plt.style.use('dark_background')

    fig, axs = plt.subplots(1, 1, figsize=(24,5), dpi=100)
    fig.subplots_adjust(hspace=0)
    axs.set_title('House Temperature and Dew Point', loc='left', fontweight='bold')

    time = data_dict['times']
    stat = data_dict['stats']
    ttmp = data_dict['ttmps']
    # Create discontinuities in target temp
    ttmp = [float('nan') if ttmp[i] != ttmp[i+1] else int(ttmp[i]) for i in range(len(ttmp)-1)]

    # Find first zero or half hour for labeling
    for i, t in enumerate(time):
        if t[-2:] == "00" or t[-2:] == "30":
            hr1 = i
            break

    # Plot indoor temperature
    axs.plot( range(len(time))  , data_dict['temps'], 'r-'            )
    # Plot dew point
    axs.plot( range(len(time))  , data_dict['dtmps'], 'yellowgreen'   )
    # Plot target temperature set in thermopi namelist
    axs.plot( range(len(time)-1), ttmp,               'c--', alpha=0.75 )
    axs.grid(True, linewidth=.25)

    # Labels every half hour
    axs.xaxis.set_ticks( range(len(time))[i::30] )
    axs.set_xticklabels(time[i::30], rotation=30, fontsize=9)

    axs.set_ylim((53, 77))
    axs.yaxis.set_ticks(range(55, 76)[::5])

    # Plot vertical fill to show when furnace is on
    heat = False
    for i, s in enumerate( stat ):
        if s and not heat:
            n1 = i
            heat = True
        elif not s and heat:
            axs.axvspan(n1, i, alpha=0.5, color="purple")
            heat = False

    plt.savefig(img_dir+"thermoplot.png")


if __name__ == "__main__":
    #plot_series( get_series(upd_dir+"log.test") )
    plot_series( )
