import requests
import time

apiAddress ='http://api.openweathermap.org/data/2.5/weather?appid=YOUR_OPEN_WEATHER_MAP_API_KEY&q='

def weatherInfo(cityName):
    apiUrl = apiAddress + cityName
    jsonData = requests.get(apiUrl).json()
    weatherDescription = jsonData['weather'][0]['description']
    kelvinTemperature = jsonData['main']['temp']
    maxKelvinTemperature = jsonData['main']['temp_max']
    minKelvinTemperature = jsonData['main']['temp_min']
    humidtyPercent = jsonData['main']['humidity']
    windKmh = jsonData['wind']['speed']
    minCelciusTemperature = minKelvinTemperature - 273.15
    maxCelciusTemperature = maxKelvinTemperature - 273.15
    celciusTemperature = kelvinTemperature - 273.15
    return weatherDescription,humidtyPercent,windKmh,minCelciusTemperature,maxCelciusTemperature,celciusTemperature,kelvinTemperature


cityName = input('City Name :')
print(weatherInfo(cityName))

#Get your free API key from https://openweathermap.org/api


