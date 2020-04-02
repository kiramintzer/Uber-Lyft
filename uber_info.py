from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lat_long_list import lat_long_list

import uber_tokens
import json
import sqlite3
import datetime

# This file is meant to do access the Uber API and then populate our created table with the Uber information. 
# Anything that is commented out do not touch. The code will run perfectly with everything as is. 

session = Session(server_token= uber_tokens.server_token)
client = UberRidesClient(session)

conn = sqlite3.connect('rideshare.sqlite')
cur = conn.cursor()
# cur.execute('DROP TABLE IF EXISTS RideShareOtherCompany')
# cur.execute('CREATE TABLE RideShareOtherCompany(companyname TEXT, start_latitude FLOAT, start_longitude FLOAT, end_latitude FLOAT, end_longitude FLOAT, pair_id INTEGER, distance FLOAT, costmin FLOAT, costmax FLOAT, time_requested TIMESTAMP)')

count = 0
for pairs in lat_long_list: 
    pair_id = lat_long_list.index(pairs)


    lat1 = pairs[0]['lat']
    lat2 = pairs[1]['lat']
    long1 = pairs[0]['long']
    long2 = pairs[1]['long']

    cur.execute("SELECT time_requested FROM RideShareOtherCompany WHERE pair_id="+str(pair_id)+" ORDER BY time_requested DESC")
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

        if count > 10:
            print("Added to database. Restart to retrieve more")
            break

        response = client.get_price_estimates(
            start_latitude= lat1,
            start_longitude= long1,
            end_latitude= lat2,
            end_longitude= long2,
            )

        estimate = response.json.get('prices')
        found = False
        for line in estimate:
            if line["display_name"] == "UberX" and not found:
                found = True
                costmax = line["high_estimate"]
                costmin= line["low_estimate"]
                distance = line["distance"]
                # print(costmax)
                # print(costmin) 
                # print(distance)

                # cur.execute('INSERT INTO RideShareOtherCompany (companyname, start_latitude, start_longitude, end_latitude, end_longitude, pair_id, distance, costmin, costmax, time_requested) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("Uber", lat1, long1, lat2, long2, pair_id, distance, costmin, costmax, datetime.datetime.now()))
                # conn.commit()

        response = client.get_price_estimates(
                start_latitude= lat2,
                start_longitude= long2,
                end_latitude= lat1,
                end_longitude= long1,
                )

        estimate = response.json.get('prices')
        found = False
        for line in estimate:
            if line["display_name"] == "UberX" and not found:
                found = True
                costmax = line["high_estimate"]
                costmin= line["low_estimate"]
                distance = line["distance"]

                # cur.execute('INSERT INTO RideShareOtherCompany (companyname, start_latitude, start_longitude, end_latitude, end_longitude, pair_id, distance, costmin, costmax, time_requested) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("Uber", lat2, long2, lat1, long1, pair_id, distance, costmin, costmax, datetime.datetime.now()))
                # conn.commit()

