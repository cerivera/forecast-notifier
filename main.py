import datetime
import pytz
import os

import click
import requests

import config


# TODO don't hardcode
TZ = pytz.timezone('America/Chicago')

class DarkSkyApi:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def get_forecast(self, coords):
        return requests.get("{}/forecast/{}/{},{}".format(
            self.base_url, self.api_key, *coords)).json()

def get_rainy_days(daily_forecast, probability_threshold):
    return [day for day in daily_forecast
               if day["precipProbability"] >= probability_threshold]

def get_cold_days(daily_forecast, max_temp_threshold):
    return [day for day in daily_forecast
               if day["temperatureMax"] <= max_temp_threshold]

def get_rain_text(rainy_days):
    if len(rainy_days) == 0:
        return "No rainy days"
    else:
        return "Rainy days: [{}]".format(",".join(
            [timestamp_to_day(day["time"]) for day in rainy_days]))

def get_cold_text(cold_days):
    if len(cold_days) == 0:
        return "No cold days"
    else:
        return "Cold days: [{}]".format(",".join(
            [timestamp_to_day(day["time"]) for day in cold_days]))

def timestamp_to_day(ts):
    date = datetime.datetime.fromtimestamp(ts, tz=TZ)
    return date.strftime("%A")


@click.command(
    help="Get the week's forecast.")
@click.option(
    "--lat",
    default=29.562854,
    help="Latitude")
@click.option(
    "--lon",
    default=-98.445958,
    help="Longitude")
@click.option(
    "--rain_prob",
    "-rp",
    default=0.55,
    help="Rain probability threshold used to identify rainy days.")
@click.option(
    "--max_temp",
    "-mt",
    default=55,
    help="Max temperature threshold used to identify cold days.")
def forecast_notifier(lat, lon, rain_prob, max_temp):
    # TODO complain if no dark_sky credentials
    api_client = DarkSkyApi(config.dark_sky_root, config.dark_sky_key)
    response = api_client.get_forecast((lat, lon))

    rainy_days = get_rainy_days(response["daily"]["data"], rain_prob)
    cold_days = get_cold_days(response["daily"]["data"], max_temp)

    print(get_cold_text(cold_days))
    print(get_rain_text(rainy_days))

if __name__ == "__main__":
    forecast_notifier()
