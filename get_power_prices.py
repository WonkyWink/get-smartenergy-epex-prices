import requests
import sqlite3

std_url ="https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices"
std_db = "DailyPowerPricesDB.db"
std_tbl = "powerPriceTable"
std_datetime="DateTime"
std_price="Price"
def get_json(url):
    url = "https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices"
    #headers = {"Content-Type": "application/json"}
    response = requests.get(url)
    dictionary=response.json()
    result=dictionary["energyPrice"]["values"]
    return result
#print(get_json())

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

def create_table(db,table, col1, col2):
    con = sqlite3.connect(db)
    cur = (con.cursor())
    cur.execute(f"CREATE TABLE {table}("
                f"{col1} STRING UNIQUE NOT NULL,"
                f"{col2} INTEGER NOT NULL"
                f")")
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())

def get_full_table(db,table):
    # Connecting to sqlite databse
    con = sqlite3.connect(db)

    # cursor object
    cur = con.cursor()

    # to select all column we will use
    statement = f'''SELECT * FROM {table}'''

    cur.execute(statement)

    print("All the data")
    output = cur.fetchall()
    for row in output:
        print(row)

    con.commit()

    # Close the connection
    con.close()
def check_duplicate(raw_json,db,table):
    try:

        con = sqlite3.connect(db)
        cur = (con.cursor())
        for j in raw_json[0:int(len(raw_json) / 2):4]:
            cur.execute(f"""
                INSERT INTO {table} VALUES
                    ('{j['dateTimeFrom']}','{j['value']}')
                """)
        cur.execute(f"SELECT * FROM {table}")
        con.close()
    except:
        print("ERROR: duplicates found! ")
        return True
    return False





def fill_todays_prices(url, db,table,datetime, price):
    raw_json=get_json(url)

    if len(raw_json)==192:
        print(f"correct amount of lines!: {len(raw_json)}")
    elif len(raw_json)<192:
        raise ValueError('less entries than expected')
    else:
        raise ValueError('more entries than expected')
    if check_duplicate(raw_json, db, table): #True=duplicate
        return False
    con = sqlite3.connect(db)
    cur = (con.cursor())
    for j in raw_json[0:int(len(raw_json)):4]:
        cur.execute(f"""
            INSERT INTO {table} VALUES
                ('{j['dateTimeFrom']}','{j['value']}')
            """)
    print("Data Inserted in the table: ")
    cur.execute(f"SELECT * FROM {table}")
    con.commit()
    con.close()

def fill_tomorrows_prices(url, db,table,datetime, price):
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

    for j in raw_json[int(len(raw_json))/2:int(len(raw_json)):4]:
        cur.execute(f"""
            INSERT INTO {table} VALUES
                ('{j['dateTimeFrom']}','{j['value']}')
            """)
    print("Data Inserted in the table: ")
    cur.execute(f"SELECT * FROM {table}")
    con.commit()
    con.close()

create_table("DailyPowerPricesDB.db","powerPriceTable","DateTime","Price")
get_full_table(std_db,std_tbl)

#check_duplicate(get_json(std_url),std_db,std_tbl)
fill_todays_prices(std_url,std_db,std_tbl,std_datetime,std_price)
get_full_table(std_db,std_tbl)

#fill_tomorrows_prices(std_url,std_db,std_tbl,std_datetime,std_price)
#check_duplicate(get_json(std_url),std_db,std_tbl)
