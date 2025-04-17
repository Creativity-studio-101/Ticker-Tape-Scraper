# Ticker-Tape-Scraper
Python Code to Scrape company data from Ticker tape 

# How It Works
Reads company names from Missing.csv.

Opens Tickertape using Microsoft Edge WebDriver.

For each company:
Searches and selects the company.
Scrapes Balance Sheet, Income Statement, and Cash Flow data.
Saves each statement as a separate .csv file.

# Notes
Ensure Missing.csv is in the same folder as the script.

Works best with Microsoft Edge installed.

Introduces delays to avoid detection or being blocked by the site.
