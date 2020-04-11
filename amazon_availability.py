import datetime
from selenium import webdriver
import time
import os

FREQUENCY = 1.5  # in minutes
system = "windows"  # "mac" or "windows"
types = ["fresh", "whole food"]

email = email # your login ID email or phone number
password = password


def send_notification(type_):
    print("{} available. Playing sound.".format(type_))
    if system == "windows":
        os.system("powershell -c (New-Object Media.SoundPlayer 'abc.wav').PlaySync();")
    elif system == "mac":
        os.system("afplay abc.wav")


def preprocess(driver):
    driver.get("https://amazon.com")
    time.sleep(1)
    driver.find_element_by_id("nav-cart").click()


def iterate():
    i = 0
    while i < 7:
        for type_ in types:
            if type_ == "fresh":
                preprocess(driver)
                time.sleep(1)
                driver.find_elements_by_xpath("//span[contains(.,'Checkout Amazon Fresh Cart')]")[0].click()
                time.sleep(1)
                driver.find_elements_by_xpath("//a[contains(.,'Continue')]")[0].click()
                no_available_text = 'No delivery windows available. New windows are released throughout the day.'
                time.sleep(5)
                available = no_available_text not in driver.find_elements_by_tag_name("html")[0].text
                if available:
                    send_notification(type_)
                    exit()
                print(str(datetime.datetime.now()) + " {} Not available".format(type_))
            elif type_ == "whole food":
                preprocess(driver)
                time.sleep(1)
                driver.find_elements_by_xpath("//span[contains(.,'Checkout Whole Foods Market Cart')]")[0].click()
                time.sleep(1)
                driver.find_elements_by_xpath("//a[contains(.,'Continue')]")[0].click()
                time.sleep(1)
                driver.find_elements_by_xpath("//span[contains(.,'Continue')]")[0].click()
                no_available_text = 'No delivery windows available. New windows are released throughout the day.'
                time.sleep(5)
                available = no_available_text not in driver.find_elements_by_tag_name("html")[0].text
                if available:
                    send_notification(type_)
                    exit()
                print(str(datetime.datetime.now()) + " {} Not available".format(type_))
        time.sleep(FREQUENCY * 60)
        i += 1

if __name__ == "__main__":
    while True:
        driver = webdriver.Firefox(executable_path="geckodriver") # Download geckodriver.exe here https://github.com/mozilla/geckodriver/releases
        driver.get("https://amazon.com")
        time.sleep(1)
        driver.find_elements_by_link_text("Sign in securely")[0].click()
        driver.find_element_by_id("ap_email").send_keys(email)
        driver.find_element_by_id("continue").click()
        driver.find_element_by_id("ap_password").send_keys(password)
        driver.find_element_by_id("signInSubmit").click()
        iterate()
        driver.close()
        print("Restart...")

