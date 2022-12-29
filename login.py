import ks_api_client
from ks_api_client import ks_api
import urllib3
urllib3.disable_warnings()
from time import time, sleep

import requests
from requests.exceptions import HTTPError
import base64
import socketio
import json
import threading


def kotak_login():
    access_token="e6586cb7-faf4-3c0b-9cd5-7589d65e65da"
    userid="SR23021988"
    consumer_key="2ERqlgIlO7mZhYGGLz8l8EPdY_ca"
    consumer_secret="ZJj4e2qo7YN4FfMEm6BGNq8f7Aoa"
    app_id="test"
    password = "Trade@1988"
    pw="DGBD1880"
    accesscode= "8380"


    client = ks_api.KSTradeApi(access_token = access_token, userid = userid, consumer_key = consumer_key,ip = "127.0.0.1", app_id = app_id, host = "https://tradeapi.kotaksecurities.com/apim")#, consumer_secret = consumer_secret)
    client.login(password = password)
    client.session_2fa(access_code = accesscode)



    #websocket
    AUTH ="2ERqlgIlO7mZhYGGLz8l8EPdY_ca:ZJj4e2qo7YN4FfMEm6BGNq8f7Aoa"
    token_api = "https://wstreamer.kotaksecurities.com/feed/auth/token" 

    AUTH_BASE64 = base64.b64encode(AUTH.encode("UTF-8"))
    # print(AUTH_BASE64)
    PAYLOAD = {"authentication":AUTH_BASE64.decode("UTF-8")}
    # print(PAYLOAD)
    response = requests.post(url=token_api, data =PAYLOAD)
    # print(response)
    jsonResponse=response.json()
    # print(jsonResponse)



    try:
        AUTH_BASE64 = base64.b64encode(AUTH.encode("UTF-8"))
    #     print(AUTH_BASE64)
        PAYLOAD = {"authentication":AUTH_BASE64.decode("UTF-8")}
    #     print(PAYLOAD)
        response = requests.post(url=token_api, data =PAYLOAD)
    #     print(response)
        jsonResponse=response.json()
    #     print(jsonResponse)

        if jsonResponse['result']['token'] is None:
            print('Token not found')
        else:
            sio = socketio.Client(reconnection = True, request_timeout=20,reconnection_attempts=5, engineio_logger=True, logger=True)

            def setInterval(func, time):
                e=threading.Event()
                while not e.wait(time):
                    func()

            def foo():  
                sio.emit('handshake',{'inputtoken':'Hello world'})


            @sio.event
            def conncect():
                print('connection success')
                sio.emit('pageload',{'inputtoken':'1900'})
                # sio.emit('pageload',{'inputtoken':'110,1900,9516,43865,891,607,717,411,720,904,727,2574,9907,759,1811,96,734,7667,775,421,9410,21935,815,7567,38,815,847,850,436'})
                #sio.emit('pageload',{'inputtoken':'{0},{1}'.format(token1, token2)})
                setInterval(foo,5)

            @sio.event
            def disconnect():
                print('disconnection closed')

            @sio.on('message')
            def on_message(msg):
                print('message',msg)

            @sio.on('getdata')
            def on_getdata(data):
                
                print('price',data)


            sio.connect('https://wstreamer.kotaksecurities.com',headers={'Authorization':'bearer '+jsonResponse['result']['token']},transports=['websocket'],socketio_path='/feed/fast')
            sio.wait()

    except HTTPError as h:
        print(f'HTTP error occurred :{h}')
    except Exception as e:
        print(f'Error occurred :{e}')




if __name__ == "__main__":
    kotak_login()

# Equity: https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_DD_MM_YYYY.txt
# Derivatives: https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_DD_MM_YYYY.txt