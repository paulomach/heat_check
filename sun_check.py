def now():
    from datetime import datetime
    return (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def getWeather():
    latitude = '-23.513084722626527'
    longitude = '-47.59298163469899'
    api_key = '55d54b1934ab95c1b15b877dfa724442'
    from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
    client = DarkSkyClient(api_key, (latitude, longitude), units='ca', exclude=['minutely', 'hourly'], lang='en')
    current_weather = client.get_current()
    return current_weather.temperature, current_weather.cloudCover


def processWeather(temp, cover):
    if cover >= 0.9:
        cmd = 'enabletimer'
    elif temp <= 27:
        if cover < 0.5:
            cmd = 'disabletimer'
        else:
            cmd = 'enabletimer'
    elif temp > 27:
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


def processCommand(cmd):
    import requests
    headers = {'Authorization': 'Basic cGF1bG86b3JsYW5kbzQ='}
    requests.get(url='http://192.168.15.11:8080/json.htm?type=command&param=' + cmd + '&idx=3', headers=headers)


if __name__ == '__main__':
    temp, cover = getWeather()
    cmd = processWeather(temp, cover)
    processCommand(cmd)
    logCommand(cmd, temp, cover)
