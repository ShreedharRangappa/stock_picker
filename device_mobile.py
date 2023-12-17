from threading import Thread, Event, Lock
from queue import Queue
import time

import datetime
from datetime import date
from kotak_online import kotak
import os
import random
import pandas as pd
import json
import logging





class DUMMY_KOTAK():
    def __init__(self) -> None:
        
        logger = logging.getLogger(__name__)
        
        # Important file checks
        conf_path = os.path.join(os.getcwd(),'config.ini')
        self.instrument_token_file_path =  os.path.join(os.getcwd(),'requested_tokens.json')



        assert os.path.exists(conf_path) , f"Missing {conf_path}. Exiting"
        assert os.path.exists(self.instrument_token_file_path) , f"Missing {self.instrument_token_file_path}. Exiting"
        
        self.kk = kotak(path_ini='./config.ini')

        # Directory generation
        if not os.path.exists(self.kk.save_path):
            os.mkdir(self.kk.save_path)

        assert os.path.exists(self.kk.save_path), f"failed to located directory {self.kk.save_path}. Exiting!"

        # Generate txt file
        x = datetime.datetime.now()
        x_str = x.strftime("%d%m%Y")
        self.saving_text_path = os.path.join(self.kk.save_path,f"{x_str}.txt")
        with open(self.saving_text_path, 'w') as f:
            f.write(f"{x_str}\n")

        # Get instrument token list
        f = open(self.instrument_token_file_path)
        data = json.load(f)
        self.instrument_token = data["userinstrumentTokens"]

    def looped_get_quote(self,):
        
        delta_sec = self.kk.delta
        elapse_time_sec = 0

        while(True):

            if elapse_time_sec>0:
                time.sleep(elapse_time_sec)
            start_ = time.time()
            self.get_quote_of_list()
            

            inner_delta =  time.time() -start_
            if inner_delta >= delta_sec:
                elapse_time_sec = 0
            else:
                elapse_time_sec = delta_sec -inner_delta
                print("sleep time ",elapse_time_sec)


    def get_quote_of_list(self,):
        """
        instrument_token="717,754,1900,2574,14111"              
        """
        
        data=[]

        start = time.process_time()
        
        if len(self.instrument_token)<=0:
            print("No Instrument Token provided")
        else:
            for instrument_token_ in self.instrument_token:
                try:
                    quote_ = self.kk.get_quote(instrument_token=str(instrument_token_))
                    if quote_ != "":
                        data.append(quote_)
                    # print(quote_)
                except Exception as e:
                    print(f"{e} -- {instrument_token_}")
                    self.instrument_token.remove(int(instrument_token_))

        if self.kk.verbose:
            print(f"{self.get_quote_of_list.__name__} Time : {time.process_time() - start} ")

        # Save into Text
        self.save_quote2text(data)


    def save_quote2text(self, data_write):
        
        start = time.process_time()
        with open(self.saving_text_path, 'a') as f:
            for data in data_write:
                f.write(f"{data}\n")
        f.close()
        if self.kk.verbose:
            print(f"{self.save_quote2text.__name__} Time : {time.process_time() - start} ")



if __name__ == "__main__":
    e = DUMMY_KOTAK()
    e.kk.kotak_login()
    e.looped_get_quote()



