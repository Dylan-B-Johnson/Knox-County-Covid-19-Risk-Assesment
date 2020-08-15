# "Researchers say anywhere from 25 percent to 80 percent of people with COVID-19 are unaware they have the virus.""
# From Healthline:
# https://www.healthline.com/health-news/50-percent-of-people-with-covid19-not-aware-have-virus
# Model assumes the quartiles, minimum, and maximum frequency of asymptomatic carriers from the above source.
# Model assumes active cases have self-isolated 
# Model assumes the group has the same prevalence of COVID as all other groups in Knox County
# Model assumes that asymptomatic carriers don't know they have the virus. 
# Data is scraped from Knox County's COVID data page

import pandas as pd
from datetime import date
import datetime
import requests
import csv, io  

# Displays most of the data avaiable from Knox County's Health Department about COVID-19 and
# breaks it down by age group, sex, and race.
def knox_data():
    print('\n\n--------------------Extra Data--------------------\n')
    url = "https://covid.knoxcountytn.gov/includes/covid_summary.csv"
    content_of_csv = requests.get(url).text
    count=0
    data=[]
    for i in csv.reader(io.StringIO(content_of_csv)):
        if count==0:
            cats=i
        if count!=0:
            data.append(i)
        count+=1

    for cat, i in zip(cats[-10:], range(len(cats[-10:]))): 
        if cat!='': print('----------'+cat+'----------')
        for row in data:
            if row[i+1]=='':
                pass
            else: print(row[0]+':\t'+row[i+1])
        if cat!='': print('\n') 

# Using a given group size this calculates and displays the expected number of people 
# in that group that have COVID-19 in Knox County, Tennessee
# Feel free to adapt for other counties 
def knox_get_my_risk(group_size):
    print('\n\n--------------------Group COVID Risk--------------------\n')
    url = "https://covid.knoxcountytn.gov/includes/covid_cases.csv"
    content_of_csv = requests.get(url).text
    for i in csv.reader(io.StringIO(content_of_csv)):
        if i[0] == "Number of Active Cases":
            active_cases=int(i[1])
        if i[0]=='deaths':
            deaths=int(i[1])
    url = "https://covid.knoxcountytn.gov/includes/covid_summary.csv"
    content_of_csv = requests.get(url).text
    for i in csv.reader(io.StringIO(content_of_csv)):
        if i[0] == "Total":
            population=int(i[1][:3]+i[1][-3:])
    print('Active Cases: ',active_cases,'\n')
    q=4
    for asymp_percentage in [0.80,((0.80-0.25)*0.75),((0.80-0.25)*0.50),((0.80-0.25)*0.25),0.25]:
        asymp_cases=((active_cases)/(1-asymp_percentage))-active_cases
        west_students=asymp_cases/population*group_size
        if q==4:
            label='Max'
            maximum_west=west_students
        if q==3: label='Q3'
        if q==2:
            label='Med'
            med_west=west_students
        if q==1: label='Q2'
        if q==0:
            label='Min'
            min_west=west_students
        print('----------'+label+' ('+str(asymp_percentage*100)[:4]+'%)----------\nCounty Asymp Cases:\n'+
              str(asymp_cases)[:6]+' ('+str(asymp_cases/population*100)+'%)\n')
        print('Asymp Ppl in Group:\n'+str(west_students)[:4]+'\n')
        q-=1 
    print('\n--------------------Summary--------------------\n'+
         'Range of Asymp Ppl in Group:\n'+str(min_west)[:4]+' - '+str(maximum_west)[:4]+'\n\nMed of Asymp Ppl in Group:'+
          '\n'+str(med_west)[:4])
       
if __name__ == "__main__":
    answer=input('Group Size? Type press enter for West\'s student population.\n')
    knox_data()
    if answer=='':
        knox_get_my_risk((1443-435)) # The number of West students in 2018-2019 minus the number that went online
    else:
        knox_get_my_risk(int(answer))