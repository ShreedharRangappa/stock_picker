import threading
from kotak_online import kotak
from test_script import Test
from threading import Thread, Event
from configparser import ConfigParser



class SBOT():
    def __init__(self) -> None:
        self.event = threading.Event()
        self.event.clear()              # unset as default
        self.KOT = kotak(self.event)
        # self.TST = Test(self.event)



    if __name__ == "__main__":
        sb=SBOT()



#https://www.digitalocean.com/community/tutorials/how-to-install-and-use-timescaledb-on-ubuntu-18-04
