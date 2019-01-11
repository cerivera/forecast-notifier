import datetime
import os

import requests

import config

class DarkSkyApi:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def get_forecast(self, coords):
        return requests.get("{}/forecast/{}/{},{}".format(
            self.base_url, self.api_key, *coords)).json()

def get_rainy_days(daily_forecast):
    return len([day for day in daily_forecast
                if day["precipProbability"] > 0.6])

if __name__ == "__main__":
    RAINY_DAYS_THRESHOLD = os.getenv('RAINY_DAYS_THRESHOLD', 2)

    api_client = DarkSkyApi(config.dark_sky_root, config.dark_sky_key)

    coords = (29.562854, -98.445958) # TODO Accept as args

    response = api_client.get_forecast(coords)

    num_rainy_days = get_rainy_days(response["daily"]["data"])
    print("{} rainy days this week".format(num_rainy_days))

    if num_rainy_days > RAINY_DAYS_THRESHOLD:
        today = datetime.datetime.now()
        next_week = today + datetime.timedelta(days=7)
        print("Turn off your sprinklers {}".format(today.strftime("%D")))
        print("Turn on your sprinklers {}".format(next_week.strftime("%D")))
