import requests
from datetime import datetime, timezone, timedelta

def lineSendText(message,token):
    payload = {'message' : message}
    r = requests.post('https://notify-api.line.me/api/notify'
        , headers={'Authorization' : 'Bearer {}'.format(token)}
        , params = payload)
    return r.status_code
    
def lineSendSticker(stickerpack_id, sticker_id,token, message=' '):
    # sticker code https://developers.line.biz/en/docs/messaging-api/sticker-list/
    payload = {'message' : message,
            'stickerPackageId' : stickerpack_id,
            'stickerId' : sticker_id}
    r = requests.post('https://notify-api.line.me/api/notify'
        , headers={'Authorization' : 'Bearer {}'.format(token)}
        , params = payload)
    return r.status_code

def datetimeUtcNow():
    return datetime.utcnow()

def nameOfWeek():
    # return Monday,tuesday,Wednesday,Thursday,Friday,...
    return datetimeUtcNow().strftime('%A')