import psycopg2
import configparser
from time import sleep
import datetime


class DBMANAGER_SHORT():
    def __init__(self) -> None:
        self.dbConf = self.getParams()
        self.conn = None
        self.curr = None
        x = datetime.datetime.now()
        self.mmddyy=x.strftime("%d%m%Y_short")
    
        

    def getParams(self,):
        try:

            conf = configparser.ConfigParser()
        except:
            conf = ConfigParser.ConfigParser()
        # conf_file=os.path.join(pwd,"src/mo_settings.ini")

        conf.read('/home/vdgs/git/stock_bot/config.ini')

        # Read params

        self.hostname = conf.get('db', 'hostname')
        self.db_name = conf.get('db', 'db_name')
        self.usrname = conf.get('db', 'usrname')
        self.pwd = conf.get('db', 'pwd')
        self.port_id = conf.getint('db', 'port_id')
        
        

    def linkStockDB(self,):
        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.db_name,
                user=self.usrname,
                password=self.pwd,
                port=self.port_id
            )
            self.curr = self.conn.cursor()

            table_attributes = self.createStockTable()
            try:
                self.curr.execute(table_attributes)
                return True
            except Exception as e:
                print(e)
                return False
        except Exception as e:
            print(e)
            return False

    def createStockTable(self,):
        # wtoken ,ltp ,lv_net_chg ,lv_net_chg_perc ,open_price ,closing_price ,high_price ,low_price ,average_trade_price ,last_trade_qty ,BD_last_traded_time ,OI ,BD_TTQ ,market_exchange ,stk_name ,display_segment ,display_fno_eq 
        
        
        attributes = ''' CREATE TABLE IF NOT EXISTS db_20221229  (
                        wtoken varchar(40),
                        ltp varchar(40),
                        lv_net_chg varchar(40),
                        lv_net_chg_perc varchar(40),
                        open_price varchar(40),
                        closing_price varchar(40),
                        high_price varchar(40),
                        low_price varchar(40),
                        average_trade_price varchar(40),
                        last_trade_qty varchar(40),
                        BD_last_traded_time varchar(40),
                        OI varchar(40),
                        BD_TTQ varchar(40),
                        market_exchange varchar(40),
                        stk_name varchar(40),
                        display_segment varchar(40),
                        display_fno_eq varchar(40)
                                    
                        )''',
        return attributes

    def updateStockTable(self,):
        insert_script = 'INSERT INTO stockdb (wtoken ,ltp ,lv_net_chg ,lv_net_chg_perc ,open_price ,closing_price ,high_price ,low_price ,average_trade_price ,last_trade_qty ,BD_last_traded_time ,OI ,BD_TTQ ,market_exchange ,stk_name ,display_segment ,display_fno_eq ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        
        try:
            for record in insert_values:
                self.curr.execute(insert_script, record)

            self.conn.commit()
            return True

        except Exception as e:
            print(e)

            return False

            
        
    
    def closeDB(self,):
        try:
            if self.curr is not None:
                self.curr.close()
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    dbm = DBMANAGER_SHORT()
    dbm.linkStockDB()
    dbm.updateStockTable()
    
    for i in range(10,200,1):
        insert_values =[(str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i))]
        dbm.updateStockTable_test(insert_values)
        sleep(1/1000)
     
    print(dbm.closeDB())
