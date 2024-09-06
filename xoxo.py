from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

# Set up Chrome options to run in headless mode
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver with the specified options
driver = webdriver.Chrome()

# Initialize the WebDriver wait
wait = WebDriverWait(driver, 1)

scraped_data = []

# URL to scrape
url = "https://xoxo-eg.com/products/maybelline-fit-me-concealer?_pos=2&_sid=24379445c&_ss=r"

try:
    # Open the URL
    driver.get(url)

    # Get the product title
    productTitle = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/main/div[1]/div/div[2]/div/div/div[2]/div/div[1]/h1/span'))
    )

    # Get the product prices (assuming multiple prices are present in a list)
    price_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/main/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div'))
    )
    print(price_elements)
    
    # Extract text from each price element
    prices = [price.text for price in price_elements]

    # Append the scraped data
    scraped_data.append({
        'Barcode': "product",
        'Name': productTitle.text,
        'Prices': ', '.join(prices)  # Join multiple prices into a single string
    })

    # Save to CSV
    if os.path.isfile('scraped_data_xoxo.csv'):
        df_scraped = pd.DataFrame(scraped_data)
        df_scraped.to_csv('scraped_data_xoxo.csv', index=False, mode='a', header=False)
    else:
        df_scraped = pd.DataFrame(scraped_data)
        df_scraped.to_csv('scraped_data_xoxo.csv', index=False)

except Exception as e:
    print(e)

# Close the browser
driver.quit()
