import sqlite3
#PART 3
conn = sqlite3.connect('stock_weather_data_demo.db')
cur = conn.cursor()

# TAKE THE STOCK TABLES AND FIND AVERAGE STOCK VOLUME, AND JOINS THEM BASED ON THEIR DATE ID
# SELECT DATE_ID, DATE, AVERAGE STOCK VOLUME, AND TEMPERATURE
cur.execute('''
    SELECT amzn_stock.date_id AS date_id,
           date_table.date AS date,
           AVG((amzn_stock.amazon_stock_volume + netflix_stock.netflix_stock_volume + tsla_stock.tesla_stock_volume) / 3) AS avg_stock,
           weather.temp AS temperature
    FROM amzn_stock
    JOIN netflix_stock ON amzn_stock.date_id = netflix_stock.date_id
    JOIN tsla_stock ON amzn_stock.date_id = tsla_stock.date_id
    JOIN weather ON amzn_stock.date_id = weather.date_id
    JOIN date_table ON amzn_stock.date_id = date_table.date_id
    GROUP BY amzn_stock.date_id, date_table.date, weather.temp
''')

result = cur.fetchall()

# PRINT RESULTS INTO A FILE OUT.TXT
result.insert(0, ('Date ID', 'Date', 'Average Stock Volume (shares)', 'Temperature (Fahrenheit)'))
with open('out.txt', 'w') as file:
    # Calculate the padding based on the length of the column headers
    column_padding = [max(len(str(row[i])) for row in result) for i in range(len(result[0]))]

    # Write column names with aligned formatting
    for i, column in enumerate(result[0]):
        file.write("{:<{width}s}".format(column, width=column_padding[i] + 5))
    file.write('\n')

    # Write data rows with aligned formatting
    for row in result[1:]:
        for i, value in enumerate(row):
            file.write("{:<{width}}".format(str(value), width=column_padding[i] + 5))
        file.write('\n')
conn.close()