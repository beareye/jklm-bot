import time, random
from selenium.webdriver.common.keys import Keys
charList = set("ABCDEFGHIJLMNOPQRSTUV")
wordsList = list()
def firstWord(syllable, wordsFile):
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line:
                return line
    return "bot failed"

def randomWord(syllable, wordsFile):
    import random
    wordsList = [] # lazy mb
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line:
                wordsList.append(line)
    if len(wordsList) == 0:
        return "bot failed"
    return random.choice(wordsList)

def bestWord(syllable, wordsFile):
    bestWord = ""
    wordValue = -1
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and getWordValue(line) > wordValue and line not in wordsList:
                bestWord = line
                wordValue = getWordValue(line)
    commitWord(bestWord)
    return bestWord

def longestWord(syllable, wordsFile):
    longestWord = ""
    wordLength = -1
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and len(line) > wordLength:
                longestWord = line
                wordLength = len(line)
    return longestWord

def shortestWord(syllable, wordsFile):
    shortestWord = ""
    wordLength = 100
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and len(line) < wordLength:
                shortestWord = line
                wordLength = len(line)
    return shortestWord

def getWordValue(word):
    return len(set(word).intersection(charList))
def commitWord(word):
    global charList
    charList=set(charList).difference(set(word))
    wordsList.append(word)
    if len(charList) == 0:
        charList = set("ABCDEFGHIJLMNOPQRSTUV")


def outputWord(input, word, driver, thinkTime=1.5, typeDelay=.15):
    time.sleep(random.uniform(0,thinkTime))
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
            except(Exception):
                print("keys error")
                print(Exception)
        else:
            return
        time.sleep(random.uniform(0,typeDelay))
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except(Exception):
            print("enter error")
            print(Exception)

def outputWordWithTypos(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    time.sleep(random.uniform(0,1.5))
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                if (random.uniform(0,1) < chanceOfTypoAtEachLetter):
                    randomness = random.randint(-1*characterRandomness, characterRandomness)
                    input.send_keys(chr(ord(char)+randomness))
            except(Exception):
                print("keys error")
        else:
            return
        time.sleep(random.uniform(.01,.15))
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except(Exception):
            print("enter error")
def outputWordBackspaces(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    time.sleep(random.uniform(0,0.01))
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                if (random.uniform(0,1) < chanceOfTypoAtEachLetter):
                    randomness = random.randint(-1*characterRandomness, characterRandomness)
                    input.send_keys(chr(ord(char)+randomness))
                    time.sleep(random.uniform(.01,.1))
                    input.send_keys(Keys.BACKSPACE)
            except(Exception):
                print("keys error")
        else:
            return
        time.sleep(random.uniform(.01,.1))
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except(Exception):
            print("enter error")

def outputWordRestartAfterMistake(input, word, driver, chanceOfTypoAtEachLetter=.10, characterRandomness=5):
    time.sleep(random.uniform(0,.1))
    counter = 0
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                if (random.uniform(0,1) < chanceOfTypoAtEachLetter):
                    randomness = random.randint(-1*characterRandomness, characterRandomness)
                    input.send_keys(chr(ord(char)+randomness))
                    for i in range(counter+2):
                        time.sleep(random.uniform(.03,.07))
                        input.send_keys(Keys.BACKSPACE)
                    return outputWord(input, word, driver, thinkTime=.15, typeDelay=.1)
            except(Exception):
                print("keys error")
        else:
            return
        time.sleep(random.uniform(.01,.15))
        counter += 1
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except(Exception):
            print("enter error")

def check_input(driver):
    return driver.find_element_by_css_selector("form input").is_displayed()

if __name__ == "__main__":
    commitWord("QUEENSZ")
    print(charList)
    commitWord("POT")
    print(charList)
    commitWord("ABCDEFGHIJLMNOPQRSTUV")
    print(charList)