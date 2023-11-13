from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import pandas as pd
import time
import random #to not be detected as a bot


load_dotenv()
user_id = os.getenv('USER_ID')
password = os.getenv('PASSWORD')

# Set Chrome options for incognito mode
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--log-level=3')  # This should suppress the verbose logging

service = Service(ChromeDriverManager().install())

# Set up the Selenium WebDriver with incognito mode
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the login page
driver.get("https://account.everytime.kr/login")

# Wait for the page to load and for the input fields to be present
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'id')))

# Find the username and password input elements and enter the credentials
username_input = driver.find_element(By.NAME, 'id')
password_input = driver.find_element(By.NAME, 'password')

username_input.send_keys(user_id)
password_input.send_keys(password)

# Find and click the login button
login_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
login_button.click()

# Wait for login to complete by checking for a known element on the home page
# You will need to replace 'unique_element_id' with an actual element that indicates successful login.
print("Login successful!")

# Now navigate to the hotarticles page
driver.get('https://everytime.kr/hotarticles')



def scrape_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.list")))
     # Random delay before scraping articles
    time.sleep(random.uniform(1, 3))
    articles = driver.find_elements(By.CSS_SELECTOR, "article.list")
    data = []
    for article in articles:
        title = article.find_element(By.CSS_SELECTOR, 'h2').text
        content = article.find_element(By.CSS_SELECTOR, 'p').text
        data.append({'title': title, 'content': content})
    return data

# Function to click the 'next' button
def go_to_next_page(driver):
    next_button = driver.find_element(By.LINK_TEXT, '다음')
    next_button.click()

# Scrape the first page
driver.get('https://everytime.kr/hotarticle/p/1')
data = scrape_page(driver)

# Go to the next page and scrape
go_to_next_page(driver)
random_delay = random.uniform(2, 5)  # Random delay between 2 and 5 seconds
time.sleep(random_delay)  # Wait for the next page to load with a random delay
data.extend(scrape_page(driver))

# Quit the driver
driver.quit()

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Get the desktop path for the current user
desktop_path = os.path.join(os.path.expanduser('~'), 'C:/Users/parkj/OneDrive/바탕 화면')

# Define the path for the Excel file on the desktop
excel_path = os.path.join(desktop_path, 'hot_articles.xlsx')

# Save the DataFrame to an Excel file on the desktop
df.to_excel(excel_path, index=False)

print(f"The Excel file has been saved to {excel_path}")