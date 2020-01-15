from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
from os import system

latitude = '-23.513084722626527'
longitude = '-47.59298163469899'
api_key = '55d54b1934ab95c1b15b877dfa724442'
cmd_on = '/usr/bin/sqlite3 /home/pi/domoticz/domoticz.db  "update timers set active = 1 where id = 3;"'
cmd_off = '/usr/bin/sqlite3 /home/pi/domoticz/domoticz.db  "update timers set active = 0 where id = 3;"'

client = DarkSkyClient(api_key, (latitude,longitude), units='ca', exclude=['minutely','hourly'], lang='en')

current_weather = client.get_current()

if current_weather.temperature > 28:
    print('cmd off - temperature')
    system(cmd_off)
elif current_weather.cloudCover < 0.55:
    print('cmd_off - cloud cover')
    system(cmd_off)
else:
    print('cmd on - else')
    system(cmd_on)

