import sqlite3
from p1 import *
from hard_code_db import *
reset = False
program_count = 5
conn = sqlite3.connect('stock_weather_data_demo.db')
cur = conn.cursor()
# RESET STOCK AND WEATHER TABLES IF NEEDED
if reset:
    cur.execute('DELETE FROM amzn_stock')
    cur.execute('DELETE FROM netflix_stock')
    cur.execute('DELETE FROM tsla_stock')
    cur.execute('DELETE FROM weather')
    cur.execute('DROP TABLE amzn_stock')
    cur.execute('DROP TABLE netflix_stock')
    cur.execute('DROP TABLE tsla_stock')
    cur.execute('DROP TABLE weather')
    conn.commit()
    conn.close()
else:
    # Create Stock and Weather Tables
    cur.execute('''
        CREATE TABLE IF NOT EXISTS amzn_stock (
            date_id INTEGER PRIMARY KEY,
            amazon_stock_volume INTEGER
        )''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS netflix_stock (
            date_id INTEGER PRIMARY KEY,
            netflix_stock_volume INTEGER
        )''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tsla_stock (
            date_id INTEGER PRIMARY KEY,
            tesla_stock_volume INTEGER
        )''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            date_id INTEGER PRIMARY KEY,
            temp REAL
        )
    ''')

    # Split tables into 6 parts of < 25 items each
    count = 0

    # POPULATE STOCK TABLES WITH DATE_ID AND STOCK VOLUME
    cur.execute('''
        SELECT date_id FROM amzn_stock
                ''')
    used_amzn = cur.fetchall()
    used_amzn = [item[0] for item in used_amzn]
    count_amzn_rep = 0
    for key,val in amzn_volume_data.items():
        # Find date id based on date
        cur.execute('''
            SELECT date_id
            FROM date_table
            WHERE date = ?
        ''', (key,))
        date_id = cur.fetchone()[0]
        if count_amzn_rep < 25 and date_id not in used_amzn:
            # Populate amzn stock table
            cur.execute('''
                INSERT INTO amzn_stock
                (date_id, amazon_stock_volume)
                VALUES (?, ?)''', (date_id, amzn_volume_data[key], ))
            conn.commit()
            count_amzn_rep += 1
    
    cur.execute('''
    SELECT date_id FROM netflix_stock
            ''')
    used_nflx = cur.fetchall()
    used_nflx = [item[0] for item in used_nflx]
    count_nflx_rep = 0
    for key,val in nflx_volume_data.items():
        cur.execute('''
            SELECT date_id
            FROM date_table
            WHERE date = ?
        ''', (key,))
        date_id = cur.fetchone()[0]
        if count_nflx_rep < 25 and date_id not in used_nflx:
            cur.execute('''
                INSERT INTO netflix_stock
                (date_id, netflix_stock_volume)
                VALUES (?, ?)''', (date_id, nflx_volume_data[key], ))
            conn.commit()
            count_nflx_rep += 1

    cur.execute('''
    SELECT date_id FROM tsla_stock
            ''')
    used_tsla = cur.fetchall()
    used_tsla = [item[0] for item in used_tsla]
    count_tsla_rep = 0

    for key,val in tsla_volume_data.items():
        cur.execute('''
            SELECT date_id
            FROM date_table
            WHERE date = ?
        ''', (key,))
        date_id = cur.fetchone()[0]
        if count_tsla_rep < 25 and date_id not in used_tsla:
            cur.execute('''
                INSERT INTO tsla_stock
                (date_id, tesla_stock_volume)
                VALUES (?, ?)''', (date_id, tsla_volume_data[key], ))
            conn.commit()
            count_tsla_rep += 1
            
    cur.execute('''
    SELECT date_id FROM weather
            ''')
    used_weather = cur.fetchall()
    used_weather = [item[0] for item in used_weather]
    count_weather_rep = 0

    for key,val in weather_data.items():
        cur.execute('''
            SELECT date_id
            FROM date_table
            WHERE date = ?
        ''', (key,))
        date_id = cur.fetchone()[0]

        if count_weather_rep < 25 and date_id not in used_weather:
            cur.execute('''
                INSERT INTO weather
                (date_id, temp)
                VALUES (?, ?)''', (date_id, val))
            conn.commit()
            count_weather_rep += 1





    conn.close()