def now():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_weather():
    latitude = '-23.513084722626527'
    longitude = '-47.59298163469899'
    api_key = '55d54b1934ab95c1b15b877dfa724442'
    from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
    client = DarkSkyClient(api_key, (latitude, longitude), units='ca',
                           exclude=['minutely', 'hourly'], lang='en')
    current_weather = client.get_current()
    return current_weather.temperature, current_weather.cloudCover


def process_weather(temperature, cloud_cover):
    if (cloud_cover >= 0.9 and temperature < 28.0) or temperature < 20.0:
        command = 'enabletimer'
    elif temperature < 22 and cloud_cover > 25:
        command = 'enabletimer'
    elif temperature <= 27.0:
        if cloud_cover < 0.5:
            command = 'disabletimer'
        else:
            command = 'enabletimer'
    elif temperature > 27.0:
        command = 'disabletimer'
    else:
        command = 'enabletimer'
    return command


def log_command(command, temperature, cloud_cover):
    from os import system
    log_str = ' - Timer On  -' if command == 'enabletimer' else ' - Timer Off -'
    log_str = now() + log_str + ' Temp: ' + str(temperature) + 'C' + ' - Cloud Cover: ' + str(
        100 * cloud_cover) + '%'
    try:
        system('echo ' + log_str + ' >> /var/log/sun_check.log')
    except:
        system('echo ' + log_str + ' >> ./sun_check.log')

    print(log_str)


def process_command(command):
    import requests
    headers = {'Authorization': 'Basic cGF1bG86b3JsYW5kbzQ='}
    requests.get(url='http://192.168.15.11:8080/json.htm?type=command&param=' + command + '&idx=3',
                 headers=headers)


if __name__ == '__main__':
    temp, cover = get_weather()
    cmd = process_weather(temp, cover)
    process_command(cmd)
    log_command(cmd, temp, cover)
