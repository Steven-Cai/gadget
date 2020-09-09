#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

url = "https://parking.evacheckin.com/car_park_booking/select_car_park?siteId=2"

class customer_info:
    def __init__(self):
        self.ski_area = ""
        self.first_name = "";
        self.last_name = "";
        self.phone = "";
        self.email = "";
        self.rego = "";
        self.partysize = "";
        self.date = {};

def customer_info_init(info):
    info.ski_area = "Tūroa"
    info.first_name = "Steven"
    info.last_name = "Cai"
    info.phone = "0224608136"
    info.email = "stevencaiyaohua@gmail.com"
    info.rego = "GEY395"
    info.partysize = "2"
    info.date = {0: '10:00 AM',
                 1: '',
                 2: '',
                 3: '',
                 4: '',
                 5: '',
                 6: ''}

def print_current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def choose_ski_area(b, ski_area):
    if ski_area == "Tūroa":
        b.find_element_by_xpath('//button[text()="Tūroa"]').click()
    elif ski_area == "Whakapapa":
        b.find_element_by_xpath('//button[text()="Whakapapa"]').click()
    b.find_element_by_xpath('//button[text()="Make a booking"]').click()

def select_arrival_time(b, time):
    time_table = b.find_element_by_class_name("form-control")
    time_table.clear()
    #time_table.send_keys("10:00 AM")
    count = 0
    for i in b.find_elements_by_class_name("react-datepicker__time-list-item"):
        count += 1
    print("number of list item")
    print(count)
    xpath = "//*[contains(text(), " + '"' + time + '"' + ")]"
    b.find_element_by_xpath(xpath).click()

def check_available(b):
    booking_slots = b.find_element_by_id('booking-slots-slider')
    status = []
    for booking_status in booking_slots.find_elements_by_css_selector(".mb-3.col-lg.px-2.col-6"):
        # get date
        datetime = booking_status.find_element_by_css_selector(".mb-1.text-center")
        date = datetime.find_element_by_tag_name('time').text
        # get percent
        percent = booking_status.find_element_by_class_name("booking-slot-percent").text
        status.append({'Date': date, 'Percent': percent})

    print('\n'.join(map(str, status)))

def date_select(booking_status):
    add_btn = booking_status.find_element_by_xpath('//button[text()="Add"]')
    if add_btn.is_enabled() == True:
        # start to add dates
        print_current_time()
        print("new parking tickets available")
        datetime = booking_status.find_element_by_css_selector(".mb-1.text-center")
        date = datetime.find_element_by_tag_name('time').text
        print("Date: " + date)
        add_btn.click()
        return True
    else:
        return False

def details_input(b, info):
    print(info.first_name)
    b.find_element_by_id('FirstName').send_keys(info.first_name)
    b.find_element_by_id('LastName').send_keys(info.last_name)

    b.find_element_by_id('Phone').send_keys(info.phone)
    b.find_element_by_id('Email').send_keys(info.email)
    b.find_element_by_id('Rego').send_keys(info.rego)
    b.find_element_by_id('PartySize').clear()
    b.find_element_by_id('PartySize').send_keys(info.partysize)

def parking_book(b, info):
    available = 0
    # choose date
    while True:
        count = 0
        booking_slots = b.find_element_by_id('booking-slots-slider')
        for booking_status in booking_slots.find_elements_by_css_selector(".mb-3.col-lg.px-2.col-6"):
            if info.date[count] == '':
                count += 1;
                continue
            else:
                print("try to choose date, count = ", count)
                if date_select(booking_status):
                    available += 1;
            count += 1
        if available > 0:
            break
        else:
            b.refresh()
            time.sleep(3)

    # choose arrival time
    select_arrival_time(b, "10:30 AM")

    # click Next, then go to next page
    nav_field = b.find_element_by_css_selector(".mt-4.row.row-cols-2")
    nav_field.find_element_by_xpath('//button[text()="Next"]').click()
    time.sleep(1)

    # enter details
    details_input(b, info)

    # button enter details
    b.find_element_by_id('ButtonEnterDetails').click()
    time.sleep(3)

    # click confirmation button
    b.find_element_by_id('ButtonSubmitPreRegistrations').click()
    time.sleep(5)

    # get confirm details
    for elem in b.find_element_by_xpath('.//span[@class="mb-2"]'):
        print(elem.text)


print("Ruapehu Parking Ticket Agency")

# customer information init
info = customer_info()
customer_info_init(info)

# browser init
browser = webdriver.Chrome()
browser.get(url)

# select ski area
choose_ski_area(browser, "Tūroa")
time.sleep(3)

# check parking information
check_available(browser)

# book the parking ticket
parking_book(browser, info)

# quit
#browser.quit()


