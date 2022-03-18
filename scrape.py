import time, json, sys, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import scrape_utils

# load settings file
global settings
global driver

with open("./settings.json", "r") as settings_file:
    settings = json.load(settings_file)
print(settings)
driver = webdriver.Chrome()
# setup profile
profile_pic = settings["Profile Pic"] if "Profile Pic" in settings and settings["Profile Pic"] else "cringePic.jpg"
profile_pic = os.getcwd() + "/" + profile_pic
print(f"setting up profile picture to {profile_pic}")
driver.get('https://jklm.fun/')
profile_pic_elem = driver.find_element_by_css_selector("button+input")
profile_pic_elem.send_keys(f"{profile_pic}")
# open the window
print("opening window")
driver.get('https://jklm.fun/'+settings["Lobby Code"])

time.sleep(1) # Wait for response

# set Nickname
print("setting nickname")
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

# Checking which selection algorithm

# Play Game
print("PLAYING GAME")
syllable = ""
while (True):
    time.sleep(1)
    if driver.find_element_by_class_name("joinRound").is_displayed():
        driver.find_element_by_class_name("joinRound").click()
        print("JOINED ROUND")
    if driver.find_element_by_css_selector("form input").is_displayed():
        syllable=driver.find_element_by_class_name("syllable").text
        print("received TEXT: " + syllable)

        # select word and picking algorithm
        wordPickingAlgorithm = scrape_utils.shortestWord
        if (scrape_utils.flipAWeightedCoin(0.1)):
            wordPickingAlgorithm = scrape_utils.bestWord
        elif (scrape_utils.flipAWeightedCoin(0.02)):
            wordPickingAlgorithm = scrape_utils.longestWord
        elif (scrape_utils.flipAWeightedCoin(0.7)):
            wordPickingAlgorithm = scrape_utils.randomWord
        
        result = wordPickingAlgorithm(syllable, "words.txt")
        print("targeted NEXT word: " + result)
        inputElem = driver.find_element_by_css_selector("form input")

        if (scrape_utils.flipAWeightedCoin(0.33)):
            scrape_utils.outputWordWithTypos(inputElem, result, driver)
        elif (scrape_utils.flipAWeightedCoin(0.1)):
            scrape_utils.outputWordRestartAfterMistake(inputElem, result, driver)
        else:
            scrape_utils.outputWordBackspaces(inputElem, result, driver)
        scrape_utils.outputWord(inputElem,result, driver, thinkTime=.1, typeSpeed=.1)
        print()
        print()
        print("="*80)
        

#driver.quit()