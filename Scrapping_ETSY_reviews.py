# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:09:50 2021

@author: khitish sahu
"""

#Extracting review data from Etsy.com
#importing all the required libraries
import pandas as pd #for reading and writing dataframes
from bs4 import BeautifulSoup # for webscrapping which needs extraction of data
from time import sleep # for adding delays
from selenium import webdriver #for webscrapping which needs input and clicks
import sqlite3 as sql # for loading the data to a sql database

#Declaring variables
urls = []
product_urls = []
list_of_reviews = []


# Each page urls
for i in range(1, 225):
    urls.append(f"https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&explicit=1&page={i}")

# Scrapping each product's urls | 16,064 products
for url in urls:
    #driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(r"C:\Users\khsahu\Downloads\Installables\chromedriver.exe")
    driver.get(url)
    sleep(5)
    for i in range(1, 65):
        product = driver.find_element_by_xpath(f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div/ul/li[{i}]/div/a')
        #print(product.get_attribute('href'))
        product_urls.append(product.get_attribute('href'))

# Scrapping each product's reviews     
#driver = webdriver.Chrome(executable_path='chromedriver.exe')  
driver = webdriver.Chrome(r"C:\Users\khsahu\Downloads\Installables\chromedriver.exe")
for product_url in product_urls[15:]:
    try:
        driver.get(product_url)
        sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html,'html')
        for i in range(4):
            try:
                list_of_reviews.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
            except:
                continue
        while(True):
            try:
                next_button = driver.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a[contains(@href, "https")]')
                                                            #//*[@id="reviews"]/div[2]/nav/ul/li[6]/a/span[2]/svg , making it dynamic by removing li[6] with last()
                if next_button != None:
                    next_button.click()
                    sleep(5)
                    html = driver.page_source
                    soup = BeautifulSoup(html,'html')
                    for i in range(4):
                        try: 
                            list_of_reviews.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
                        except:
                            continue
            except Exception as e:
                print('finsish : ', e)
                break
    except:
        continue
            
scrappedReviewsAll = pd.DataFrame(list_of_reviews, index = None, columns = ['reviews'])         
scrappedReviewsAll.to_csv('scrappedReviews.csv')


df = pd.read_csv('scrappedReviews.csv')
conn = sql.connect('scrappedReviewsAll.db')
df.to_sql('scrappedReviewsAllTable', conn)   