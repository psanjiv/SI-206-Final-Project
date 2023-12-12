import requests
import sqlite3
import json
from hard_code_db import *
#Hard coded api call result becuase of ran out of limited api calls on free trial per day on demo day
run_db = False
reset = False
run_date_table = True
program_count = 0

conn = sqlite3.connect('stock_weather_data_demo.db')
cur = conn.cursor()

# GET STOCK DATA FROM API CALLS AND STORE IN DICT
if run_db:
  # key = "DLCMSMT81ZNW1D20"
  key = "DDPJI47V1UP5FUVW"
  amzn_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&outputsize=compact&interval=5min&apikey={key}'
  r = requests.get(amzn_url)
  data = r.json()
  # time_series includes each of the dates and relevant stock data
  time_series = data.get('Time Series (Daily)', {})
  amzn_volume_data = {}
  for date, values in time_series.items():
    volume = float(values.get("5. volume", 0))
    amzn_volume_data[date] = volume


  tsla_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&outputsize=compact&interval=5min&apikey={key}'
  r = requests.get(tsla_url)
  data = r.json()
  time_series = data.get('Time Series (Daily)', {})
  tsla_volume_data = {}
  for date, values in time_series.items():
    volume = float(values.get("5. volume", 0))
    tsla_volume_data[date] = volume

  nflx_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=nflx&outputsize=compact&interval=5min&apikey={key}'
  r = requests.get(amzn_url)
  data = r.json()
  time_series = data.get('Time Series (Daily)', {})
  nflx_volume_data = {}
  for date, values in time_series.items():
    volume = float(values.get("5. volume", 0))
    nflx_volume_data[date] = volume

  print(json.dumps(amzn_volume_data, indent=2))
  print(json.dumps(tsla_volume_data, indent=2))
  print(json.dumps(nflx_volume_data, indent=2))

# GET WEATHER DATA FROM API CALL AND STORE IN DICT
response = requests.get("https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2023-07-20&end_date=2023-12-09&daily=apparent_temperature_mean&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch")
data = response.json()
weather_data = {}
count = 0
date_list = data['daily']['time']
temp_list = data['daily']['apparent_temperature_mean']
# MAKE A DICT WITH DATE AS KEY AND TEMP AS VALUE
for date in date_list:
  weather_data[date] = temp_list[count]
  count += 1

# print(json.dumps(weather_data, indent=2))
# MAKE A DATE_DICT WITH DATE_ID AS KEY AND DATE AS VALUE (SHARED INTEGER KEY)
date_dict = {}
date_id = 0
for date in date_list:
    date_dict[date_id] = date
    date_id+= 1

# MAKE 6 DICTS, WHERE WE SPLIT THE 144 WEATHER DATA INTO 6 SEPARATE DICTS
# date_dict = {date_id: date}
if reset:
  # Resets date table
  cur.execute('DELETE FROM date_table')
  cur.execute('DROP TABLE date_table')
  conn.commit()
  conn.close()
else:
  if run_date_table:
    # CREATE A TABLE OF DATE_ID TO DATE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS date_table (
            date_id INTEGER PRIMARY KEY,
            date TEXT
        )''')
    
    cur.execute('''
        SELECT date_id FROM date_table
                ''')
    used = cur.fetchall()
    used = [item[0] for item in used]
    # Populate Date Table
    count = 0
    for key,val in date_dict.items():
        if count < 25 and key not in used:
          cur.execute('''
              INSERT INTO date_table
              (date_id, date)
              VALUES (?, ?)''', (key, val, ))
          conn.commit()
          count += 1


    conn.close()