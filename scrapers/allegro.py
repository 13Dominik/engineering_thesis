import random
import time
from typing import List
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from write_data_to_csv import write_row_to_csv
from validate_link import check_if_article_in_base, check_has_proper_end

""" 
To reduce imbalance in dataset choose only reviews with specific score. 
i.e. [1,2,3] -> to dataset will be only added reviews with score 1,2 or 3.
"""
RATINGS_TO_DOWNLOAD = [1, 2, 3, 4]
def delay(a, b) -> None:
    """
    Random delay (2 - 8 [s]) between interactions on website to mimic human delay
    """
    time.sleep(random.randint(a, b))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        link = input("Type allegro link: >>> ")
        link = check_has_proper_end(link)
    else:
        link = sys.argv[1]

    link = check_has_proper_end(link)
    # Adding options to mimic real user
    options = webdriver.ChromeOptions()
    #options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    #options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    # open page
    driver.get(link)
    delay(5, 8)

    # Accept privacy policy
    ok_button_xpath = """//*[@id="opbox-gdpr-consents-modal"]/div/div[2]/div/div[2]/button[1]"""
    ok_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ok_button_xpath)))
    ok_button.click()
    delay(5, 8)

    # Get auction title
    title = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-box-name="ProductReviewsTitle"]')))

    # Validate article based on auction title. Check if not reviews of auction in database
    check_if_article_in_base(title.text)
    delay(5, 7)

    # Add firstly loaded reviews
    reviews = driver.find_elements(By.XPATH, "//div[@itemprop='review']")
    ratings = driver.find_elements(By.CSS_SELECTOR, "meta[itemprop='ratingValue']")
    for review, rating in zip(reviews[1:], ratings[2:]):
        row = []
        row.append(review.text.split("\n")[2])  # review
        # Check if this one should be added to dataset
        if int(rating.get_attribute('content')) in RATINGS_TO_DOWNLOAD:
            row.append(rating.get_attribute('content'))  # rating
        else:
            continue
        row.append(title.text)  # title of auction
        write_row_to_csv('../data/allegro/rtvagd/data.csv', row)

    # Go to new loaded reviews in next iteration
    max_reviews = len(reviews) - 2
    max_ratings = len(ratings) - 2

    # expand the list of reviews
    has_more_reviews = True
    while has_more_reviews:
        try:
            ok_button = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Zobacz więcej opinii')]")))
            ok_button.click()
            delay(10, 15)
            reviews = driver.find_elements(By.XPATH, "//div[@itemprop='review']")
            ratings = driver.find_elements(By.CSS_SELECTOR, "meta[itemprop='ratingValue']")
            for review, rating in zip(reviews[max_reviews:], ratings[max_ratings:]):
                row = []
                row.append(review.text.split("\n")[2])  # review
                # Check if this one should be added to dataset
                if int(rating.get_attribute('content')) in RATINGS_TO_DOWNLOAD:
                    row.append(rating.get_attribute('content'))  # rating
                else:
                    continue
                row.append(title.text)  # title of auction
                write_row_to_csv('../data/allegro/rtvagd/data.csv', row)
            # Go only for new loaded reviews
            max_reviews = len(reviews)
            max_ratings = len(ratings)
        # If no more reviews (end of page)
        except:
            has_more_reviews = False
