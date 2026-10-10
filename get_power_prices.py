import requests
import sqlite3

def get_json():
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

def create_table(db,table, col1, col2, col3):
    con = sqlite3.connect(db)
    cur = (con.cursor())
    cur.execute(f"CREATE TABLE {table}({col1}, {col2}, {col3})")
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())


create_table('DailyPowerPricesDB.db','powerPriceTable','Call_ID','DateTime','Price')

#print("Database connected successfully")


'''

for row in cur.execute("SELECT test1, test2 FROM testx ORDER BY test2"):
    print(row)
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())
cur.execute("""
    INSERT INTO testx VALUES
        ('2026-10-08T00:00:00+02:00', 25.476)
""")

conn.commit()

res = cur.execute("SELECT test1 FROM testx")
print(res.fetchall())

conn.close()

call_json=get_json()
call_readable=convert_to_readable(call_json)
#print(call_readable)
'''