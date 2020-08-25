from time import sleep
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from slack import WebClient
from slack.errors import SlackApiError
from secret import SLACK_API_TOKEN, URL, CHANNEL_ID, USER_ID


# Setting Up Slack API
client = WebClient(token=SLACK_API_TOKEN)

interval = 30 #in minutes
def slack_message(message):
    try:
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            text=message,
            user=USER_ID
        )
        # print(response)
        return response #only prevents warning
    except SlackApiError as e:
        assert e.response["error"]


# My availability
openDays = ["20200824", "20200825", "20200826", "20200827", "20200828",
            "20200831","20200901", "20200902", "20200903", "20200904"]
openHours = ["17:45","11:00","14:00", "18:00" ]


# Patterns
showMoreSelector = '/html/body/div[1]/div[3]/div[2]/div[3]/div/div/button'
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
        # print("Sending notification to Slack...")
        messages = []
        print("Opening the reservation website...")
        browser.get(URL)
        sleep(delay)

        # Selecting a pool
        poolElement = browser.find_element(By.XPATH, showMoreSelector)
        sleep(delay)
        poolElement.click()
        print("Selecting prefered pool... \n")
        sleep(delay)

        # Click to start the reservation process
        bookingElement = browser.find_element(By.XPATH, bookingSelector)
        sleep(delay)
        bookingElement.click()
        sleep(delay)
        print("Exploring available slots...")

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
                        date[4:6]), int(date[6:8])).strftime("%a %B %d")
                    # print(time)
                    sleep(delay)

                    # Select hours slots
                    hourElements = browser.find_elements(
                        By.CSS_SELECTOR, hoursSelector)
                    for hourElement in hourElements:
                        # print(hourElement)
                        hour = hourElement.get_attribute("value")
                        if (hour in openHours):
                            messages.append(f'{time} at {hour} ✅')
                            print(f'{time} at {hour} slot available')
            

    except:
        print("an error occured")

    finally:
        sleep(delay)
        browser.quit()

    print("\nSending available slots to Slack...")

    if (len(messages) != 0):
        # messages.append(f'404 water not found 😥')
        slack_message("🏊 Checking available slots 🏊")
        for message in messages:
            slack_message(message)

    # os.system("cls")
    print(f"{interval} minutes before next search...")
    sleep(interval * 60)
