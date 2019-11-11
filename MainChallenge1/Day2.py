from flask import Flask, request
from datetime import datetime, date
import logging
from typing import List, Tuple, Dict, Optional
import time
import re
import pymysql
import requests
import json
import pprint

import csv

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

username = "pdtpatrick"
password = "u3!WL2uC0dxu"
# in seconds
start_time = 3600 * 48  # 48 hours
# airport code
# airport = "KSEA" # Frankfurt
airport = "EDDF"  # Frankfurt


def read_airport(filename: str) -> Dict[str, str]:
    keys = [
        "id",
        "name",
        "city",
        "country",
        "IATA",
        "ICAO",
        "latitude",
        "longitude",
        "altitude",
        "timezone",
        "dst",
        "tz",
        "type",
        "source",
    ]
    airports = csv.DictReader(
        open(filename,encoding="UTF-8"), delimiter=",", quotechar='"', fieldnames=keys
    )
    d = {airport["ICAO"]: airport for airport in airports}
    return d


def call_api(airport: str = None) -> Dict[str, str]:
    """Call opensky API and return all departures

    begin = now - days ago
    end = now
    """
    current_time = time.time()
    URL = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={int(current_time) - start_time}&end={int(current_time)}"
    logging.info(f"URL is now: {URL}")
    r = requests.get(URL, auth=(username, password))
    if r.status_code == 404:
        logging.error("Cannot find data")
        return None
    assert len(r.json()) != 0
    return r.json()

def process_coordinates(start_time: int, end_time: int) -> List[Dict[str, str]]:
    """Process Coordinates
    Pull data from opensky api, read the csv and create an output like:

    List[Dict[Dict[str, str]]]

    Meaning, we'll have a List[Airport[Coordinates[longitude, latitude]]]
    """

    # data to be returned
    _data = []

    # Query the api for departure flights
    api_response =  call_api(airport)

    # Read the csv file into dictionary
    csv_data = read_airport('airports.csv')

    # Remove duplicate



    # Get departure and arrival airport

    for departure in api_response:

        departure_airport = departure['estDepartureAirport']
        arrival_airport = departure['estArrivalAirport']

        try:

           # get the latitude and longitude of departure
            lat_dep = csv_data[departure_airport]['latitude']
            lon_dep = csv_data[departure_airport]['longitude']



             # get the latitude and longitude of arrival
            lat_arr = csv_data[arrival_airport]['latitude']
            lon_arr = csv_data[arrival_airport]['longitude']
        except:
            continue
        #return lat_arr
        #return str(_data)
        # Check for duplicates before appending
        _data.append([{departure_airport: [lon_dep, lat_dep]},{arrival_airport: [lon_arr, lat_arr]}])
    #return json.dumps(_data)

    _new_data = set()
    for i in _data:
        _new_data.add(str(i))


    return str(_new_data)
    pass


def process_flights(start_time: int, end_time: int) -> List[Dict[str, str]]:
    """Process flight information

    Call the opensky api; this will return List[Dict[str, sr]]
    
    Remember our final output, we want to return:
    List[Dict[str, str]]

    In the Dict, we'll have departure, arrival. So something like:
    Dict[departure, arrival]

    The shouldn't be duplicates in your json returned. 
    """


    # data to be returned
    _data = []

    # Query the api for departure flights
    api_response =  call_api(airport)

    # Read the csv file into dictionary
    csv_data = read_airport('airports.csv')


    # Get departure and arrival airport

    for departure in api_response:
        departure_airport = departure['estDepartureAirport']
        destination_airport = departure['estArrivalAirport']


        # Formulate the return data and append
        _data.append({"departure airport":departure_airport,"arrival airport":destination_airport})



    # Return the data
    return json.dumps(_data)

    pass

@app.route('/')
def index() -> str:
    """use this as a test to show your app works"""
    return f"Hello world!"


@app.route('/flights')
def flights() -> str:
    """API for flight information

    your API will receive `start_time` and `end_time`
    Your API will return a json in the form of
    [
        {departure_airport: destination_airport},
        {departure_airport: destination_airport}
    ]

    Remember to add some logging so it is easy for you
    to troubleshoot. 

    Once you have your initial version, think about how you can
    scale your API. Also think about how you can speed it up
    """
    start_time = None
    end_time = None
    return process_flights(start_time, end_time)


@app.route('/coordinates')
def coordinates() -> str:
    """API for coordinate information

    your API will receive `start_time` and `end_time`
    Your API will return a json in the form of
    [
        {departure_airport: 
            {
                "longitude": long,
                "latitude": lat
            }
        },
        {departure_airport: 
            {
                "longitude": long,
                "latitude": lat
            }
        },
    ]

    Remember to add some logging so it is easy for you
    to troubleshoot. 

    Once you have your initial version, think about how you can
    scale your API. Also think about how you can speed it up
    """
    start_time = None
    end_time = None
    return process_coordinates(start_time, end_time)

if __name__ == "__main__":
    app.run(debug=True)