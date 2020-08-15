# COVID-19 Risk Assesment for Knox County
This project has a program, which allows you to view up to date Knox County COVID-19 data, as well as calculate the expected number of people in a 
group of a given size that would have COVID-19, not know about it, and be asymptomatic.

This project scrapes its data from the Knox County Health Department at: https://covid.knoxcountytn.gov/case-count.html.

Prediction assumptions:
"Researchers say anywhere from 25 percent to 80 percent of people with COVID-19 are unaware they have the virus."
--Healthline:   https://www.healthline.com/health-news/50-percent-of-people-with-covid19-not-aware-have-virus.
Prediction assumes the quartiles, minimum, and maximum frequency of asymptomatic carriers from the aforementioned source.
Prediction assumes active cases have self-isolated. 
Prediction assumes the group has the same prevalence of COVID as all other groups in Knox County.
Prediction assumes that asymptomatic carriers don't know they have the virus. 

Dependencies:
- pandas
- requests 

To Install: 
1) Install the latest version of Python (https://www.python.org/downloads/), checking the "Add to PATH" option on install, and open up command prompt.
2) Run the install.bat file (by double clicking on it).
3) Press "y" twice when prompted.
6) Edit the COVID19_Assesment.bat file (you can use notepad) and repalce the <user> with your username and the <path> with the rest of the path to the
  COVID-19_School_Risk.py file.
