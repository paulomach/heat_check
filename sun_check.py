from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
from os import system
import requests


latitude = '-23.513084722626527'
longitude = '-47.59298163469899'
api_key = '55d54b1934ab95c1b15b877dfa724442'

def now():
    from datetime import datetime
    return(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

client = DarkSkyClient(api_key, (latitude,longitude), units='ca', exclude=['minutely','hourly'], lang='en')

current_weather = client.get_current()
temp = current_weather.temperature
cover = current_weather.cloudCover

if temp > 28:
    log_str = '- Timer Off -'
    cmd = 'disabletimer'
elif cover < 0.55:
    log_str = '- Timer Off -'
    cmd = 'disabletimer'
else:
    log_str = '- Timer On -'
    cmd = 'enabletimer'

log_str = now() + log_str + ' Temp: ' + str(temp) + ' - Cover: ' + str(cover)

headers={'Authorization': 'Basic cGF1bG86b3JsYW5kbzQ='}
requests.get(url='http://192.168.15.11:8080/json.htm?type=command&param=' + cmd + '&idx=3' , headers=headers)

system('echo ' + log_str + ' >> /var/log/sun_check.log')
