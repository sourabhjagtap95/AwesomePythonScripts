import json

import requests
from twilio.rest import TwilioRestClient

# Info for Weather Underground API call
STATE = ''
CITY = ''
WU_KEY = ''
# Twilio API Keys
TW_SID = ''
TW_AUTH = ''
# Your Twilio phone number
MY_NUM = ''
# Recepient's phone number
HONEY_NUM = ''


def current():
  api_url = 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(WU_KEY, STATE, CITY)
  request = requests.get(api_url).json()
  current_temp = request['current_observation']['temp_f']
  return current_temp


def forecast():
  api_url = 'http://api.wunderground.com/api/{}/forecast/q/{}/{}.json'.format(WU_KEY, STATE, CITY)
  request = requests.get(api_url).json()
  high = request['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
  low = request['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
  return high, low


def text(current, forecast):
  twilio = TwilioRestClient(TW_SID, TW_AUTH)

  msg = '''
  	Hey honey! Right now, the temperature(F) is {}.\n\n
    Today has a high of {}, and a low of {}.\n\n
  	You can't opt-out of these texts.\n\n
  	See you tomorrow!\n\n
    #HoneyWeather
  	'''.format(current, forecast[0], forecast[1])

  message = twilio.messages.create(body=msg, from_=MY_NUM, to=HONEY_NUM)


if __name__ == '__main__':
  current = current()
  forecast = forecast()
  text(current, forecast)