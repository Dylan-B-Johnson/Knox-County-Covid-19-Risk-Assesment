# COVID-19 Risk Assesment for Knox County
COVID-19_School_Risk.py allows you to view the latest Knox County COVID-19 data, as well as calculate the expected number of people in a 
group of a given size that would have COVID-19 and be asymptomatic.

This project scrapes its data from the Knox County Health Department at: https://covid.knoxcountytn.gov/case-count.html at the time the program is run.

###  Assumption Basis:
* As of July 10, in the CDC's 5 Pandemic Scenarios (https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html), they describe 10% of cases being asymptomatic carriers as their lower-bound estimate, 40% as their best estimate, and 70% as their upper-bound estimate. 

### Prediction Assumptions:
1) This program makes six different predictions, assuming that 10% (the given minium), 21.2% (Q1), 32.4% (Medium), 43.7% (Q3), 70.0% (the given maximum), and 40% (the best given estimate) of COVID cases are asymptomatic carriers. 
2) The prediction assumes that active cases have self-isolated and are therefore of no concern.
3) The prediction assumes that the group in question has the same prevalence of COVID as all other groups in Knox County.
4) The prediction assumes that asymptomatic carriers don't know they have the virus. 
5) If applicable, the prediction assumes that the population of West High School is 1090 people (1443 students + 82 teaching staff - 435 students that chose the online option). The student and teaching staff numbers are for the 2018-2019 school year from https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1&DistrictID=4702220&SchoolPageNum=6&ID=470222000822.
* Note: The CDC's estimates are for asymptomatic carriers, not all those that don't know they have the virus, which would include presymptomatic cariers, so these predictions might be a bit lower than they should be.

### Formula for Prediction:
* Predicted Total Asymptomatic Cases in the County = ((Current Active Cases)/(1-Assumed Asymptomatic Carrier Percentage (as a decimal)))-Current Active Cases
* Predicted Asymptomatic Cases in a Group of Size N = Predicted Total Asymptomatic Cases in the County/Current County Population\*N

### Dependencies:
* requests 

### To Install on Windows: 
1) Download and install the latest version of Python (https://www.python.org/downloads/), checking the "Add to PATH" option on install. This WILL NOT WORK if you have not checked the "Add to PATH" option, which is not checked by default.
2) Download all files in the repository.
3) Run the install.bat file (by double clicking on it).
4) Press the "y" key when prompted.
5) If this worked you can delete the install.bat file.
6) You can now check up on the data and enter any group size you want by simpily double clicking on the COVID-19_School_Risk.py file (if this asks for an application to open it with select Python3.8).

### To Install on Mac OS:
1) Download and install the latest version of Python (https://www.python.org/downloads/), checking the "Add to PATH" option on install. This WILL NOT WORK if you have not checked the "Add to PATH" option, which is not checked by default.
2) Download COVID-19_School_Risk.py
3) Press Command + Space and search for "terminal". Press enter to open it.
4) Type '`pip install requests`' and press enter. 
5) Press the "y" key when prompted.
6) You can now check up on the data and enter any group size you want by simpily double clicking on the COVID-19_School_Risk.py file (if this asks for an application to open it with select Python3.8).

* Note: If you plan to use Python for anything else, I would recommend installing anaconda to manage your Python packages using conda environments.
### To Do:
- [ ] Schedule a batch script to write and upload the daily best prediction and prediction range for the West HS and the county.
### License:
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
