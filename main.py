from time import sleep
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from slack import WebClient
from slack.errors import SlackApiError
from secret import SLACK_API_TOKEN, URL, CHANNEL_ID, USER_ID

client = WebClient(token=SLACK_API_TOKEN)
def slack_message(message):
    try:
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            text=message,
            user=USER_ID
        )
    except SlackApiError as e:
        assert e.response["error"]



openDays = ["20200824", "20200825", "20200826", "20200827", "20200828",
            "20200831","20200901", "20200902", "20200903", "20200904"]

openHours = ["16:30","17:45" ]
# openHours = ["16:30", "18:00"]
# Patterns
showMoreSelector = '/html/body/div[1]/div[3]/div[2]/div[1]/div/div/button'
bookingSelector = '/html/body/div[1]/div[4]/div[3]/div/a[1]'
locationSelector = '/html/body/div[1]/div[4]/div[3]/div/div/div/form/div[2]/div[1]/select/option[2]'
datesSelector = '#dates option:not([disabled])'
hoursSelector = '#heures option:not([disabled]'
delay = 2


while True:
    browser = webdriver.Chrome("./driver/chromedriver")
    print("Browser lauched successfully")
    browser.set_window_size(600, 768)
    os.system("cls")

    try:
        # Open the target URL
        slack_message("===Checking available pool slots===")
        messages = []

        print("Phone notified")

        browser.get(URL)
        sleep(delay)
        print("Website launched")
        # Select a pool
        poolElement = browser.find_element(By.XPATH, showMoreSelector)
        sleep(delay)
        poolElement.click()
        print("Pool selected \n")
        sleep(delay)

        # Click to start the reservation process
        bookingElement = browser.find_element(By.XPATH, bookingSelector)
        sleep(delay)
        bookingElement.click()
        sleep(delay)
        print("Exploring available slots")

        # Select the right municipality
        locationElement = browser.find_element(By.XPATH, locationSelector)
        sleep(delay)
        locationElement.click()

        # Find available the days slot
        sleep(delay)
        dateElements = browser.find_elements(By.CSS_SELECTOR, datesSelector)
        sleep(delay)
        for dateElement in dateElements:
            dateElement.click()
            # Filter the ones that concord with current availabity
            date = dateElement.get_attribute("value")
            if (date in openDays):
                    time = datetime(int(date[:4]), int(
                        date[4:6]), int(date[6:8])).strftime("%B %d")
                    print(time)
                    # print(date[:4], date[4:6], date[6:8])
                    # print(date)
                    sleep(delay)
                    # Select hours slots
                    hourElements = browser.find_elements(
                        By.CSS_SELECTOR, hoursSelector)
                    for hourElement in hourElements:
                        # print(hourElement)
                        hour = hourElement.get_attribute("value")
                        if (hour in openHours):
                            messages.append(f'the {hour} slot is available on {time}')
                            print(f'Available on {time} at {hour}')
    except:
        print("an error occured")

    finally:
        sleep(5)
        browser.quit()

    print("\n Sending notifications available slots on Slack")
    for message in messages:
        slack_message(message)

    print("10 minutes before next search...")
    sleep(1800)
