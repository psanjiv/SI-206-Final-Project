import matplotlib.pyplot as plt
from p3 import *

data = result[1:]
# SELECT DATE AND STOCK PRICE FROM DATA
dates = [entry[1] for entry in data]
stock_prices = [entry[2] for entry in data]

# Create a line plot
plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(dates, stock_prices, marker='o', linestyle='-', color='b')  # Plot the data

# Set titles and labels
plt.title('Average Stock Volume over Time (from 07/20/23 - 12/08/23)')
plt.xlabel('Date')
plt.ylabel('Average Stock Volume (shares) of AMZN, TSLA, NFLX')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)
plt.xticks(dates[::9], rotation=45)

# Display gridlines
plt.grid(True)

# Show plot
plt.tight_layout()
# plt.show()

##########################################################################################
# MATCHES TEMP AND STOCK VOLUME TOGETHER
# SORT BASED ON THE TEMP (MAKE SURE EACH TEMP IS ASSOCIATED WITH ITS STOCK VOLUME)
# PLOT IT WITH TEMP ON X-AXIS AND STOCK VOLUME ON Y-AXIS

temp = [entry[3] for entry in data]
stock_prices = [entry[2] for entry in data]
data_list = [[temp[i], stock_prices[i]] for i in range(len(temp))]
data_list = sorted(data_list, key=lambda x: x[0])

temp_values = [entry[0] for entry in data_list]
temp_stock_prices = [entry[1] for entry in data_list]
# Create a line plot
plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(temp_values, temp_stock_prices, marker='o', linestyle='-', color='b')  # Plot the data

# Set titles and labels
plt.title('Average Stock Volume (shares) vs Weather (from 07/20/23 - 12/08/23)')
plt.xlabel('Temperature (deg F) Over Time')
plt.ylabel('Average Stock Volume of AMZN, TSLA, NFLX')

# Display gridlines
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()