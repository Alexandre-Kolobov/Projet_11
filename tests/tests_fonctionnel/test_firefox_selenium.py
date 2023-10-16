from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_add_endpoint_to_live_server():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:5000/")

    element = driver.find_element(By.NAME, "email")
    element.send_keys("admin@irontemple.com")

    button = driver.find_element(By.TAG_NAME, "button")
    sleep(2)
    button.click()

    link = driver.find_element(By.LINK_TEXT, 'Book Places')
    sleep(2)
    link.click()

    element = driver.find_element(By.NAME, "places")
    # element.click()
    element.send_keys("2")
    button = driver.find_element(By.TAG_NAME, "button")
    sleep(2)
    button.click()

    link = driver.find_element(By.LINK_TEXT, 'Logout')
    sleep(2)
    link.click()
    sleep(2)
    driver.close()
