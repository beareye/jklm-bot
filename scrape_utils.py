import time, random
from selenium.webdriver.common.keys import Keys
def firstWord(syllable, wordsFile):
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line:
                return line
    return "bot failed"

def randomWord(syllable, wordsFile):
    import random
    wordsList = []
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line:
                wordsList.append(line)
    if len(wordsList) == 0:
        return "bot failed"
    return random.choice(wordsList)

def outputWord(input, word, driver):
    time.sleep(random.uniform(.3,3))
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
            except(Exception):
                print("keys error")
                print(Exception)
        else:
            return
        time.sleep(random.uniform(.01,.15))
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except(Exception):
            print("enter error")
            print(Exception)

def check_input(driver):
    return driver.find_element_by_css_selector("form input").is_displayed()