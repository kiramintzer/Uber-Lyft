from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient
import lat_long_list

import lyft_tokens
import json
import sqlite3
import datetime
import time

# This file is meant to do access the Lyft API and then populate our created table with the Lyft information. 
# Anything that is commented out do not touch. The code will run perfectly with everything as is. 

auth_flow = ClientCredentialGrant(
    lyft_tokens.YOUR_CLIENT_ID,
    lyft_tokens.YOUR_CLIENT_SECRET,
    lyft_tokens.YOUR_PERMISSION_SCOPES,
    )
session = auth_flow.get_session()
client = LyftRidesClient(session)


conn = sqlite3.connect('rideshare.sqlite')
cur = conn.cursor()
# cur.execute('DROP TABLE IF EXISTS RideShare') #comment this (and below) out after running first time
# cur.execute('CREATE TABLE RideShare(companyname TEXT, start_latitude FLOAT, start_longitude FLOAT, end_latitude FLOAT, end_longitude FLOAT, pair_id INTEGER, distance FLOAT, costmin FLOAT, costmax FLOAT, time_requested TIMESTAMP)')

count = 0
for pairs in lat_long_list.lat_long_list:
    pair_id = lat_long_list.lat_long_list.index(pairs)


    lat1 = pairs[0]['lat'] 
    lat2 = pairs[1]['lat']
    long1 = pairs[0]['long']
    long2 = pairs[1]['long']

    cur.execute("SELECT time_requested FROM RideShare WHERE pair_id="+str(pair_id)+" ORDER BY time_requested DESC")
    if cur.fetchone():
        timestring = cur.fetchone()[0]
        dateobject = datetime.datetime.strptime(timestring,"%Y-%m-%d %H:%M:%S.%f")
        diff = datetime.datetime.now() - dateobject
    else:
        diff = datetime.timedelta(seconds=10000) 
    
    if diff.total_seconds() < 1800: 
        print("Found in database ")
    else:
        count += 1

        if count > 10 :
            print('Added to database, restart to retrieve more')
            break

        response = client.get_cost_estimates(
            start_latitude = lat1,
            start_longitude = long1,
            end_latitude = lat2,
            end_longitude = long2,
            ride_type = 'lyft'
        )
        estimate = response.json.get('cost_estimates')
        distance = estimate[0]['estimated_distance_miles']
        costmin = estimate[0]['estimated_cost_cents_min']
        costmax = estimate[0]['estimated_cost_cents_max']

        # cur.execute('INSERT INTO RideShare(companyname, start_latitude, start_longitude, end_latitude, end_longitude, pair_id, distance, costmin, costmax, time_requested) VALUES (?,?,?,?,?,?,?,?,?,?)', ('Lyft', lat1, long1, lat2, long2, pair_id, distance, costmin, costmax, datetime.datetime.now()))
        # conn.commit()

        # flipping lat and long pair
        response = client.get_cost_estimates(
            start_latitude = lat2,
            start_longitude = long2,
            end_latitude = lat1,
            end_longitude = long1,
            ride_type = 'lyft'
        )
        estimate = response.json.get('cost_estimates')
        distance = estimate[0]['estimated_distance_miles']
        costmin = estimate[0]['estimated_cost_cents_min']
        costmax = estimate[0]['estimated_cost_cents_max']

        # cur.execute('INSERT INTO RideShare(companyname, start_latitude, start_longitude, end_latitude, end_longitude, pair_id, distance, costmin, costmax, time_requested) VALUES (?,?,?,?,?,?,?,?,?,?)', ('Lyft', lat2, long2, lat1, long1, pair_id, distance, costmin, costmax, datetime.datetime.now()))
        # conn.commit()

    
