import configparser
import datetime
from configparser import ConfigParser
import threading
import json
import socketio
import base64
from requests.exceptions import HTTPError
import requests
from time import time, sleep
import ks_api_client
from ks_api_client import ks_api
import urllib3
urllib3.disable_warnings()
import json
import os


class kotak():
    def __init__(self, event=None) -> None:
        # Configure prase
        self.conf = self.configure_params()
        # Get params

        self.event = event

        # self.kotak_login()

    def configure_params(self,):
        # Change the path accordingly
        try:
            conf = configparser.ConfigParser()
        except:
            conf = ConfigParser.ConfigParser()
        # conf_file=os.path.join(pwd,"src/mo_settings.ini")

        conf.read('/home/vdgs/git/stock_bot/config.ini')
        return conf

    def readConfigParams(self,):

        self.access_token = self.conf.get('credentials', 'access_token')
        self.userid = self.conf.get('credentials', 'userid')
        self.consumer_key = self.conf.get('credentials', 'consumer_key')
        self.consumer_secret = self.conf.get('credentials', 'consumer_secret')
        self.app_id = self.conf.get('credentials', 'app_id')
        self.password = self.conf.get('credentials', 'password')
        self.pw = self.conf.get('credentials', 'pw')
        self.accesscode = self.conf.get('credentials', 'accesscode')
        self.url = self.conf.get('connection', 'url')
        self.auth = self.conf.get('connection', 'auth')
        self.token_api = self.conf.get('connection', 'token_api')
        self.mode = self.conf.get('mode', 'mode')
        self.verbose = self.conf.get('general', 'verbose')

    def updateTokenNames(self,):
        # TODO: add a logic to refresh the token_cmp_names files
        self.cash_url = self.conf.get('connection', 'info_cash')
        self.token_cmp_names = self.conf.get('files', 'token_list')

        date = datetime.datetime.now()

        dd, mm, yyyy = date.strftime("%d"), date.strftime(
            "%m"), date.strftime("%Y")
        # Replace the DD, MM , YYYY by the actual and latest dates
        self.cash_url = self.cash_url.replace("DD", str(dd))
        self.cash_url = self.cash_url.replace("MM", str(mm))
        self.cash_url = self.cash_url.replace("YYYY", str(yyyy))
        print(self.cash_url)
        # download the file
        r = requests.get(self.cash_url, allow_redirects=True)
        open('temp.txt', 'wb').write(r.content)

        # Read the temp.txt
        with open("temp.txt") as file:
            lines = [line.rstrip() for line in file]

        instrumentToken = []
        instrumentName = []
        name = []

        for line in lines[1:]:
            split_line = line.split("|")
            instrumentToken.append(split_line[0])
            instrumentName.append(split_line[1])
            name.append(split_line[2])

        # split using | symbol
        # instrumentToken|instrumentName|name

        data = {
            "instrumentToken": instrumentToken,
            "instrumentName": instrumentName,
            "name": name
        }


        with open(self.token_cmp_names, 'w') as f:
            json.dump(data, f)
        
        
        f.close()
        os.remove("temp.txt")
        
        


        with open(self.token_cmp_names, 'r') as f:
            data_test = json.load(f)
        
        print(data_test['instrumentToken'][0], data_test['instrumentName'][0], data_test['name'][0])

    def kotak_login(self,):

        self.client = ks_api.KSTradeApi(access_token=self.access_token, userid=self.userid, consumer_key=self.consumer_key, ip="127.0.0.1",
                                        app_id=self.app_id, host="https://tradeapi.kotaksecurities.com/apim")  # , consumer_secret = consumer_secret)
        self.client.login(password=self.password)
        # Exception has occurred: ApiException
        self.client.session_2fa(access_code=self.accesscode)

        ## Test ##
        print(self.client.quote(instrument_token=110))
        url = 'https://tradeapi.kotaksecurities.com/apim/scripmaster/1.1/filename'
        headers = {'accept': 'application/json', 'consumerkey': f"{self.consumer_key}",
                   "Authorization": f"Bearer {self.access_token}"}
        res = requests.get(url, headers=headers).json()
        print(res)
        ## Test ##

        # websocket
        self.AUTH = "2ERqlgIlO7mZhYGGLz8l8EPdY_ca:ZJj4e2qo7YN4FfMEm6BGNq8f7Aoa"
        self.token_api = "https://wstreamer.kotaksecurities.com/feed/auth/token"

        self.AUTH_BASE64 = base64.b64encode(self.AUTH.encode("UTF-8"))
        # print(AUTH_BASE64)
        self.PAYLOAD = {"authentication": self.AUTH_BASE64.decode("UTF-8")}
        # print(PAYLOAD)
        response = requests.post(url=self.token_api, data=self.PAYLOAD)
        # print(response)
        jsonResponse = response.json()
        # print(jsonResponse)

        try:
            self.AUTH_BASE64 = base64.b64encode(self.AUTH.encode("UTF-8"))
        #     print(AUTH_BASE64)
            self.PAYLOAD = {"authentication": self.AUTH_BASE64.decode("UTF-8")}
        #     print(PAYLOAD)
            response = requests.post(url=self.token_api, data=self.PAYLOAD)
        #     print(response)
            jsonResponse = response.json()
        #     print(jsonResponse)

            if jsonResponse['result']['token'] is None:
                print('Token not found')
            else:
                # self.event.set()
                sio = socketio.Client(reconnection=True, request_timeout=20,
                                      reconnection_attempts=5, engineio_logger=True, logger=True)

                def setInterval(func, time):
                    e = threading.Event()
                    while not e.wait(time):
                        func()

                def foo():
                    sio.emit('handshake', {'inputtoken': 'Helo world'})

                @sio.event
                def conncect():
                    print('connection success')
                    sio.emit('pageload', {'inputtoken': '3928'})
                    # sio.emit('pafeload',{'inputtoken':'110,1900,9516,43865,891,607,717,411,720,904,727,2574,9907,759,1811,96,734,7667,775,421,9410,21935,815,7567,38,815,847,850,436'})

                    # sio.emit('pageload',{'inputtoken':'{0},{1}'.format(token1, token2)})
                    setInterval(foo, 5)

                @sio.event
                def disconnect():
                    print('disconnection closed')

                @sio.on('message')
                def on_message(msg):
                    print('message', msg)

                @sio.on('getdata')
                def on_getdata(data):
                    # self.event.set()
                    print('price', data)

                sio.connect('https://wstreamer.kotaksecurities.com', headers={
                            'Authorization': 'Bearer '+jsonResponse['result']['token']}, transports=['websocket'], socketio_path='/feed/fast')
                sio.wait()

        except HTTPError as h:
            print(f'HTTP error occurred :{h}')
        except Exception as e:
            print(f'Error occurred :{e}')


if __name__ == "__main__":
    k = kotak()
    k.updateTokenNames()
    k.kotak_login()
