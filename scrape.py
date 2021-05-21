import time, json, subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import scrape_utils

# load settings file
global settings
global driver
inGame = False

with open("./settings.json", "r") as settings_file:
    settings = json.load(settings_file)
print(settings)
#check if we want window even open :do later
driver = webdriver.Chrome()

# open the window
driver.get('https://jklm.fun/'+settings["Lobby Code"])

time.sleep(1) # Wait for response

# set Nickname
name_box = driver.find_element_by_css_selector("form input")
name_box.send_keys(Keys.BACKSPACE)
name_box.send_keys(settings["Nickname"])
time.sleep(1)
search_box = driver.find_element_by_css_selector("form button")
search_box.click()

# Wait for response and loading
time.sleep(5)

# Context switch
driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))

# Play Game
syllable = ""
while (True):
    time.sleep(1)
    if driver.find_element_by_class_name("joinRound").is_displayed():
        driver.find_element_by_class_name("joinRound").click()
        print("JOINED ROUND")
    if driver.find_element_by_css_selector("form input").is_displayed():
        syllable=driver.find_element_by_class_name("syllable").text
        result = scrape_utils.bestWord(syllable, "words.txt")
        print(result)
        inputElem = driver.find_element_by_css_selector("form input")
        scrape_utils.outputWordWithTypos(inputElem, result, driver)
        scrape_utils.outputWordRestartAfterMistake(inputElem, result, driver)

#driver.quit()