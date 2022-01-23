import pandas as pd
import datetime as dt
import math
from math import radians, cos, sin, asin, sqrt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle


df = pd.read_csv('uber.csv')


# Firs I'm going to remove unnamed and key columns as we do not need them.
df.drop(columns = ['Unnamed: 0', 'key'], inplace= True)

# latitude and longitude = 0 is in the middle of ocean!
df = df[(df['pickup_latitude']!=0.000000)|(df['pickup_longitude']!=0.000000)|(df['dropoff_latitude']!=0.000000)|(df['dropoff_longitude']!=0.000000)]

# Before doing EDA wi are going to need to extract time and date infromation from pickup_datetime column

df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], utc = True)

# Now I will split date and time into two columns

df['date'] = pd.to_datetime(df['pickup_datetime']).dt.date
df['time'] = pd.to_datetime(df['pickup_datetime']).dt.time

# In this step I am going to remove pickup_datetime column
df.drop('pickup_datetime' , axis = 1,inplace=True)

df.reset_index(inplace=True)

# Now let's convert date into days of the week, months, years  

df['day'] = df['date'].apply(lambda x: x.strftime('%A')) # day of the week like Friday
df['month'] = df['date'].apply(lambda x: x.month)
df['year'] = df['date'].apply(lambda x: x.year)

# Remove date column
df.drop('date', axis=1, inplace= True)

df.dropna(inplace=True)

# Now let's convert time into morning, afternoon, night and mid-night

def date_splitter(times):
    output = ''
    if dt.time(6,0,0) <= times <= dt.time(11,59,59):
        output = 'morning'
    elif dt.time(12,0,0) <= times <= dt.time(17,59,59):
        output = 'evening'
    elif dt.time(18,0,0) <= times <= dt.time(23,59,59):
        output = 'night'
    elif dt.time(0,0,1) <= times <= dt.time(5,59,59):
        output = 'mid-night'
    return output

df['day-time'] = df.time.apply(date_splitter)
df = df[df['day-time'] != '']
df.drop('time', inplace=True, axis=1)


def calculate_distance(lat1, lat2, lon1, lon2):
	
	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	
	# calculate the result
	return(c * r)
	
df['distance_travelled (KM)']= df.apply(lambda x: calculate_distance(x['pickup_latitude'],x['dropoff_latitude'],x['pickup_longitude'],x['dropoff_longitude']),axis=1)

# We can not have negative fare_amount
df = df[df['fare_amount'] > 0]
# We can not have ziro passengers
df = df[df['passenger_count'] > 0]

# Considering only fares less than 100 KM 
df = df[df['distance_travelled (KM)'] < 100]

df.drop(['index','pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'], axis =1, inplace= True)


categoricals = df[['day','day-time']]

# One hot encoding
one_hot = pd.get_dummies(categoricals)

df = df.join(one_hot)
df.drop(categoricals, axis = 1,inplace=True)



scaler = StandardScaler()
scaling = df[['passenger_count','month', 'year','distance_travelled (KM)']]
scaled = scaler.fit_transform(scaling)
df[['passenger_count','month', 'year','distance_travelled (KM)']] = scaled



X = df.drop('fare_amount', axis=1)
y = df['fare_amount']


X_main, X_evaluate, y_main , y_evaluate = train_test_split(X,y, test_size=0.2, random_state=10)

X_train,X_test,y_train,y_test= train_test_split(X_main,y_main, test_size=0.3, random_state=10)

# Save the dataframe for test
import pickle
df_evaluate = X_evaluate.join(y_evaluate)


with open('df_evaluate.pickle', 'wb') as f_out:
    pickle.dump(( 'df_evaluate.pickle'), f_out)
# Random Forest Regressor
rf_reg = RandomForestRegressor(max_depth=5)
rf_reg.fit(X_train,y_train)

# Save the model
with open('RandomForestRegressor.pickle', 'wb') as f_out:
    pickle.dump(( rf_reg), f_out)

print(f'the model is saved to RandomForestRegressor.pickle')