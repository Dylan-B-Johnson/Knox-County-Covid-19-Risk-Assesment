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
		if q==3: label='Q3 Assumption'
		if q==2:
			label='Med Assumption'
			med_west=expect_asymp_infect
		if q==1: label='Q1 Assumption'
		if q==0:
			label='CDC Min Assumption'
			min_west=expect_asymp_infect
		if q==-1:
			label='CDC Current Best Assumption'
		print('----------'+label+' ('+str(asymp_percentage*100)[:4]+'%)----------\nExpected County Asymp\Presymp Infections:\n'+
			  str(asymp_infections)[:6]+' ('+str(asymp_infections/population*100)[:4]+'% of Total County Population)\n')
		print('Expected Asymp\Presymp Ppl in Group:\n'+str(expect_asymp_infect)[:4]+'\n')
		q-=1 
	print('----------Range----------\n'+
		 'Range of Expected Asymp\Presymp Ppl in Group:\n'+str(min_west)[:4]+' - '+str(maximum_west)[:4])

def ask_loop(message, y_or_enter):
	while True:
		answer=input('\n'+message)
		if y_or_enter and (answer=='Y' or answer=='y' or answer=='yes' or answer=='YES' or answer =='yES' or answer=='Yes' or answer=='yeS' or answer=='YeS' or answer=='yEs' or answer=='YEs'):
			return 'y'
		elif y_or_enter and (answer=='N' or answer=='n' or answer=='No' or answer=='NO' or answer =='nO' or answer=='no'):
			return 'n'
		elif answer.isdigit():
			return answer
		else:
			if y_or_enter:
				input('\n"'+answer+'" does not appear to be  valid response. Press any key to continue.\n')
			else:
				input('\n"'+answer+'" Does not appear to be  valid response. Make sure not to use any commas. Press any key to continue.\n')
	
				
if __name__ == "__main__":
	ans_school=ask_loop('Is the group a elementary, middle, or high school? (Type "y" if yes, otherwise, press enter.)\n',True)
	if ans_school=='y':
		ans_school_west=ask_loop('Is this school West High School? (Type "y" if yes, otherwise, press enter.)\n',True)
		if ans_school_west=='y':
			knox_data()
			knox_get_my_risk(True,teachers=82, students=(1443-435)) 
		else:
			teacher_num=ask_loop('Enter the number of teachers at this school:\n',False)
			student_num=ask_loop('Enter the number of students at this school (without commas):\n',False)
			knox_data()
			knox_get_my_risk(True,teachers=int(teacher_num),students=int(student_num))
	else:
		size_ans=ask_loop('Please enter this group\'s size.\n',False)
		knox_data()
		knox_get_my_risk(False,group_size=int(size_ans))
	