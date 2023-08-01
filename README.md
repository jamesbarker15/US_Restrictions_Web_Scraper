# US Sanctions Web Scraper
This program will firstly scrape https://ofac.treasury.gov/sanctions-programs-and-country-information
of all the current sanctions in place, store all known sanctions into a 
text file. 

A cronjob can be applied on refresh.py, to run automatically. What this will then
do is re-scrape the website, download the new contents
into another text file and compare to identify if any restrictions
have been added or removed. If any have been update it will send an email to the recipient notifying them of that fact and 
then overwrite the original sanctions text file meaning it will continuously run without the need for human input. 

# Update

refresh_jira.py has been added. This allows for the creation of a Jira ticket,
on a high priority as a notification instead of email. This will only notify
if there is a change in sanctions. 
