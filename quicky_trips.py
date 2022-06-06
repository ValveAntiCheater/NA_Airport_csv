# -*- coding: utf-8 -*-
"""quicky_trips.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uraiOio9YDofVQ4UjS4B1aK15Iq1UF2E

START OF ACTUAL STUFF
"""

# !pip install FlightRadarAPI
from math import cos, asin, sqrt, pi
import pandas as pd
import sys
import requests
import json
from FlightRadar24.api import FlightRadar24API
flight = FlightRadar24API()

def distance(lat1, lat2, lon1, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

url = 'https://raw.githubusercontent.com/ValveAntiCheater/NA_Airport_csv/main/Major%20Airports%20-%20NORTH%20AMERICA.csv'
df = pd.read_csv(url)

key = '&key=AIzaSyCnaGh7vSWH2GOJK7xKAIzz6wx-E8q_s1E'
city = 'Austin' #NEED TO GET FROM INPUT
address = 'address='+city
api_base = 'https://maps.googleapis.com/maps/api/geocode/json?'
api_result_maps = requests.get(api_base+address+key)
api_response_maps = api_result_maps.json()
lat = api_response_maps['results'][0]['geometry']['location']['lat']
lng = api_response_maps['results'][0]['geometry']['location']['lng']
latlng = df['Lat, Long']
min = sys.float_info.max
airport_iata = ''
for string in latlng.items():
  lat1 = float(string[1].split(", ")[0])
  lng1 = float(string[1].split(", ")[1])
  if(distance(lat,lng,lat1,lng1) < min):
    airport_iata = df['IATA'][string[0]]
    min = distance(lat,lat1,lng,lng1)

params = {
  'api_key': '035d195b-2a63-4d2e-aa80-2223077e8f6e',
  'dep_iata': airport_iata
}
method = 'schedules'
api_base = 'http://airlabs.co/api/v9/'
api_result_sced = requests.get(api_base+method, params)
api_response_sced = api_result_sced.json()

lst = api_response_sced['response'][:20]
interests = ['sport','natural'] #NEED FROM INPUT
max = 0
max_city = ''
for air in lst:
  air_code = air['arr_iata']
  air_ar = flight.get_airport(air_code)
  air_city = air_ar['position']['region']['city']
  lat_air = air_ar['position']['latitude']
  lng_air = air_ar['position']['longitude']
  api_result_air = requests.get('http://api.opentripmap.com/0.1/en/places/radius?radius=25000&lon='+str(lng_air)+'&lat='+str(lat_air)+'&apikey=5ae2e3f221c38a28845f05b6231b8f0b19665326413cf30cbe082e55')
  api_response_air = api_result_air.json()
  kinds = api_response_air['features']
  count = 0
  for k in kinds:
    attrac = k['properties']['kinds'].split(",")
    for a in attrac:
      if a in interests:
        count += 1
        if(count == len(interests)):
          break
  if(count > max):
    max_city = air_city
print(max_city) #ADD THINGS SUCH AS FLIGHT INFORMATION, WHAT TO DO AT THE CITY, THINGS LIKE THAT, FIGURE OUT HOW TO INTEGRATE INTO FRONTEND