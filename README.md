# Ticker-Tape-Scraper
Python Code to Scrape company data from Ticker tape 

# How It Works
1) Reads company names from Missing.csv.

2) Opens Tickertape using Microsoft Edge WebDriver.

3) For each company:

i) Searches and selects the company.

ii) Scrapes Balance Sheet, Income Statement, and Cash Flow data.

iii) Saves each statement as a separate .csv file.

# Notes
Ensure Company.csv is in the same folder as the script.

Works only with Microsoft Edge installed.

Introduces delays to avoid detection or being blocked by the site.
