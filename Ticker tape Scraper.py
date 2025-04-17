import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the company names from the CSV file
file_path = r'Company.csv'
company_df = pd.read_csv(file_path)
company_names = company_df.iloc[:, 0].tolist()  # Assuming company names start from column B (index 1)

# Automatically download and set up the WebDriver for Microsoft Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Open the base URL
base_url = "https://www.tickertape.in/stocks/reliance-industries-RELI?ref=screener_int-asset-widget"
driver.get(base_url)

# Function to parse and save table data
def parse_and_save_table(soup, statement_type, company_name):
    try:
        print(f"Searching for {statement_type} of {company_name} on page: {driver.title}")
        
        # Identify the table by statement type
        table = soup.find("table", {"data-statement-type": statement_type})
        
        if not table:
            table = soup.find("table")  # Fallback to find any table if the specific one is not found
        
        if table:
            headers = table.find_all('th')
            titles = [header.text for header in headers]

            rows = table.find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                if cols:
                    data.append(cols)

            df = pd.DataFrame(data, columns=titles)
            df.to_csv(f"{company_name}_{statement_type}.csv", index=False)
            print(f"{statement_type.capitalize()} data saved for {company_name}.")
        else:
            print(f"{statement_type.capitalize()} table not found for {company_name}!")
            print("Page HTML snapshot (first 1000 characters):")
            print(soup.prettify()[:1000])

    except Exception as e:
        print(f"Error while parsing {statement_type} for {company_name}: {e}")

# Function to search for a company and scrape the required data
def search_and_scrape(company_name):
    try:
        # Find the search input element
        search_input = driver.find_element(By.ID, "search-stock-input")
        
        # Clear the input field and enter the company name
        search_input.clear()
        search_input.send_keys(company_name)
        
        # Wait for suggestions to appear and select the correct one
        time.sleep(4)
        company_suggestion = driver.find_element(By.XPATH, f"//a[contains(@id, 'stock-suggestion-{company_name.split()[0]}')]")
        company_suggestion.click()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        time.sleep(4)

        # Get the page source and parse the Balance Sheet
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        
        # Click the Balance Sheet tab
        input_element = driver.find_element(By.XPATH, "//input[@name='segment-radio' and @value='balancesheet']")
        driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", input_element)

        # Wait for the balance sheet content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        time.sleep(4)

        # Update the BeautifulSoup object with the new content
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        parse_and_save_table(soup, "balancesheet", company_name)

        # Scroll to Income Statement and click using JavaScript
        input_element_income = driver.find_element(By.XPATH, "//input[@name='segment-radio' and @value='income']")
        driver.execute_script("arguments[0].scrollIntoView(true);", input_element_income)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", input_element_income)

        # Wait for the income statement content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        time.sleep(4)

        # Update the BeautifulSoup object with the new content
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        parse_and_save_table(soup, "income", company_name)

        # Scroll to Cash Flow and click using JavaScript
        input_element_cashflow = driver.find_element(By.XPATH, "//input[@name='segment-radio' and @value='cashflow']")
        driver.execute_script("arguments[0].scrollIntoView(true);", input_element_cashflow)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", input_element_cashflow)

        # Wait for the cash flow content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        time.sleep(4)

        # Update the BeautifulSoup object with the new content
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        parse_and_save_table(soup, "cashflow", company_name)

        # Introduce random short delay
        random_delay = random.randint(1, 4)
        time.sleep(random_delay)

    except Exception as e:
        print(f"Failed to scrape data for {company_name}: {e}")

# Loop through all the companies and scrape data
for company_name in company_names:
    search_and_scrape(company_name)

    # Introduce a random longer delay after scraping data for 10-20 companies
    if company_names.index(company_name) % 10 == 0:
        random_long_delay = random.randint(5, 15)
        time.sleep(random_long_delay)

# Close the WebDriver
driver.quit()
