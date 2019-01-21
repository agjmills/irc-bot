# -*- coding: utf8 -*-
import requests
import yaml
from pathlib import Path

configuration = {}

def on_message(bot, channel, sender, message):
    configuration = configure()
    if message.split()[0] == ".weather":
        bot.send_message(channel, get_weather(bot, configuration, message))
    if message.split()[0] == ".forecast":
        bot.send_message(channel, get_forecast(bot, configuration, message))

def configure():
    path = Path().absolute()
    with open(str(path) + "/conf.yml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            print(exception)
            return {}
        
def get_weather(bot, configuration, message):
    if len(message.split()) > 1:
        weather_data = requests.get("http://api.apixu.com/v1/current.json",params={"key":configuration["weather_api_key"],"q":message.split(" ", 1)[1]}).json()
        if not 'error' in weather_data:
            weather_string = "\"{}\" and the temperature is {}°C ({}°F)".format(weather_data["current"]["condition"]["text"],weather_data["current"]["temp_c"], weather_data["current"]["temp_f"])
            location_string = "{}, {}, {}".format(weather_data["location"]["name"],weather_data["location"]["region"],weather_data["location"]["country"])
            return "The weather in {} is {}.".format(location_string, weather_string)
        else:
            return "{}".format(weather_data["error"]["message"])

def get_forecast(bot, configuration, message):
    if len(message.split()) > 1:
        weather_data = requests.get("http://api.apixu.com/v1/forecast.json",params={"key":configuratino["weather_api_key"],"q":message.split(" ", 1)[1]}).json()
        if not 'error' in weather_data:
            max_temperature = "{}°C ({}°F)".format(weather_data["forecast"]["forecastday"][0]["day"]["maxtemp_c"],weather_data["forecast"]["forecastday"][0]["day"]["maxtemp_f"])
            min_temperature = "{}°C ({}°F)".format(weather_data["forecast"]["forecastday"][0]["day"]["mintemp_c"],weather_data["forecast"]["forecastday"][0]["day"]["mintemp_f"])
            weather_string = "\"{}\" with a maximum temperature of {} and a minimum temperature of {}".format(weather_data["forecast"]["forecastday"][0]["day"]["condition"]["text"], max_temperature, min_temperature)
            location_string = "{}, {}, {}".format(weather_data["location"]["name"],weather_data["location"]["region"],weather_data["location"]["country"])
            return "The 24-hour forecast for {} is {}.".format(location_string, weather_string)
        else:
            return "{}".format(weather_data["error"]["message"])
