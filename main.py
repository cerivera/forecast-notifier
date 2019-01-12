import datetime
import os

import click
import requests

import config

class DarkSkyApi:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def get_forecast(self, coords):
        return requests.get("{}/forecast/{}/{},{}".format(
            self.base_url, self.api_key, *coords)).json()

def get_rainy_days(daily_forecast, probability_threshold):
    return len([day for day in daily_forecast
                if day["precipProbability"] > probability_threshold])

@click.command(
    help='Warns you to turn off your sprinklers if rain is forecasted this week')
@click.option(
    '--lat',
    default=29.562854,
    help='Latitude')
@click.option(
    '--lon',
    default=-98.445958,
    help='Longitude')
@click.option(
    '--days_threshold',
    '-dt',
    default=2,
    help='Trigger reminder after this many rainy days forecasted.')
@click.option(
    '--prob_threshold',
    '-pt',
    default=0.6,
    help='Rain probability threshold used to identify rainy days.'
)
def sprinkler_tasker(lat, lon, days_threshold, prob_threshold):
    # TODO complain if no dark_sky credentials
    api_client = DarkSkyApi(config.dark_sky_root, config.dark_sky_key)
    response = api_client.get_forecast((lat, lon))

    num_rainy_days = get_rainy_days(response["daily"]["data"], prob_threshold)

    if num_rainy_days == 0:
        print("No rainy days this week.")
    elif num_rainy_days < days_threshold:
        days_text = "day" if num_rainy_days == 1 else "days"
        print("Only {} rainy {} this week".format(num_rainy_days, days_text))
    else:
        today = datetime.datetime.now()
        next_week = today + datetime.timedelta(days=7)
        # TODO actually push the task somewhere. RTM?
        print("Turn off your sprinklers {}".format(today.strftime("%D")))
        print("Turn on your sprinklers {}".format(next_week.strftime("%D")))


if __name__ == "__main__":
    sprinkler_tasker()
