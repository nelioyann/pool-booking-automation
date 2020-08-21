from time import sleep
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
# keyboard = Controller()
from selenium.webdriver.support.ui import WebDriverWait


url = "https://reservations.lille.fr/event/piscines"

browser = webdriver.Chrome("./driver/chromedriver")



# Patters
showMore = '/html/body/div[1]/div[3]/div[2]/div[1]/div/div/button'
bookButton = '/html/body/div[1]/div[4]/div[3]/div/a[1]'
homeLink = '/html/body/nav/div/a[1]/h3'
locationSelect = '/html/body/div[1]/div[4]/div[3]/div/div/div/form/div[2]/div[1]/select'
mylocation = '/html/body/div[1]/div[4]/div[3]/div/div/div/form/div[2]/div[1]/select/option[2]'

try:
    browser.get(url)
    # password_field = browser.find_element(By.XPATH, '//*[@id="password"]')
    sleep(2)
    poolElement =  browser.find_element(By.XPATH, showMore)
    sleep(2)
    print(poolElement)
    poolElement.click()
    sleep(2)
    bookingElement =  browser.find_element(By.XPATH, bookButton)
    sleep(2)
    print(bookingElement)
    bookingElement.click()

    sleep(2)
    locationElement =  browser.find_element(By.XPATH, mylocation)
    sleep(2)
    print(locationElement)
    locationElement.click()

finally:
    sleep(10)
    browser.quit()