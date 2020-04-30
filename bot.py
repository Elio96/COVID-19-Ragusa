import requests

def sendPhoto(token, channel, cap):
    files = {'photo': open('COVID-19_Ragusa.png', 'rb')}
    params = {'chat_id': channel, 'caption': cap}
    r= requests.post("https://api.telegram.org/bot" + token + '/sendPhoto', files=files, data=params)
    print(r.status_code, r.reason, r.content)
