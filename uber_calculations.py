from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lat_long_list import lat_long_list

import matplotlib
import matplotlib.pyplot as plt
import csv
import os

import uber_tokens
import json
import sqlite3
import datetime
import uber_info
import math


# calculations
def get_costmax(id_num):
    ''' Get the cost max for Uber rides for each pair id of our select latitudes and longitudes. 
        The passed in parameter (the input for the function) is pair_id from our database which maps to the column cost_max.
        This function returns two lists (the output for the function): EvenList is a list of the cost max for every ride from our select major city to a smaller one. 
        OddList is a list of the cost max for every ride from the smaller city to that same major city. '''
    EvenList = [] # even list is ride from major city to smaller suburb 
    OddList = [] # odd list is ride from smaller suburb to major city 
    uber_info.cur.execute('SELECT costmax FROM RideShareOtherCompany WHERE pair_id ='+ str(id_num)) # gives list of tuple [(),(),(),(),(),()]
    for idx, tup in enumerate(uber_info.cur):
        if idx % 2 == 0:
            EvenList.append(tup[0])
        else:
            OddList.append(tup[0])
    print(EvenList)
    print(OddList)
    return EvenList, OddList

def costmax_diff(EvenList, OddList):
    ''' The passed in parameters (the input for this function) are the EvenList and OddList returned from the previous function get_costmax. 
        This function calculates two separate things. First, it calculates the average price for the EvenList (cost there: a trip from a major city to smaller one) 
        and the average price for the OddList(cost back: a trip from a smaller city to a larger one). The second thing it calculates is the difference in price 
        for the two(cost there less cost back), to return the total difference in cost for a trip to-and-from the same locations (the output).  '''
    # evenlist: take sum of all tuples, then divide by number of tuples (2)
    # oddlist: take sum of all tuples, then divide by number of tuples (2) 
    cost_there = sum(EvenList) 
    cost_there_avg = cost_there/len(EvenList)
    cost_back = sum(OddList)
    cost_back_avg = cost_back/len(OddList)
    
    # cost diff of average there and average back
    diff_of_costs = (cost_there_avg - cost_back_avg)
    return (cost_there_avg, cost_back_avg, diff_of_costs)

''' Calling the function for various pair ids, and creating a final list which will consist of the data we plot on our visuals. The list
    will contain differences in average costs for five chosen pair ids.  '''
FinalList = []
EvenList, OddList = get_costmax(0)
FinalList.append(costmax_diff(EvenList, OddList)) # should print 66.66
EvenList, OddList = get_costmax(7)
FinalList.append(costmax_diff(EvenList, OddList)) # should print 8.66
EvenList, OddList = get_costmax(10)
FinalList.append(costmax_diff(EvenList, OddList)) # should print -2.66
EvenList, OddList = get_costmax(15)
FinalList.append(costmax_diff(EvenList, OddList)) # should print 0
EvenList, OddList = get_costmax(20)
FinalList.append(costmax_diff(EvenList, OddList)) # should print 16.67
print(FinalList)


''' Here we are creating our visual and assigning all the necessary variables. '''
# graph
# Get the data that needs to be plotted on x-axis
xvals = ['New York \nto \nScarsdale', 'Ann Arbor \nto \nBloomfield Hills', 'Miami \nto \nFt Lauderdale', 'Chicago \nto \nHighland Park','Nashville \nto \nClarksville' ]
# Get the data that needs to be plotted on y-axis
yvals = [FinalList[0][2], FinalList[1][2], FinalList[2][2], FinalList[3][2],FinalList[4][2]]


'''This section of our code is creating the CSV file that will contain the differences in average costs for our five chosen pairs for both Lyft and Uber. '''
#CSV
headers = ['Cities', 'Price Difference', 'Company']
csvfile = open('writefile.csv', 'a')
file_is_empty = os.stat('writefile.csv').st_size == 0
writefile = csv.writer(csvfile)
if file_is_empty:
    writefile.writerow(headers)
for i in range(len(xvals)):
    row = [xvals[i], FinalList[i][0], FinalList[i][1], yvals[i], 'Uber']
    writefile.writerow(row)

'''This is the remaining part of our code needed to create our visual. '''
# graph continued
#2. plot the bar chart with xvals and yvals. Align the bars in center and assign a color to each bar.
plt.bar(xvals, yvals, align='center', color = ["purple", "pink", "red", "orange", "yellow"])
plt.ylim(-20,80)
plt.axhline(linewidth=1, color='black')
#3.Give ylabel to the plot
plt.ylabel("Difference in Average Price ($)")
#4.Give the title to the plot
plt.title("Price Difference Going From Popular City to Smaller City (within 100 miles) for Uber")
#5.Show the plot
plt.show()



