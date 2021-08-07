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

import pandas as pd
from datetime import date
import datetime
import requests
import csv, io  
import os
 

# A function to download and save a csv from a url to a folder named after the file name
def save_data(url,path,name,operating_system):
	date=datetime.datetime.today()
	date=date.strftime("%m-%d-%Y")
	if not os.path.exists(name[:-4]):
		os.makedirs(name[:-4])
	r = requests.get(url)  
	if path[-1:]=='/' or path[-2:]=='\\':
		if operating_system=='windows':
			with open(path+name[:-4]+'\\'+date+'_'+name, 'wb') as f:
				f.write(r.content)
		if operating_system!='windows':
			with open(path+name[:-4]+'/'+date+'_'+name, 'wb') as f:
				f.write(r.content)
	else:
		if operating_system=='windows':
			with open(path+'\\'+name[:-4]+'\\'+date+'_'+name, 'wb') as f:
				f.write(r.content)
		if operating_system!='windows':
			with open(path+'/'+name[:-4]++'/'+date+'_'+name, 'wb') as f:
				f.write(r.content)
				
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
    for cat, i in zip(cats[-7:], range(len(cats[-7:]))): 
        if cat!='': print('----------'+cat+'----------')
        for row in data:
            if row[i+1]=='':
                pass
            else: print(row[0]+':\t'+row[i+1])
        if cat!='': print('\n')

# Using a given group size this calculates and displays the expected number of people 
# in that group that have COVID-19 in Knox County, Tennessee
def knox_get_my_risk(is_school, group_size=None, teachers=None, students=None):
	#gets percent of total cases that are minors and adaults 18-64
	if is_school:
		url = "https://covid.knoxcountytn.gov/includes/covid_summary.csv"
		content_of_csv = requests.get(url).text
	
		for i in csv.reader(io.StringIO(content_of_csv)):
			if i[0]=='0-17':
				#minor_cases=int(i[2])
				minor_cases_per_ten_k=float(i[3])
			if i[0]=='18-44':
				#adault_to_44_cases=int(i[2])
				adault_to_44_cases_per_ten_k=float(i[3])
			if i[0]=='45-64':
				adault_to_64_cases_per_ten_k=float(i[3])
				#adault_to_64_cases=int(i[2])
			if i[0]=='Total':
				total_cases_per_ten_k=float(i[3])
				#total_cases_real=int(i[2])
		teacher_percent=(adault_to_64_cases_per_ten_k+adault_to_44_cases_per_ten_k)/(2*total_cases_per_ten_k)
		student_percent=minor_cases_per_ten_k/total_cases_per_ten_k
	
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
		asymp_infections=total_infections*asymp_percentage
		if is_school:
			expect_asymp_infect=asymp_infections/population*students*student_percent+asymp_infections/population*teachers*teacher_percent
		else:
			expect_asymp_infect=asymp_infections/population*group_size
		if q==4:
			label='CDC Max Assumption'
			maximum_west=expect_asymp_infect
			max_county=asymp_infections
		if q==3: label='Q3 Assumption'
		if q==2:
			label='Med Assumption'
			med_west=expect_asymp_infect
		if q==1: label='Q1 Assumption'
		if q==0:
			label='CDC Min Assumption'
			min_west=expect_asymp_infect
			min_county=asymp_infections
		if q==-1:
			best_county=asymp_infections
			best_west=expect_asymp_infect
			label='CDC Current Best Assumption'
		print('----------'+label+' ('+str(asymp_percentage*100)[:4]+'%)----------\nExpected County Asymp Cases:\n'+
			  str(asymp_infections)[:6]+' ('+str(asymp_infections/population*100)[:4]+'% of Total County Population)\n')
		print('Expected Asymp Ppl in Group:\n'+str(expect_asymp_infect)[:4]+'\n')
		q-=1 
	print('----------Range----------\n'+
		 'Range of Expected Asymp Ppl in Group:\n'+str(min_west)[:4]+' - '+str(maximum_west)[:4])
	date=datetime.datetime.today()
	date=date.strftime("%m-%d-%Y")
	csvf=open('C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\historical_predictions.csv','r')
	results=pd.read_csv(csvf)
	csvf.close()
	results_append={'Date':date,'Min_County_Asymp':min_county,'Best_County_Asymp':best_county,'Max_County_Asymp':max_county,'Min_West_Asymp':min_west,'Best_West_Asymp':best_west,'Max_West_Asymp':maximum_west,'Active_Cases':active_cases}
	results=results.append(results_append,ignore_index=True)
	results.to_csv(r'C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\historical_predictions.csv',index = False)
	
	
	west=[['West HS (Special model see readme)'],[[str(active_cases*2.7*0.40/population*(1443-435)*student_percent+active_cases*2.7*0.40/population*82*teacher_percent)[:4]]],
	[str(active_cases*2.7*0.10/population*(1443-435)*student_percent+active_cases*2.7*0.10/population*82*teacher_percent)[:4]+'-'+str(active_cases*2.7*0.70/population*(1443-435)*student_percent+active_cases*2.7*0.70/population*82*teacher_percent)[:4]]]
	
	sizes=[i for i in range(1,10000)]
	estimates=[str(active_cases*2.7*0.40/population*i)[:4] for i in range (1,10000)]
	blank = [None for i in range(1,10001)]
	results={'Group Size':west[0]+sizes,'Best Estimate (Assumes 40% of Infections are Asymp/Presymp)':west[1][0]+estimates,'Estimate Range (Assumes 10-70% of Infections are Asymp/Presymp)':west[2]+[str(active_cases*2.7*0.10/population*i)[:4]+'-'+str(active_cases*2.7*0.70/population*i)[:4] for i in range (1,10000)],('Date Updated: '+date):blank}
	results=pd.DataFrame(data=results)
	results.to_csv(r'C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\daily_risk.csv',index = False)
	
	sizes=[i for i in range(1,3000)]
	estimates=[str(active_cases*2.7*0.40/population*i)[:4] for i in range (1,3000)]
	blank = [None for i in range(1,3001)]
	results={'Group Size':west[0]+sizes,'Best Estimate (Assumes 40% of Infections are Asymp/Presymp)':west[1][0]+estimates,'Estimate Range (Assumes 10-70% of Infections are Asymp/Presymp)':west[2]+[str(active_cases*2.7*0.10/population*i)[:4]+'-'+str(active_cases*2.7*0.70/population*i)[:4] for i in range (1,3000)],('Date Updated: '+date):blank}
	results=pd.DataFrame(data=results)
	results.to_csv(r'C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\daily_risk_lite.csv',index = False)
	
	
	sizes=[i for i in range(1,1100)]
	estimates=[str(active_cases*2.7*0.40/population*i)[:4] for i in range (1,1100)]
	blank = [None for i in range(1,1101)]
	results={'Group Size':west[0]+sizes,'Best Estimate (Assumes 40% of Infections are Asymp/Presymp)':west[1][0]+estimates,'Estimate Range (Assumes 10-70% of Infections are Asymp/Presymp)':west[2]+[str(active_cases*2.7*0.10/population*i)[:4]+'-'+str(active_cases*2.7*0.70/population*i)[:4] for i in range (1,1100)],('Date Updated: '+date):blank}
	results=pd.DataFrame(data=results)
	results.to_csv(r'C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\daily_risk_mobile.csv',index = False)
	
	
	teachers=[]
	students=[]
	blank=[]
	best_estimates=[]
	estimate_ranges=[]
	for teacher_num in range(20,101):
		for student_num in range(200,2001):
			teachers.append(teacher_num)
			students.append(student_num)
			blank.append(None)
			best_estimate=str(active_cases*2.7*0.40/population*student_num*student_percent+active_cases*2.7*0.40/population*teacher_num*teacher_percent)[:4]
			estimate_range=str(active_cases*2.7*0.10/population*student_num*student_percent+active_cases*2.7*0.10/population*teacher_num*teacher_percent)[:4]+'-'+str(active_cases*2.7*0.70/population*student_num*student_percent+active_cases*2.7*0.70/population*teacher_num*teacher_percent)[:4]
			best_estimates.append(best_estimate)
			estimate_ranges.append(estimate_range)
	
	results={'School Students':students,'School Teachers':teachers,'Best Estimate (Assumes 40% of Infections are Asymp/Presymp)':best_estimates,'Estimate Range (Assumes 10-70% of Infections are Asymp/Presymp)':estimate_ranges,('Date Updated: '+date):blank}
	results=pd.DataFrame(data=results)
	results.to_csv(r'C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\daily_school_risk_huge.csv',index = False)
	
	
	
 #   results={'Date':date,'Min_County_Asymp':[min_county],'Best_County_Asymp':[best_county],'Max_County_Asymp':[max_county],'Min_West_Asymp':[min_west],'Best_West_Asymp':[best_west],'Max_West_Asymp':[maximum_west]}
  #  results=pd.DataFrame(data=results)
   # results.to_csv(r'C:\Users\maxbear123\Documents\Python_Scripts\historical_predictions.csv',index = False)
	   
if __name__ == "__main__":
	knox_get_my_risk(True,teachers=82, students=(1443-435))  # The number of West students in 2018-2019, minus the number that went online, plus the number of 2018-2019 teaching staff members.
	path='C:\\Users\\maxbear123\\Documents\\Python_Scripts\\Knox-County-Covid-19-Risk-Assesment\\'
	save_data('https://covid.knoxcountytn.gov/includes/covid_cases.csv',path,'hist_covid_cases.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/covid_gender.csv',path,'hist_covid_gender.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/covid_age.csv',path,'hist_covid_age.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/covid_tests.csv',path,'hist_covid_tests.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/covid_summary.csv',path,'hist_covid_summary.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/race1.csv',path,'hist_race1.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/race2.csv',path,'hist_race2.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/covid_bed_capacity.csv',path,'hist_covid_bed_capacity.csv','windows')
	save_data('https://covid.knoxcountytn.gov/includes/covid_surge_capacity.csv',path,'hist_covid_surge_capacity.csv','windows')
