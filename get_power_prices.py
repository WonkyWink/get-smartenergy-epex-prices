import requests
import sqlite3
import datetime as dt
from matplotlib import pyplot as plt


#from matplotlib import pyplot as plt


class PowerPrices:
    #read api json data from the current and 1 day ahead
    def __init__(self, url:str, db:str="New.db", tbl:str="New_table", columns=None):
        if columns is None:
            columns = ['1', '2']
        self.url = url
        self.db = db
        self.tbl=tbl
        self.columns=columns
        self.today_date =dt.date.today()
        self.current_json = requests.get(url).json()
    def __str__(self):
        return f"This object contains data from: {self.url}, in DB: {self.db}, in cable: {self.tbl}, has columns: {self.columns}."

    def get_json(self):
        response = requests.get(self.url)
        result = response.json()["energyPrice"]["values"]
        return result

    def check_duplicate(self, day="today"):#today or tomorrow
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(f'''SELECT * FROM {self.tbl} order by DateTime desc;''')
        today_date = str(dt.date.today())
        tomorrow_date = str(dt.date.today() + dt.timedelta(days=1))
        fetched_results = cur.fetchmany(25)
        error_string = []
        position = [0]

        if day == "today" :
            try:
                if fetched_results[-25][0][:10] == today_date:
                    error_string.append(f'{today_date} is already in table at 2nd last index')
                    position+='1'
                if fetched_results[-1][0][:10] == today_date:
                    error_string.append(f'{today_date} is already in table at last index')
                    position+='2'
            except AssertionError:
                con.close()
        if day == "tomorrow":
            try:
                if fetched_results[-25][0][:10] == tomorrow_date:
                    error_string.append(f'{tomorrow_date} is already in table at 2nd last index')
                    position+=3
                if fetched_results[-1][0][:10] == tomorrow_date:
                    error_string.append(f'{tomorrow_date} is already in table at last index')
                    position+='4'
            except AssertionError:
                con.close()
            finally:
                if position != [0]: print(*error_string, sep=" & ")
                con.close()
        if error_string: return True #positions: 1=today in 2nd last,
        else: return False


    def get_today_table(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(f'''SELECT * FROM {self.tbl}''')
        table = cur.fetchall()

        string = ""
        for entry in table:
            if entry[0][0:10] == self.today_date:
                string+= f"date:{entry[0][0:10]}\ntime:{entry[0][11:13]}\nprice:{entry[1]}\n\n"
        if string: return string
        else: return "today data is not in table"
    def json_validator(self, json):
        if len(json) == 192:
            print(f"correct amount of lines!: {len(json)}")
        elif len(json) < 192:
            raise ValueError('less entries than expected')
        else:
            raise ValueError('more entries than expected')
        return True


        # add today prices
    def fill_todays_prices(self):
        current_json=self.get_json()
        if not self.json_validator(current_json):
            raise ValueError("invalid json-format")
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        if self.check_duplicate():# True=duplicate
            raise ValueError('Duplicate found, unable to add')

        else:
            for entry in current_json[0:int(len(current_json) / 2):4]:
                cur.execute(f"""
                       INSERT INTO {self.tbl} VALUES
                       ('{entry['dateTimeFrom']}','{entry['value']}')
                  """)
                con.commit()
        print("todays prices inserted successfully")
        return True

    def fill_tomorrows_prices(self):
        current_json = self.get_json()
        if not self.json_validator(current_json):
            raise ValueError("invalid json-format")
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        if self.check_duplicate():  # True=duplicate
            raise ValueError('Duplicate found, unable to add')
        if len(current_json) == 192:
            print(f"correct amount of lines!: {len(current_json)}")
        elif len(current_json) < 192:
            raise ValueError('less entries than expected')
        else:
            raise ValueError('more entries than expected')

        if self.check_duplicate():  # True=duplicate
            raise ValueError('Duplicate found, unable to add')

        else:
            for entry in current_json[int(len(current_json) / 2):int(len(current_json) - 1):4]:
                cur.execute(f"""
                          INSERT INTO {self.tbl} VALUES
                          ('{entry['dateTimeFrom']}','{entry['value']}')
                     """)
                con.commit()
        print("tomorrows prices inserted successfully")
        return True

    #plot basic diagram
    def visualize_today(self, ):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(f'''SELECT * FROM {self.tbl}''')
        table = cur.fetchall()
        y_values = []
        for entry in table:
            if entry[0][0:10] == dt.datetime.now().strftime("%Y-%m-%d"):
                y_values.append(entry[1])
        x_time = range(0,24)
        plt.plot(x_time,y_values)
        plt.title(f'prices of today {dt.datetime.now().strftime("%d.%b %Y")}')
        plt.xlabel('hour')
        plt.ylabel('cent/kWh')

        plt.grid()
        plt.show()


SmartEnergy = PowerPrices("https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices", "DailyPowerPricesDB.db", "powerPriceTable", ["DateTime", "Price"])
#print(SmartEnergy.check_duplicate())
#print(SmartEnergy.get_today_table())
#print(type(SmartEnergy.get_json()))
#print(SmartEnergy.fill_todays_prices())
#print(SmartEnergy.visualize_today())
#print(SmartEnergy.fill_tomorrows_prices())


