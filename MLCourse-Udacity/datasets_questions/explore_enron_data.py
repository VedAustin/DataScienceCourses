#!/usr/bin/python

""" 
    starter code for exploring the Enron dataset (emails + finances) 
    loads up the dataset (pickled dict of dicts)

    the dataset has the form
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person
    you should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

count_pay = 0
count_email = 0

for key in enron_data:
	if enron_data[key]['poi'] == True:
		count_email +=1
	if enron_data[key]['total_payments'] == 'NaN':
		count_pay += 1
	
	'''
	if enron_data[key]['salary'] != 'NaN':
		count_sal += 1
	if enron_data[key]['email_address'] != 'NaN':
		count_email += 1
	
print count_sal,count_email
'''
print float(count_pay)/(len(enron_data)+10)
print len(enron_data),float(count_pay+10),count_email

'''
import pandas as pd
names_poi = pd.read_csv('../final_project/poi_names.txt',sep=' ')
print len(names_poi)
'''
print enron_data['SKILLING JEFFREY K']
#james['exercised_stock_options'] + james['restricted_stock']

