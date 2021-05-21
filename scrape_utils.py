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

def outputWord(input, word, driver, thinkTime=1.5, typeSpeed=.15):
    
    think(0,thinkTime)
    if (not check_input(driver)):
        return
    print("Printing accurately")
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
            except Exception as e:
                print("keys error")
                print(e)
        else:
            return
        typeWait(typeSpeed)
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter error")
            print(e)

def outputWordWithTypos(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    print("Printing with possible typos but continue typing")
    think()
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                typeWrongCharacter(char, input, chanceOfTypoAtEachLetter, characterRandomness)
            except Exception as e:
                print(e)
                print("keys error")
        else:
            return
        typeWait()
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter error")
            print(e)

def outputWordBackspaces(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    print("Printing with possible typos but self correct")
    think()
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                if (typeWrongCharacter(char, input, chanceOfTypoAtEachLetter, characterRandomness)):
                    typeWait()
                    input.send_keys(Keys.BACKSPACE)
            except Exception as e:
                print("keys error")
                print(e)
        else:
            return
        typeWait()
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter error")
            print(e)

def outputWordRestartAfterMistake(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    print("Printing with possible typos and restart")
    think()
    counter = 0 # remember length of word typed
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                if (typeWrongCharacter(char, input, chanceOfTypoAtEachLetter, characterRandomness)):
                    typeWait()
                    for i in range(counter+2): # the typo and the current character as well
                        typeWait(.05)
                        input.send_keys(Keys.BACKSPACE)
                    return
            except Exception as e:
                print("keys error")
                print(e)
        else:
            return
        typeWait()
        counter += 1
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter error")
            print(e)

# Returns True if typo is made
def typeWrongCharacter(originalChar, input, chanceOfTypo, characterRandomness):
    if (flipAWeightedCoin(chanceOfTypo)):
        print("making typo")
        randomness = random.randint(-1*characterRandomness, characterRandomness)
        wrong = chr(ord(originalChar)+randomness)
        typeWait()
        if wrong.isalpha():
            input.send_keys(wrong)
        else:
            print("caught non alpha char")
            input.send_keys(originalChar)
        return True
    return False

def typeWait(typeSpeed=.1):
    time.sleep(random.uniform(.05, typeSpeed))

def check_input(driver):
    return driver.find_element_by_css_selector("form input").is_displayed()

def flipAWeightedCoin(weight=0.5):
    return random.uniform(0,1) < weight
def think(reactionSpeed=0.1, thinkTime=1.5):
    return time.sleep(random.uniform(reactionSpeed,thinkTime))
if __name__ == "__main__":
    commitWord("QUEENSZ")
    print(charList)
    commitWord("POT")
    print(charList)
    commitWord("ABCDEFGHIJLMNOPQRSTUV")
    print(charList)