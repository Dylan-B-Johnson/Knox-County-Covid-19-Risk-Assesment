# COVID-19 Risk Assesment
This project has a program, which allows you to view up to date Knox County COVID-19 data, as well as calculate the expected number of people in a 
group of a given size that would have COVID-19, not know about it, and be asymptomatic.

This project scrapes its data from the Knox County Health Department at: https://covid.knoxcountytn.gov/case-count.html.

Prediction assumptions:
"Researchers say anywhere from 25 percent to 80 percent of people with COVID-19 are unaware they have the virus."
--Healthline:   https://www.healthline.com/health-news/50-percent-of-people-with-covid19-not-aware-have-virus
\nPrediction assumes the quartiles, minimum, and maximum frequency of asymptomatic carriers from the above source.
\nPrediction assumes active cases have self-isolated. 
\nPrediction assumes the group has the same prevalence of COVID as all other groups in Knox County.
\nPrediction assumes that asymptomatic carriers don't know they have the virus. 

Dependencies:
- pandas
- requests 
