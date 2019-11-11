# Here We Use the existing openSKY API

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

# create new figure, axes instances.

fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])

# setup mercator map projection.

m = Basemap(llcrnrlon=-100., llcrnrlat=20., urcrnrlon=20., urcrnrlat=60.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)

# # nylat, nylon are lat/lon of New York
#
# nylat = 40.78; nylon = -73.98
#
# # lonlat, lonlon are lat/lon of London.
#
# lonlat = 51.53; lonlon = 0.08
#
# # draw great circle route between NY and London
#
# m.drawgreatcircle(nylon, nylat, lonlon, lonlat, linewidth=2, color='b')
# m.drawcoastlines()
# m.fillcontinents()
#
# # draw parallels
#
# m.drawparallels(np.arange(10, 90, 20), labels=[1, 1, 0, 1])
#
# # draw meridians
#
# m.drawmeridians(np.arange(-180, 180, 30), labels=[1, 1, 0, 1])
# ax.set_title('Great Circle from New York to London')
# plt.show()

m = Basemap(llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90, \
            projection='mill', resolution='c')
m.shadedrelief()
plt.show()

# This function plots the flight on map
def show_flight(flight_info):
    m = Basemap(llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90, \
                projection='mill', resolution='c')
    m.shadedrelief()

    plt.show()

    m.drawcoastlines()
    # m.drawcounties(linewidth=2)
    m.drawstates(color='b')

    xs = []
    ys = []

    # Plot arrival points
    NYClat, NYClon = float(flight_info[1][0]), float(flight_info[1][1])
    xpt, ypt = m(NYClon, NYClat)
    xs.append(xpt)
    ys.append(ypt)
    m.plot(xpt, ypt, 'go', markersize=20)

    # Plot departure points
    LAlat, LAlon = float(flight_info[0][0]), float(flight_info[0][1])
    xpt, ypt = m(LAlon, LAlat)
    xs.append(xpt)
    ys.append(ypt)
    m.drawgreatcircle(NYClon, NYClat, LAlon, LAlat, linewidth=2, color='b')
    m.drawcoastlines()
    m.plot(xpt, ypt, 'r^', markersize=20)

    m.plot(xs, ys, color='y', linewidth=3, label='Flight 112')

    # Customization of plotted map and displaying it
    plt.title('Flight Map')
    #plt.show()




##python
import time
import requests
import logging
import pprint
import csv

currentTime = int(time.time())  # currentTime in second
startTime = currentTime - 3600 * 48  # 48h in the past
username = "pdtpatrick"
password = "u3!WL2uC0dxu"


def call_api(airport, startTime, endTime):
    """Call opensky API and return all departures

    begin = now - days ago
    end = now
    """
    time.sleep(10)
    URL = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={startTime}&end={endTime}"
    logging.info(f"URL is now: {URL}")
    r = requests.get(URL, auth=(username, password))
    if r.status_code == 404:
        logging.error("Cannot find data")
        return None
    assert len(r.json()) != 0
    return r.json()


airport_name = "KSEA"

depatures = call_api('KLGA', startTime, currentTime)
print(len(depatures))


def read_airport(filename: str):
    keys = ["id", "name", "city", "country", "IATA", "ICAO",
            "latitude", "longitude", "altitude", "timezone",
            "dst", "tz", "type", "source"]
    airports = [a for a in
                csv.DictReader(open(filename, encoding="utf-8"), delimiter=',', quotechar='"', fieldnames=keys)]

    return airports  # [15:25]


airports = read_airport("airports.csv")

print(f'{airports} \n')
dictionary_ = {}


for i in airports:
    key = i['ICAO']
    dictionary_[key] = [i['latitude'],i['longitude']]


def getLocation(airport):
    return dictionary_[airport]

#print(getLocation("KSEA"))


def flight_information(dep,arr):
    dep_loc = getLocation(dep)
    arr_loc = getLocation(arr)
    temp = []
    temp.append(dep_loc)
    temp.append(arr_loc)
    return temp


for departure in depatures:
    flight_dep = departure['estDepartureAirport']
    flight_arr = departure['estArrivalAirport']
    # print(flight_arr)
    flight_loc = flight_information(flight_dep,flight_arr)
    #print(flight_information(flight_dep,flight_arr))
    show_flight(flight_loc)





# show_flight([[10,20],[30,40]])