import json

settingsTitleList = ["Nickname", "Delay (in seconds)", "Lobby Code"]
settings = {}
for settingsName in settingsTitleList:
    print("Enter " + settingsName + ": ")
    response = input()
    settings[settingsName] = response

with open('settings.json', 'w+') as settingsFile:
    json.dump(settings, settingsFile)
    