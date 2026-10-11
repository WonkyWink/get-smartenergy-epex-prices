import requests
import sqlite3
import datetime as dt
from matplotlib import pyplot as plt





std_url ="https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices"
std_db = "DailyPowerPricesDB.db"
std_tbl = "powerPriceTable"
std_datetime="DateTime"
std_price="Price"

#read api json data from the current and 1 day ahead
def get_json(url):
    url = "https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices"
    #headers = {"Content-Type": "application/json"}
    response = requests.get(url)
    dictionary=response.json()
    result=dictionary["energyPrice"]["values"]
    return result
#converting json to readable (deprecated)
def convert_to_readable(json):
    i=0
    for res in json[::4]:

        date=res["dateTimeFrom"][0:10]
        print(date)
        time=res["dateTimeFrom"][11:16]
        print(time)
        cent_price= str(res["value"])[:2]
        print(cent_price, "Cent\n")
        i+=1

    return True
#initial setup of table in sqlite
def create_table(db,table, col1, col2):
    con = sqlite3.connect(db)
    cur = (con.cursor())
    cur.execute(f"CREATE TABLE {table}("
                f"{col1} STRING UNIQUE NOT NULL,"
                f"{col2} INTEGER NOT NULL"
                f")")
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())
#output full table
def get_full_table(db,table):
    con = sqlite3.connect(db)
    cur = con.cursor()
    statement = f'''SELECT * FROM {table}'''
    cur.execute(statement)
    table = cur.fetchall()
    for row in table:
        print(row[0][0:10],row[0][11:13],'Uhr',row[1])
    con.close()
#output todays table
def get_today_table(db,table):
    con = sqlite3.connect(db)
    cur = con.cursor()
    statement = f'''SELECT * FROM {table}'''
    cur.execute(statement)
    table = cur.fetchall()
    for row in table:
        if row[0][0:10] == dt.datetime.now().strftime("%Y-%m-%d"):
            print(row[0][0:10],row[0][11:13],'Uhr',row[1])
    con.close()
#checks if there is duplicate entries
def check_duplicate(db,table):
    con = sqlite3.connect(db)
    cur = (con.cursor())
    try:#
        for row in table:
            if row[0][0:10] == dt.datetime.now().strftime("%Y-%m-%d"):
                    print('duplictate today')
        cur.execute(f"SELECT * FROM {table}")
        con.close()
    except:
        print("ERROR: duplictate today found! ")
        return True
    try:
        for row in table:
            if row[0][0:10] == dt.datetime.now().strftime("%Y-%m-%d+1"):
                    print('duplictate tomorrow')
        cur.execute(f"SELECT * FROM {table}")
        con.close()
    except:
        print("ERROR: duplicates tomorrow found! ")
        return True
    return False
#add todays prices
def fill_todays_prices(url, db,table):
    raw_json=get_json(url)

    if len(raw_json)==192:
        print(f"correct amount of lines!: {len(raw_json)}")
    elif len(raw_json)<192:
        raise ValueError('less entries than expected')
    else:
        raise ValueError('more entries than expected')
    if check_duplicate(db, table): #True=duplicate
        return False
    con = sqlite3.connect(db)
    cur = con.cursor()
    for j in raw_json[0:int(len(raw_json)):4]:
        cur.execute(f"""
            INSERT INTO {table} VALUES
                ('{j['dateTimeFrom']}','{j['value']}')
            """)
    print("Data Inserted in the table: ")
    cur.execute(f"SELECT * FROM {table}")
    con.commit()
    con.close()
#add tomorrows prices
def fill_tomorrows_prices(url, db,table):
    raw_json=get_json(url)
    if len(raw_json)==192:
        print(f"correct amount of lines!: {len(raw_json)}")
    elif len(raw_json)<192:
        raise ValueError('less entries than expected')
    else:
        raise ValueError('more entries than expected')
    #if check_duplicate(raw_json, db, table): #True=duplicate
    #    raise ValueError('ERROR: duplicates found!')
    con = sqlite3.connect(db)
    cur = (con.cursor())
    #print(raw_json[int(len(raw_json)-1)])
    for j in raw_json[int(len(raw_json)/2):int(len(raw_json)-1):4]:
        cur.execute(f"""
            INSERT INTO {table} VALUES
                ('{j['dateTimeFrom']}','{j['value']}')
            """)
    print("Data Inserted in the table: ")
    cur.execute(f"SELECT * FROM {table}")
    con.commit()
    con.close()
#plot basic diagram
def visualize_today(db,table):
    y_values = []
    con = sqlite3.connect(db)
    cur = con.cursor()
    statement = f'''SELECT * FROM {table}'''
    cur.execute(statement)
    table = cur.fetchall()
    for row in table:
        if row[0][0:10] == dt.datetime.now().strftime("%Y-%m-%d"):
            y_values.append(row[1])
            #plt.plot(row[0][11:13])
            #print(row[0][11:13], 'Uhr', row[1])

    x_time = range(0,24)
    plt.plot(x_time,y_values)
    plt.title(f'prices of today {dt.datetime.now().strftime("%d.%b %Y")}')
    plt.xlabel('hour')
    plt.ylabel('cent/kWh')

    plt.grid()
    plt.show()


#TESTING uncomment to test

#visualize_today(std_db,std_tbl)
#create_table("DailyPowerPricesDB.db","powerPriceTable","DateTime","Price")
#get_full_table(std_db,std_tbl)
#get_today_table(std_db,std_tbl)
#check_duplicate(get_json(std_url),std_db,std_tbl)
#fill_todays_prices(std_url,std_db,std_tbl,std_datetime,std_price)
#get_full_table(std_db,std_tbl)

#fill_tomorrows_prices(std_url,std_db,std_tbl,std_datetime,std_price)
#get_full_table(std_db,std_tbl)

#check_duplicate(std_db,std_tbl)
