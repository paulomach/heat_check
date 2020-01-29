def now():
    from datetime import datetime
    return (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def getWeather(latitude, longitude, api_key):
    from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
    client = DarkSkyClient(api_key, (latitude, longitude), units='ca', exclude=['minutely', 'hourly'], lang='en')
    current_weather = client.get_current()
    return current_weather.temperature, current_weather.cloudCover


def processWeather(temp, cover):
    if cover >= 0.9 or temp < 18.0:
        cmd = 'enabletimer'
    elif temp <= 27.0:
        if cover < 0.5:
            cmd = 'disabletimer'
        else:
            cmd = 'enabletimer'
    elif temp > 27.0:
        cmd = 'disabletimer'
    else:
        cmd = 'enabletimer'
    return cmd


def logCommand(cmd, temp, cover):
    from os import system
    log_str = ' - Timer On  -' if cmd == 'enabletimer' else ' - Timer Off -'
    log_str = now() + log_str + ' Temp: ' + str(temp) + 'C' + ' - Cloud Cover: ' + str(100 * cover) + '%'
    system('echo ' + log_str + ' >> /var/log/sun_check.log')
    print(log_str)


def processCommand(cmd, baseUrl, authKey):
    import requests
    headers = {'Authorization': authKey}
    requests.get(url=baseUrl + '/json.htm?type=command&param=' + cmd + '&idx=3', headers=headers)


if __name__ == '__main__':
    import json

    with open('config.json', 'r') as config:
        data = json.load(config)

    temp, cover = getWeather(latitude=data.get('weather').get('lat'),
                             longitude=data.get('weather').get('long'),
                             api_key=data.get('weather').get('key'))
    cmd = processWeather(temp, cover)
    processCommand(cmd=cmd,
                   baseUrl=data.get('controller').get('baseUrl'),
                   authKey=data.get('controller').get('authKey'))
    logCommand(cmd, temp, cover)
