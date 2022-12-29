import psycopg2
import configparser
from time import sleep



class DATABASEMANAGER():
    def __init__(self) -> None:
        self.dbConf = self.getParams()
        self.conn = None
        self.curr = None

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
        self.db_depth = conf.getint('record','depth')

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
        attributes = ''' CREATE TABLE IF NOT EXISTS stockdb (
                        a varchar(40),
                        b varchar(40),
                        c varchar(40),
                        d varchar(40),
                        e varchar(40),
                        f varchar(40),
                        g varchar(40),
                        h varchar(40),
                        i varchar(40),
                        j varchar(40),
                        k varchar(40),
                        l varchar(40),
                        m varchar(40),
                        n varchar(40),
                        o varchar(40),
                        p varchar(40),
                        q varchar(40),
                        r varchar(40),
                        s varchar(40),
                        t varchar(40),
                        u varchar(40),
                        v varchar(40),
                        w varchar(40)
                                    
                        )'''
        return attributes

    def updateStockTable(self,):
        insert_script = 'INSERT INTO stockdb (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        insert_values = [('1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'),
                         ('2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2')]

        try:
            for record in insert_values:
                self.curr.execute(insert_script, record)

            self.conn.commit()
            return True

        except Exception as e:
            print(e)

            return False

    def updateStockTable_test(self,insert_values):
        insert_script = 'INSERT INTO stockdb (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        
        try:
            for record in insert_values:
                self.curr.execute(insert_script, record)

            self.conn.commit()
            return True

        except Exception as e:
            print(e)

            return False
    def startDbConnection_example(self):

        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.db_name,
                user=self.usrname,
                password=self.pwd,
                port=self.port_id
            )
            self.curr = self.conn.cursor()

            create = ''' CREATE TABLE IF NOT EXISTS test1 (
                        id  int PRIMARY KEY,
                        name varchar(40) NOT NULL,
                        salary int,
                        dept_id varchar(30))'''
            try:
                self.curr.execute(create)
                return True
            except Exception as e:
                print(e)

                return False
        except Exception as e:
            print(e)

            return False

    def updateDB_example(self,):
        insert_script = 'INSERT INTO test1 (id, name, salary, dept_id) VALUES (%s,%s,%s,%s)'
        insert_values = [(10, 'jane', 1200, 'nurse'), (20,
                                                       'jane3', 100, 'nurse'), (30, 'jan2e', 1200, 'nurse')]

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
    dbm = DATABASEMANAGER()
    dbm.linkStockDB()
    dbm.updateStockTable()
    
    for i in range(10,200,1):
        insert_values =[(str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i),str(i))]
        dbm.updateStockTable_test(insert_values)
        sleep(1/1000)
        
        
        
    
    
    
    # print(dbm.startDbConnection_example())
    # print(dbm.updateDB_example())
    print(dbm.closeDB())
