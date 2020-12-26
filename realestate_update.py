#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from datetime import date
import time


url = "https://realestate.com.au/buy"

# new properties url
links = []

# get recent days update
day = 3


class search_filter:
    def __init__(self):
        self.postcode = ""
        self.price_max = "";
        self.price_min = "";

def search_filter_init(filter):
    filter.postcode = "4870; "


print("Start to get new properties from realestate")

# anti scrawl setting
mobile_emulation = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# disable some webdriver features for anti scrawl
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(chrome_options=chrome_options)


# Init: set search filter on local
filter = search_filter()
search_filter_init(filter)

driver.get(url)
time.sleep(3)
#print(driver.current_url)
#print(driver.page_source)

# set search filter on page
print("setting filter")
driver.find_element_by_id('where').send_keys(filter.postcode)
time.sleep(2)

# click red "Search" button
print("click Search button")
driver.find_element_by_class_name("rui-search-button").click()
time.sleep(2)

# sorting presentations by date
print("start to set sorting ")

dropdown = driver.find_element_by_css_selector(".Select-control")
time.sleep(3)
dropdown.click()
time.sleep(1)

actions = ActionChains(driver)
actions.send_keys(Keys.ARROW_DOWN)
actions.send_keys(Keys.ENTER)
actions.perform()

time.sleep(2)
print("sorting finished")

# get all results of presentations
results = driver.find_element_by_class_name("tiered-results-container")
#print results.text

# get presentations(properties)
presentations = results.find_elements_by_css_selector(".Box__StyledBox-sc-1mnt3o2-0.gVJskD.results-card.residential-card")
print "size of presentation list: " , len(presentations)

for element in presentations:
    date_section = element.find_element_by_class_name("residential-card__banner-strip")
    post_date = date_section.text
    if post_date == "yesterday":
        post_day = 1
    else:
        post_day = int(post_date[6:7]) # Added 2 days ago => 2
    if post_day > day:
        break
    # get href
    href = element.find_element_by_css_selector(".residential-card__image [href]")
    link =  href.get_attribute('href')
    links.append(link)

# prepare data for reporting
import os
title = 'Realestate: New properties on sale'
subtitle = ''
message = ''
count = 0
for each_link in links:
    # link_string = '<a href = "'
    # link_string = link_string + each_link
    # link_string = link_string +'">' 
    # link_name = each_link.split('.')[2]
    # link_string = link_string + link_name + '</a><br>\n'
    # message += link_string
    message += (each_link + '\n')
    count = count + 1
subtitle = str(date.today()) + ": " + str(count) + " properties"
print title
print subtitle
print message

# send data to Macos notification
def notify(title, subtitle, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" subtitle "{}"'
              """.format(text, title, subtitle))

notify(title, subtitle, message)

#time.sleep(500)

print("The end");

# quit
driver.quit()

