
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/ce42cf126a5274f0a3aa1ee140ddcf82d5288d4a3ac707fa49f0eb86.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Providence, Rhode Island, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))
    #print(df)

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'ce42cf126a5274f0a3aa1ee140ddcf82d5288d4a3ac707fa49f0eb86')


# In[4]:

#write some python code which returns a line graph of the record high and record low temperatures by day of the year 
#over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
get_ipython().magic('matplotlib notebook')

df = pd.read_csv('./data/C2A2_data/BinnedCsvs_d400/ce42cf126a5274f0a3aa1ee140ddcf82d5288d4a3ac707fa49f0eb86.csv')

#df.head()
#print(df.sort(['Date','ID']).head())

#the "*" operator unpacks a list and applies it to a function. 
#The zip function takes n lists and creates n-tuple pairs from each element from both lists:
df['Yr'], df['M-D']= zip(*df['Date'].apply(lambda x: (x[:4], x[5:])))  
df1 = df[df['M-D'] != '02-29']  
#print(len(df1))
#print(df1.head())


daily_min = df1[(df1['Element'] == 'TMIN') & (df1['Yr'] < '2015')].groupby(['M-D']).agg({'Data_Value': 'min'})/10
daily_max = df1[(df1['Element'] == 'TMAX') & (df1['Yr'] < '2015')].groupby(['M-D']).agg({'Data_Value': 'max'})/10
#print(daily_min)

daily_min15 = df1[(df1['Element'] == 'TMIN') & (df1['Yr'] == '2015')].groupby(['M-D']).agg({'Data_Value':'min'})/10
daily_max15 = df1[(df1['Element'] == 'TMAX') & (df1['Yr'] == '2015')].groupby(['M-D']).agg({'Data_Value':'max'})/10
#print(daily_min15)

#print(len(daily_min))
#print(len(daily_max))

#np.where will return index where logit is true
outlier_min = np.where(daily_min15['Data_Value'] < daily_min['Data_Value'])
outlier_max = np.where(daily_max15['Data_Value'] > daily_max['Data_Value'])
#print(outlier_min)

# start to create chart
plt.figure()

plt.plot(daily_min.values, c='blue', alpha = 0.75, label = 'Record Low (2005-14)')
plt.plot(daily_max.values, c='red', alpha = 0.75, label = 'Record High (2005-14)')
plt.scatter(outlier_min, daily_min15.iloc[outlier_min], s = 5, c = 'green', label = 'Breaking Record Low (2015)')
plt.scatter(outlier_max, daily_max15.iloc[outlier_max], s = 5, c = 'black', label = 'Breaking Record High (2015)')
plt.gca().fill_between(range(len(daily_min)), daily_min['Data_Value'], daily_max['Data_Value'], 
                       facecolor='grey', alpha=0.1)

plt.ylim(-35, 45)
plt.xlim(0, 365)
plt.legend(loc = 8, frameon=False,  fontsize=8)

plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().format_xdata = mdates.DateFormatter('%b')

ticks = np.arange(15, 350, 30.4)
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(ticks, labels)

plt.suptitle('Historical Daily High/Low Temperature (°C)', fontsize=12)
plt.title('near Providence, RI (United State)', fontsize=10)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()


# In[ ]:



