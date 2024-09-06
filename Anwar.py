from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from tqdm import tqdm

# Read the CSV file into a DataFrame
df = pd.read_csv('products.csv')

# Extract specific columns
barcodes = df['Barcode'].tolist()

# Set up Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver with the specified options
# service = Service(executable_path='path/to/chromedriver')  # Specify the path to your chromedriver
driver = webdriver.Chrome( options=chrome_options)

# Initialize the WebDriver wait
wait = WebDriverWait(driver, 1)

scraped_data = []

# Initialize the progress bar
for product in tqdm(barcodes, desc='Processing Products', unit='product'):
    try:
        # Search for the product in the URL using the barcode
        driver.get(f"https://anwar.store/search?type=product&q={product}")

        # Then click on the first product
        productLink = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="MainContent"]/div/div/div[1]/div/div/div/div/div[2]/a'))
        )
        productLink.click()

        # Get the product title
        productTitle = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ProductSection-product-template-default"]/div/div[1]/div[2]/h1/span'))
        )

        # Get the product price
        productPrice = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/div[1]/div/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[3]'))
        )
        print(productPrice)

        # Get the product availability
        productAvailability = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ProductSection-product-template-default"]/div/div[1]/div[2]/div[2]/div[2]/span'))
        )

    
        # Append the scraped data
        scraped_data.append({
            'Barcode': product,
            'Name': productTitle.text,
            'Price': productPrice.text,
            'Availability': productAvailability.text
        })

    except Exception as e:
        continue

# Save to CSV after each product
if os.path.isfile('scraped_data.csv'):
    df_scraped = pd.DataFrame(scraped_data)
    df_scraped.to_csv('scraped_data.csv', index=False, mode='a', header=False)
else:
    df_scraped = pd.DataFrame(scraped_data)
    df_scraped.to_csv('scraped_data.csv', index=False)

# Close the browser
driver.quit()
