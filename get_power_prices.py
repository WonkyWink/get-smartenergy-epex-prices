import requests
import sqlite3
import datetime as dt
from matplotlib import pyplot as plt

std_url ="https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices"
std_db = "DailyPowerPricesDB.db"
std_tbl = "powerPriceTable"
std_datetime="DateTime"
std_price="Price"
statement = f'''SELECT * FROM {std_tbl}'''
today_date= str(dt.date.today())
tomorrow_date = str(dt.date.today() + dt.timedelta(days=1))
con = sqlite3.connect(std_db)
cur = con.cursor()
cur.execute(statement)
table = cur.fetchall()

#read api json data from the current and 1 day ahead
def get_json():
    response = requests.get(std_url)
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

#output full table
def get_full_table():

    cur = con.cursor()
    statement = f'''SELECT * FROM {std_tbl}'''
    cur.execute(statement)
  #  table = cur.fetchall()
    for row in table:
        print(row[0][0:10],row[0][11:13],"o'clock",row[1])

#output todays table
def get_today_table():
    con = sqlite3.connect(std_db)
    cur = con.cursor()
    #statement = f'''SELECT * FROM {table}'''
    cur.execute(statement)
    _table = cur.fetchall()
    for row in _table:
        if row[0][0:10] == today_date:
            print(row[0][0:10],row[0][11:13],"o'clock",row[1])

#checks if there is duplicate entries
def check_duplicate():
    con = sqlite3.connect(std_db)
    cur = con.cursor()
    cur.execute(statement)
    _table = cur.fetchall()
    error_string = []
    try:
        if _table[-25][0][:10] == today_date:
            error_string.append(f'{today_date} is already in table at 2nd last index')

        if _table[-1][0][:10] == today_date:
            error_string.append(f'{today_date} is already in table at last index')
    except:
        return True
    try:
        if _table[-25][0][:10] == tomorrow_date:
            error_string.append(f'{tomorrow_date} is already in table at 2nd last index')
        if _table[-1][0][:10] == tomorrow_date:
            error_string.append(f'{tomorrow_date} is already in table at last index')
    except:
        return True
    finally:
        print(*error_string,sep = " & ")
        return False

#add todays prices
def fill_todays_prices():
    raw_json=get_json()
    con = sqlite3.connect(std_db)
    cur = con.cursor()
    if len(raw_json)==192:
        print(f"correct amount of lines!: {len(raw_json)}")
    elif len(raw_json)<192:
        raise ValueError('less entries than expected')
    else:
        raise ValueError('more entries than expected')
    print(check_duplicate())
    if check_duplicate()==True: #True=duplicate
        raise ValueError:
            print('Duplicate found, unable to add')
    else:
        for row in raw_json[0:int(len(raw_json)/2):4]:
           cur.execute(f"""
                INSERT INTO {std_tbl} VALUES
                ('{row['dateTimeFrom']}','{row['value']}')
           """)
           con.commit()
    return

#add tomorrows prices
def fill_tomorrows_prices():
    raw_json=get_json()
    if len(raw_json)==192:
        print(f"correct amount of lines!: {len(raw_json)}")
    elif len(raw_json)<192:
        raise ValueError('less entries than expected')
    else:
        raise ValueError('more entries than expected')
    #if check_duplicate(raw_json, db, table): #True=duplicate
    #    raise ValueError('ERROR: duplicates found!')

    cur = (con.cursor())
    #print(raw_json[int(len(raw_json)-1)])
    for j in raw_json[int(len(raw_json)/2):int(len(raw_json)-1):4]:
        cur.execute(f"""
            INSERT INTO {std_tbl} VALUES
                ('{j['dateTimeFrom']}','{j['value']}')
            """)
    print("Data Inserted in the table: ")
    cur.execute(f"SELECT * FROM {table}")
    con.commit()

#plot basic diagram
def visualize_today():
    y_values = []
    cur = con.cursor()

    cur.execute(statement)
    _table = cur.fetchall()
    for row in _table:
        if row[0][0:10] == dt.datetime.now().strftime("%Y-%m-%d"):
            y_values.append(row[1])


    x_time = range(0,24)
    plt.plot(x_time,y_values)
    plt.title(f'prices of today {dt.datetime.now().strftime("%d.%b %Y")}')
    plt.xlabel('hour')
    plt.ylabel('cent/kWh')

    plt.grid()
    plt.show()


#TESTING uncomment to test
#visualize_today()
#create_table("DailyPowerPricesDB.db","powerPriceTable","DateTime","Price")
#get_full_table()
#get_today_table()
#check_duplicate()
#fill_todays_prices()
#get_full_table()
#get_json()
#fill_tomorrows_prices()
print(
get_full_table(),
get_today_table(),
check_duplicate(),
fill_todays_prices(),
get_full_table(),
get_json(),
fill_tomorrows_prices())
visualize_today()

#always close the db in the end
con.close()