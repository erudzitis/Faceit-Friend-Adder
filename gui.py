import PySimpleGUI as pysg
import pycountry
import os
import json
import run
import datetime

# Country exception converter
countryConverter = {
    "russia": "Russian Federation"
}

# UI images base64
FACEITLOGO = b"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"

# Init config (create config file if it doesn't exist)
WORKING_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(WORKING_DIRECTORY_PATH + "\config.json"):
    with open("config.json", "w") as config:
        config.write("{}")


# UI definitions
pysg.theme("DarkGrey3")
pysg.set_global_icon(FACEITLOGO)
pysg.set_options(font=("Calibri", 12))

# UI layout storage
menuDef = [["Config", ["Save", "Load"]]]

SettingLayoutColum = [
    [pysg.InputText(key="-CHROMEDRIVERPATH-+"), pysg.FileBrowse(file_types=(("Executable", "*.exe"),))],
    [pysg.Input(enable_events=True, expand_x=True, key="-CHROMEPROFILEPATH-+")]
]

MainLayoutColumn = [
    [pysg.Input(enable_events=True, expand_x=True, key="-ELOFROM-+")],
    [pysg.Input(enable_events=True, expand_x=True, key="-ELOTO-+")],
    [pysg.Input(enable_events=True, expand_x=True, key="-MINIMUMINVENTORYVALUE-+")],
    [pysg.Input(enable_events=True, expand_x=True, key="-FACEITLIVEMATCHLIMIT-+")],
    [pysg.Input(enable_events=True, expand_x=True, key="-TARGETUSERCOUNTRYLIST-+")],
    [pysg.Checkbox("Faceit membership required", key="-FACEITMEMBERSHIPREQUIRED-+")],
    [pysg.Button("Start", expand_x=True, key="-STARTFACEITADDER-")]
]

OutputLayoutColumn = [
    [pysg.Multiline("Log of added users will be displayed here...", size=(1, 5), font=("Calibri", 8), expand_x=True, autoscroll=True, key="-OUTPUTLOG-")],
    [pysg.ProgressBar(max_value=1, size=(1, 20), expand_x=True, key="-OUTPUTPROGRESS-")],
    [pysg.Text("Expected time remaining: ", key="-TIMEREMAINING-")]
]

UILayout = [
    [pysg.Menu(menuDef, background_color="white", font=("Segoe UI", 10))],

    [pysg.Frame("Dependencies", element_justification="left", expand_x=True, relief="groove", layout=SettingLayoutColum)],
    [pysg.Frame("Application options", element_justification="left", expand_x=True, relief="groove", layout=MainLayoutColumn)],
    [pysg.Frame("Output", element_justification="center", expand_x=True, visible=False, relief="groove", layout=OutputLayoutColumn, key="-OUTPUTFRAME-")],
]

# UI element extension
placeholderStorage = {}

def handlePlaceholder(widget, action):
    if (action == "MOUSEENTER"):
        # mouse entered input box, if it matches placeholder, we remove it
        if (widget.get() == placeholderStorage[widget.key]):
            widget.update("")
    elif (action == "MOUSELEAVE"):
        # mouse left input box, if it is empty, add our placeholder
        if (widget.get() == ""):
            widget.update(placeholderStorage[widget.key])

def initPlaceholder(widget, placeholderText):
    placeholderStorage[widget.key] = placeholderText
    widget.set_tooltip(placeholderText)

    if widget.get() == "":
        widget.update(placeholderText)

    # set up a binding to remove placeholder text
    widget.bind("<Enter>", ":MOUSEENTER")
    widget.bind("<Leave>", ":MOUSELEAVE")

# UI init
FAUI = pysg.Window(title="Faceit Adder", layout=UILayout, element_justification="center", finalize=True)

initPlaceholder(FAUI["-CHROMEDRIVERPATH-+"], "Path to chrome driver executable")
initPlaceholder(FAUI["-CHROMEPROFILEPATH-+"], "Path to chrome profile")
initPlaceholder(FAUI["-ELOFROM-+"], "Minimum elo")
initPlaceholder(FAUI["-ELOTO-+"], "Maximum elo")
initPlaceholder(FAUI["-MINIMUMINVENTORYVALUE-+"], "Minimum inventory value")
initPlaceholder(FAUI["-FACEITLIVEMATCHLIMIT-+"], "Faceit live match search limit")
initPlaceholder(FAUI["-TARGETUSERCOUNTRYLIST-+"], "Exluded countries")

# test
import random

largeList = [random.randint(1,10) for _ in range(1000)]

# window loop
while True:
    event, values = FAUI.read()

    # exiting loop on user closing the program (X)
    if (event == pysg.WIN_CLOSED):
        break

    # save config
    if (event == "Save"):
        data = {}

        for UIKey in FAUI.AllKeysDict:
            if (not isinstance(UIKey, str)):
                continue

            if ("+" in UIKey):
                data[UIKey] = FAUI[UIKey].get()

        with open("config.json", "w") as config:
            json.dump(data, config)

    # load config
    if (event == "Load"):
        with open("config.json") as config:
            data = json.load(config)
            
            for UIKey, UIValue in data.items():
                FAUI[UIKey].update(UIValue)

    # placeholder functionality
    if (":" in event):
        eventSplit = event.split(":")
        handlePlaceholder(FAUI[eventSplit[0]], eventSplit[1]) # [widget, action type]

    # start the search, add functionality
    if (event == "-STARTFACEITADDER-"):
        countryNames = values["-TARGETUSERCOUNTRYLIST-+"].split(",")
        updatedCountryAbbrevations = []

        # Fetching country restrictions
        for country in countryNames:
            # Removing any whitespaces that user might have entered after comma, converting to lowercase
            country = country.strip().lower()

            # Checking for specific exceptions
            if (country in countryConverter):
                country = countryConverter[country]

            try:
                data = pycountry.countries.get(name=country)
                updatedCountryAbbrevations.append(data.alpha_2.lower())
            except: 
                continue
            
        # Running functionality
        APPLICATION_INSTANCE = run.Application(FAUI["-ELOFROM-+"].get(), FAUI["-ELOTO-+"].get(), FAUI["-FACEITMEMBERSHIPREQUIRED-+"].get(), FAUI["-MINIMUMINVENTORYVALUE-+"].get(), FAUI["-FACEITLIVEMATCHLIMIT-+"].get(), updatedCountryAbbrevations, FAUI["-CHROMEDRIVERPATH-+"].get(), FAUI["-CHROMEPROFILEPATH-+"].get())
        players = APPLICATION_INSTANCE.getPlayerCollection()

        # Updating output visibility
        FAUI["-OUTPUTFRAME-"].update(visible=True)
        # Updating initial progress bar state
        FAUI["-OUTPUTPROGRESS-"].max_value = len(players)

        for index, player in enumerate(players):
            # Throttling update to every 4 seconds
            event, values = FAUI.read(4000)

            # Fetching inventory value
            inventoryValue = APPLICATION_INSTANCE.playerInventoryValue(player["steam_id"])

            # Updating progress bar, time remaining
            FAUI["-OUTPUTPROGRESS-"].update(max=FAUI["-OUTPUTPROGRESS-"].max_value, current_count=index)

            secondsExpectedRemaining = (FAUI["-OUTPUTPROGRESS-"].max_value - index) * 4
            FAUI["-TIMEREMAINING-"].update("Expected time remaining: {}".format(datetime.timedelta(seconds=secondsExpectedRemaining)))

            # Checking for a match
            if (not APPLICATION_INSTANCE.playerInventoryMatch(inventoryValue)):
                continue

            # Sending friend request
            APPLICATION_INSTANCE.playerFriendRequest(player["faceit_id"])

            # Outputting data to user
            output = "{}, elo: {}, inventory price {}".format(player["faceit_url"], player["faceit_elo"], inventoryValue)

            FAUI["-OUTPUTLOG-"].update(FAUI["-OUTPUTLOG-"].get() + "\n" + output)


FAUI.close()