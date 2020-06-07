# encoding utf-8
import os, sys
import json
import requests
from dotenv import load_dotenv
import geocoder
import datetime as dt

load_dotenv(".env")
api_key = os.environ.get("OPEN_WEATHER_API_KEY")

def city2latlon(city):
    ret = geocoder.osm(city)
    print(ret.latlng)
    return ret.latlng

def week(city_name = "kyoto"):
    country_name = "japan"
    url = "http://api.openweathermap.org/data/2.5/forecast?q={},{}&APPID={}".format(city_name, country_name, api_key)
    response = requests.get(url)
    data = response.json()

def current_and_forecasts_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&lang={lang}&appid={API_KEY}"
    response = requests.get(url.format(
        lat = lat,
        lon = lon,
        API_KEY = api_key,
        part = "",
        lang = "ja"
    ))
    data = response.json()
    return data


def current_and_forecasts_weather_bycity(city):
    lat, lon = city2latlon(city)
    data = current_and_forecasts_weather(lat, lon)
    return data

def main():
    city = "kyoto"
    data = current_and_forecasts_weather_bycity(city)
    for i in data["hourly"]:
        print(dt.datetime.fromtimestamp(i["dt"]))
        print(i)
        # print(i["weather"])

if __name__ == "__main__":
    # week()
    # current_and_forecasts_weather()
    main()