import finnhub
import requests
import pandas as pd
import datetime as dt
import os
import petl as etl
import psycopg2 as pg
from twilio.rest import Client
# import petl as etl
# Get database access
conn = pg.connect(database="postgres", user="postgres", password="12345678",
                        host="database-1.cdduldn0e0oh.us-east-2.rds.amazonaws.com", port="5432")
cur = conn.cursor()


# Get API access to finnhub
finnhub_client = finnhub.Client(api_key="c4m8ur2ad3icjh0eek9g")
ticker = 'AAPL'

# Define basic parameters
dt1 = int(dt.datetime.now().timestamp())

#ETL
cur.execute("""
           select max("time_stamp"), max("id") from stock_data """)
last_t, last_id = cur.fetchall()[0]

dt_last = int(dt.datetime.timestamp(last_t))

update_data = finnhub_client.stock_candles(ticker, 'D', dt_last + 86400, dt1)
print(update_data)

if update_data['t'] == None:
    conn.close()

else:

    df_update = pd.DataFrame(update_data)

    c = []
    for i in df_update['t']:
        a = dt.datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
        c.append(a)

    df_update['t'] = c

    # add stock symbol to dataset.
    # Round data values to 4 decimals
    # reset dataset index starting from 1 instead 0
    df_update['stock'] = ticker
    df_update = df_update.round(4)
    df_update.index = df_update.index + last_id + 1

    df_update.to_csv('stock_data_update.csv')
    table = (etl.fromcsv('stock_data_update.csv')
             .convert('c', float)
             .convert('h', float)
             .convert('l', float)
             .convert('o', float)
             .convert('s', 'lower')
             .convert('v', float)
             .tocsv('stock_data_update_ReadytoLoad.csv'))

    filename_update = 'stock_data_update_ReadytoLoad.csv'

    with open(filename_update, 'r') as f:
        next(f)
        cur.copy_from(f, 'stock_data', sep=",")

    conn.commit()
    conn.close()
# set alert
    account_sid = os.getenv('ACe9f994212d6176c004f1e5634d06f81e')
    token = os.getenv('1fa66e9626963b2e9a18ab54e7f8370b')
    client = Client(account_sid, token)
    try:
        update_table(table_exist)
        message = client.messages \
            .create(body="Daily ETL job done.",
                    from_='+18437322825',
                    to='+8613311728161'
                    )
    except ValueError:
        message = client.messages \
            .create(body="Daily ETL job fail.",
                    from_='+18437322825',
                    to='+8613311728161'
                    )