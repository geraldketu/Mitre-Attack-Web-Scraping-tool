# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup Chrome options
chrome_options = ChromeOptions()
# Uncomment the next line if you want Chrome to run headlessly
# chrome_options.add_argument("--headless")

# Initialize the WebDriver with options
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the website
driver.get("https://attack.mitre.org/")

# Wait for the page to load
time.sleep(5)  # Adjust time as necessary

# Identify all links at the bottom of the page
# Adjust the selector as needed based on the page structure
links = driver.find_elements("css selector", "footer a")

# Placeholder lists for storing extracted data
mitigations_data = []
detections_data = []

# Function to extract data
def extract_data(url, data_list):
    driver.get(url)
    time.sleep(5)  # Wait for page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Here, add logic to parse the page with BeautifulSoup and extract data
    # This is a placeholder example. Customize it as per the actual page structure
    # Example: data_list.append({'column1': value1, 'column2': value2, ...})

for link in links:
    href = link.get_attribute('href')
    if "mitigations" in href:  # Check if the link is for mitigations
        extract_data(href, mitigations_data)
    elif "detections" in href:  # Check if the link is for detections
        extract_data(href, detections_data)

# Convert the lists to pandas DataFrames
df_mitigations = pd.DataFrame(mitigations_data)
df_detections = pd.DataFrame(detections_data)

# Debug: Print DataFrame information before saving (Optional)
print(df_mitigations.head())
print(df_mitigations.info())
print(df_detections.head())
print(df_detections.info())

# Save the DataFrames to CSV files, handling exceptions
try:
    df_mitigations.to_csv('mitigations.csv', index=False)
    print("Mitigations data saved successfully.")
except Exception as e:
    print(f"Error saving mitigations data: {e}")

try:
    df_detections.to_csv('detections.csv', index=False)
    print("Detections data saved successfully.")
except Exception as e:
    print(f"Error saving detections data: {e}")

# Close the WebDriver
driver.quit()
