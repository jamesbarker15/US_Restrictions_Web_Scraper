# US Sanctions Web Scraper
This program will firstly scrape https://ofac.treasury.gov/sanctions-programs-and-country-information
of all the current sanctions in place, store all known sanctions into a 
text file. 

A cronjob can be applied on refresh.py, to run automatically. What this will then
do is re-scrape the website, download the new contents
into another text file and compare to identify if any restrictions
have been added or removed. 