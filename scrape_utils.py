import time, random
from selenium.webdriver.common.keys import Keys
charList = set("ABCDEFGHIJLMNOPQRSTUV")
wordsList = list()
def firstWord(syllable, wordsFile):
    print("Selecting first word in list")
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and line not in wordsList:
                commitWord(line)
                return line
    print("Could not find word in list")
    return "bot failed"

def randomWord(syllable, wordsFile, shortestLength = 4, longestLength = 10):
    print("selecting RANDOM word in list")
    wordsList = [] # lazy mb
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if len(wordsList) == 300: # list getting big
                break
            if syllable in line and line not in wordsList and len(line)>=shortestLength and len(line)<=longestLength:
                wordsList.append(line)
    if len(wordsList) == 0:
        print("Could not find word between lengths "+shortestLength+" and "+longestLength)
        return randomWord(syllable, wordsFile, shortestLength = 0, longestLength=15)
    selectedWord = random.choice(wordsList)
    commitWord(selectedWord)
    return selectedWord

def bestWord(syllable, wordsFile):
    print("selecting BEST word in list")
    wordsList = []
    wordValue = -1
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and getWordValue(line) > wordValue and line not in wordsList:
                wordsList = []
                wordsList.append(line)
                wordValue = getWordValue(line)
            if syllable in line and getWordValue(line) == wordValue:
                wordsList.append(line)
    if len(wordsList) == 0:
        print("could not find word")
        return ""
    bestWord = random.choice(wordsList)
    commitWord(bestWord)
    return bestWord

def longestWord(syllable, wordsFile):
    print("selecting LONGEST word in list")
    longestWord = ""
    wordLength = -1
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and len(line) > wordLength and line not in wordsList:
                longestWord = line
                wordLength = len(line)
    commitWord(longestWord)
    return longestWord

def shortestWord(syllable, wordsFile):
    print("selecting SHORTEST word in list")
    shortestWord = ""
    wordLength = 100
    with open(wordsFile, "r") as words:
        lines = words.readlines()
        for line in lines:
            if syllable in line and len(line) < wordLength and line not in wordsList:
                shortestWord = line
                wordLength = len(line)
    commitWord(shortestWord)
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
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
            except Exception as e:
                print("keys ERROR")
                print(e)
        else:
            return
        typeWait(typeSpeed)
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter ERROR")
            print(e)
    print("printing ACCURATEly")

def outputWordWithTypos(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    print("printing with POSSIBLE TYPOS but CONTINUE TYPING")
    think()
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                typeWrongCharacter(char, input, chanceOfTypoAtEachLetter, characterRandomness)
            except Exception as e:
                print(e)
                print("keys ERROR")
        else:
            return
        typeWait()
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter ERROR")
            print(e)

def outputWordBackspaces(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    print("printing with POSSIBLE TYPOS but SELF CORRECT")
    think()
    for char in word:
        if check_input(driver):
            try:
                input.send_keys(char)
                if (typeWrongCharacter(char, input, chanceOfTypoAtEachLetter, characterRandomness)):
                    typeWait()
                    input.send_keys(Keys.BACKSPACE)
            except Exception as e:
                print("keys ERROR")
                print(e)
        else:
            return
        typeWait()
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter ERROR")
            print(e)

def outputWordRestartAfterMistake(input, word, driver, chanceOfTypoAtEachLetter=.05, characterRandomness=5):
    print("printing with POSSIBLE TYPOS and RESTART")
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
                print("keys ERROR")
                print(e)
        else:
            return
        typeWait()
        counter += 1
    if check_input(driver):
        try:
            input.send_keys(Keys.RETURN)
        except Exception as e:
            print("enter ERROR")
            print(e)

# Returns True if typo is made
def typeWrongCharacter(originalChar, input, chanceOfTypo, characterRandomness):
    if (flipAWeightedCoin(chanceOfTypo)):
        print("making TYPO")
        randomness = random.randint(-1*characterRandomness, characterRandomness)
        wrong = chr(ord(originalChar)+randomness)
        typeWait()
        if wrong.isalpha():
            input.send_keys(wrong)
        else:
            input.send_keys(originalChar)
        return True
    return False

def typeWait(typeSpeed=.1):
    time.sleep(random.uniform(.05, typeSpeed))

def check_input(driver):
    return driver.find_element_by_css_selector("form input").is_displayed() # WE CAN CHECK IF THE DIV OUTSIDE THE INPUT IS VISIBLE

def flipAWeightedCoin(weight=0.5):
    return random.uniform(0,1) < weight
def think(reactionSpeed=0.1, thinkTime=1.5):
    return time.sleep(random.uniform(reactionSpeed,thinkTime))
if __name__ == "__main__":
    pass