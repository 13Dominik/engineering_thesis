import csv

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://allegro.pl/listing?string=suszarka&order=qd'
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

driver.get(url)

# Get all elements with 'href' attribute - links
links = driver.find_elements(By.CSS_SELECTOR, '[href]')

# write to file all links that are 'offers'
for link in links:
    with open('links2.csv', 'a') as file:
        writer = csv.writer(file, delimiter=",")
        if '/oferta/' in str(link.get_attribute('href')):
            writer.writerow([str(link.get_attribute('href'))])

df = pd.read_csv('links2.csv')

# delete every 2 row and save file (problem with allegro source page)
df = df.iloc[::2, :]
df.to_csv('links2.csv', index=False)
