from threading import Thread, Event, Lock
from queue import Queue
from time import sleep, time
import datetime
from datetime import date
from kotak_online import kotak
import os
import random
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

import logging





class DUMMY_KOTAK():
    def __init__(self) -> None:
        
        logger = logging.getLogger(__name__)
        
        # Important file checks
        conf_path = os.path.join(os.getcwd(),'config.ini')
        instrument_token_file_path =  os.path.join(os.getcwd(),'requested_tokens.json')

        assert os.path.exists(conf_path) , f"Missing {conf_path}. Exiting"
        assert os.path.exists(instrument_token_file_path) , f"Missing {instrument_token_file_path}. Exiting"
        
        self.kk = kotak(path_ini='./config.ini')

    def get_quote_of_list(self,):
        """
        instrument_token="717,754,1900,2574,14111"              
        """
        
        instrument_token="717,754,1900,2574,14111"
        if instrument_token == "":
            print("NO Instrument Token provided")
        else:
            for instrument_token_ in instrument_token.split(','):
                try:
                    quote_ = self.kk.get_quote(instrument_token=str(instrument_token_))
                    print(quote_)
                except Exception as e:
                    print(f"{e} -- {instrument_token_}")


if __name__ == "__main__":
    e = DUMMY_KOTAK()
    e.kk.kotak_login()
    e.get_quote_of_list()



