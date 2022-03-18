import json

settingsTitleList = ["Nickname", "Lobby Code", "Profile Pic"]
settings = {}
for settingsName in settingsTitleList:
    print("Enter " + settingsName + ": ")
    response = input()
    settings[settingsName] = response

with open('settings.json', 'w+') as settingsFile:
    json.dump(settings, settingsFile)
    