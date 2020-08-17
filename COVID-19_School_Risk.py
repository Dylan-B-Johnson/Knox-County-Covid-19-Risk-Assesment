"""
Copyright [2020] [Dylan Johnson]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import csv, io  

# Displays most of the data avaiable from Knox County's Health Department about COVID-19 and
# breaks it down by age group, sex, and race.
def knox_data():
    print('\n\n--------------------Current County Data--------------------\n')
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
def knox_get_my_risk(group_size, is_west):
    
    #gets percent of total cases that are minors and adaults 18-64
    if is_west:
        url = "https://covid.knoxcountytn.gov/includes/covid_summary.csv"
        content_of_csv = requests.get(url).text
    
        for i in csv.reader(io.StringIO(content_of_csv)):
            if i[0]=='0-17':
                minor_cases=int(i[2])
            if i[0]=='18-44':
                adault_to_44_cases=int(i[2])
            if i[0]=='45-64':
                adault_to_64_cases=int(i[2])
            if i[0]=='Total':
                total_cases_real=int(i[2])
        west_teacher_percent=(adault_to_64_cases+adault_to_44_cases)/total_cases_real
        west_student_percent=minor_cases/total_cases_real
    
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
    for asymp_percentage in [0.70,((0.70-0.25)*0.75+0.10),((0.70-0.25)*0.50+0.10),((0.70-0.25)*0.25+0.10),0.10, 0.40]:
        total_infections=active_cases*2.7
        asymp_cases=total_infections*asymp_percentage
        if is_west:
            west_students=asymp_cases/population*(1443-435)*west_student_percent+asymp_cases/population*82*west_teacher_percent
        else:
            west_students=asymp_cases/population*group_size
        if q==4:
            label='CDC Max Assumption'
            maximum_west=west_students
        if q==3: label='Q3 Assumption'
        if q==2:
            label='Med Assumption'
            med_west=west_students
        if q==1: label='Q1 Assumption'
        if q==0:
            label='CDC Min Assumption'
            min_west=west_students
        if q==-1:
            label='CDC Current Best Assumption'
        print('----------'+label+' ('+str(asymp_percentage*100)[:4]+'%)----------\nExpected County Asymp\Presymp Infections:\n'+
              str(asymp_cases)[:6]+' ('+str(asymp_cases/population*100)[:4]+'% of Total County Population)\n')
        print('Expected Asymp\Presymp Ppl in Group:\n'+str(west_students)[:4]+'\n')
        q-=1 
    print('----------Range----------\n'+
         'Range of Expected Asymp\Presymp Ppl in Group:\n'+str(min_west)[:4]+' - '+str(maximum_west)[:4])
       
if __name__ == "__main__":
    answer=input('Group Size? Type press enter for West\'s student population.\n')
    knox_data()
    if answer=='':
        knox_get_my_risk((1443-435+82),True) # The number of West students in 2018-2019, minus the number that went online, plus the number of 2018-2019 teaching staff members.
    else:
        knox_get_my_risk(int(answer),False)
