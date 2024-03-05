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
from ks_api_client.exceptions import ApiValueError, ApiException
import urllib3
urllib3.disable_warnings()
import json
import os
import datetime
import concurrent.futures



class kotak():
    def __init__(self, access_code , path_ini=None, event=None, logger =None) -> None:
        if os.path.exists(path_ini):
            self.path_ini = path_ini
        else:
            assert False ,"INI path error"
            
        if logger == None:
            self.logger =True
        else:
            self.logger =logger
            
        self.access_code = access_code
        
        # Configure prase
        self.conf = self.configure_params()
        # Get params
        self.readConfigParams()

        self.event = event
        self.recount =0
        self.count_calls=0
        
        # default values
        self.client = None
        self.tokens = None
        self.thread_loops=0
        
        #Todays date
        date = datetime.datetime.now()

        dd, mm, yyyy = date.strftime("%d"), date.strftime(
            "%m"), date.strftime("%Y")
        self.todays_date = f'{dd}/{mm}/{yyyy}'
        # self.getTokenCmpNames()

    def configure_params(self,):
        # Change the path accordingly
        try:
            conf = configparser.ConfigParser()
        except:
            conf = ConfigParser.ConfigParser()
        # conf_file=os.path.join(pwd,"src/mo_settings.ini")

        conf.read(self.path_ini)
        return conf

    def readConfigParams(self,):

        self.access_token = self.conf.get('credentials', 'access_token')
        self.userid = self.conf.get('credentials', 'userid')
        self.consumer_key = self.conf.get('credentials', 'consumer_key')
        self.consumer_secret = self.conf.get('credentials', 'consumer_secret')
        self.app_id = self.conf.get('credentials', 'app_id')
        self.password = self.conf.get('credentials', 'password')
        self.pw = self.conf.get('credentials', 'pw')
        accesscode = self.conf.get('credentials', 'accesscode')
        if accesscode == '0':
            self.accesscode = str(self.access_code)
        self.url = self.conf.get('connection', 'url')
        self.auth = self.conf.get('connection', 'auth')
        self.token_api = self.conf.get('connection', 'token_api')
        self.ip = self.conf.get('connection', 'ip')
        self.host = self.conf.get('connection', 'host')
        self.cash_url = self.conf.get('connection', 'info_cash')
        self.mode = self.conf.get('mode', 'mode')
        self.verbose = self.conf.getboolean('general', 'verbose')
        self.token_cmp_names = self.conf.get('files', 'token_list')
        self.save_path = self.conf.get('save_path', 'path')
        self.delta = self.conf.getint("general","delta_sec")
        self.check_based_on_trade_date =self.conf.getboolean("general","check_based_on_trade_date")
        self.stop_shell_script_after = self.conf.getint("general","stop_shell_script_after")
        self.threaded_logic = self.conf.getboolean("general","threaded_logic")




    def updateTokenNames(self,):
        # TODO: add a logic to refresh the token_cmp_names files
        

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
        
        

    def getTokenCmpNames(self,):
        if (self.recount>2):
            return False
        else:
            self.recount =self.recount+1
                    
        if os.path.exists(self.token_cmp_names):
            
            with open(self.token_cmp_names, 'r') as f:
                self.tokens = json.load(f)
            
            return True
            
        else:
            
            self.updateTokenNames()
            self.getTokenCmpNames()
        
        
            
    def kotak_login(self,):
        try:
            self.client = ks_api.KSTradeApi(access_token=self.access_token, userid=self.userid, consumer_key=self.consumer_key, ip=self.ip,
                                            app_id=self.app_id, host=self.host, consumer_secret = self.consumer_secret, logger=self.logger)
            self.client.login(password=self.password)
            # Exception has occurred: ApiException
            self.client.session_2fa(access_code=self.accesscode)
            
        except ApiException as e:
            print(e)
            exit()
    

    def validate_quote(self,quote_details):
        now_hh= datetime.datetime.now().strftime('%H')
        close_it =False

        if(int(now_hh)>=self.stop_shell_script_after):
            close_it =True

        

        if self.check_based_on_trade_date :
            if isinstance (quote_details ,list):
                new_quote=[]
                for q_details in quote_details:
                    if isinstance(q_details, dict):
                    
                        trade_date, trade_time = q_details['success'][0]['BD_last_traded_time'].split(' ')
            
                        if(trade_date == self.todays_date):
                            new_quote.append(q_details)

                quote_details = new_quote

            elif isinstance(quote_details, dict):
            
                trade_date, trade_time = quote_details['success'][0]['BD_last_traded_time'].split(' ')
            
                if(trade_date != self.todays_date):
                    return "", close_it
            else:
                return "", close_it

        return quote_details,close_it

    def get_quote(self,instrument_token):
        # print("Token name",instrument_token)
        try:
            rt = self.client.quote(instrument_token=str(instrument_token))
            return rt
        except ApiException as e:
            return ""

    def get_quote_non_threaded(self,instrument_token):
        quote_details= ""
        close_it =False

        if instrument_token != "":
            try:
                quote_details = self.get_quote(instrument_token)
                quote_details,close_it = self.validate_quote(quote_details)
            except Exception as e:
                print(f"{e} -- {instrument_token}")


        return close_it,quote_details


    def callback_method(self,message):
        print(message)   
           
    def kotat_subscribe(self,):    
        print("Your logic/computation will come here.")
        # self.client.subscribe(input_tokens="754", callback=self.callback_method)
        self.client.subscribe(input_tokens="745,754,1900,9516, 43865, 891, 607, 13140, 5653, 10586, 26784, 94320, 16680, 15947, 717, 411, 27206, 4968, 5038, 109230, 413, 19145, 720, 904, 727, 2574, 27632, 15452"
        , callback=self.callback_method)
    
 
           
    def kotat_subscribe_(self,call_fun):    
        print("Your logic/computation will come here.")
        self.client.subscribe(input_tokens="754", callback=call_fun)
        
    
    
    def get_history(self,):
        try:
            # Get historical prices
            self.client.history("historicalprices",{"exchange":"nse","cocode":"1900","fromdate":"01-jan-2014","todate":"08-oct-2015"})
        except Exception as e:
            print("Exception when calling Historical API->details: %s\n" % e)
    
    def fetch_live_short(self,token=None):
        if token == None:
            return False,None
        try:
            data =self.client.quote(instrument_token = token)
            self.count_calls=self.count_calls+1
            print("count :",self.count_calls,"token:",token)
            return  True, data
        except Exception as e:
            print(e)
            return False,None
        
        
        
        

    def fetch_live_depth(self,):
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
                                      reconnection_attempts=5, engineio_logger=True, logger=self.logger)

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










    def get_quote_threaded(self,chunks, timeout=5):
        
        
        results =[]

        if self.thread_loops ==0:
            # Create a ThreadPoolExecutor
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(chunks))
        
            
        # Submit tasks to the executor
        futures = [self.executor.submit(self.get_quote, chunk) for chunk in chunks]

        # Wait for all tasks to complete and get the results
        # results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        
        # Signal that no more tasks will be submitted
        # executor.shutdown(wait=False)
        
        # Wait for all tasks to complete with a timeout
        try:
            completed, not_completed = concurrent.futures.wait(futures, timeout=timeout) # timeout 2 sec
        except concurrent.futures.TimeoutError:
            # Handle timeout (e.g., cancel the remaining tasks)
            print("Timeout reached. Cancelling remaining tasks.")
            for future in not_completed:
                future.cancel()
        except ApiException as e:
            print(e)
    
        # Get the results from completed tasks
        results = [future.result() for future in completed]

        print(f"The sum of the squared numbers is: {len(results)}")  
    

        self.thread_loops = self.thread_loops+1

        return results
    


if __name__ == "__main__":
    k = kotak(path_ini='./config.ini')
    #k.updateTokenNames()
    k.kotak_login()


''' ERROR RESPONSES
-Invalid access code
Reason: Please enter a valid access code
HTTP response body: {"fault":{"code":70051,"description":"Access Code entered by client is invalid. Please enter correct access code.","message":"Please enter a valid access code"}}

-

'''