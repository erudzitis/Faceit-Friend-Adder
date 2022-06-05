# init
from dotenv import load_dotenv
load_dotenv()

import faceitapi
import lolzapi
import colors
import os
from ratelimit import limits, sleep_and_retry

# API instances
faceitApiInstance = faceitapi.FACEITAPI(os.getenv("FACEITAPI_AUTHORIZATION"), os.getenv("FACEITUSER_AUTHORIZATION"), os.getenv("FACEIT_ID"))
lolzApiInstance = lolzapi.LOLZAPI("eur", os.getenv("LOLZ__xfToken"))
colorsInstance = colors.COLORS()

# Globals
REQUIRED_USER_INVENTORY_PRICE = float(os.getenv("USER_INVENTORY_PRICE"))
LIVE_MATCH_LIMIT = int(os.getenv("FACEIT_LIVE_MATCH_SEARCH_LIMIT"))

# Methods
@sleep_and_retry
@limits(calls=1, period=15)
def requestThrottler():
    return

def runScript():
    print("{c}[FACEIT-ADDER-SCRIPT] Fetching ongoing live matches...".format(c = colorsInstance.WARNING))
    ongoingMatches = faceitApiInstance.getLiveMatches(LIVE_MATCH_LIMIT, 0) # Getting ongoing matches
    
    print("{c}[FACEIT-ADDER-SCRIPT] Converting and filtering data...".format(c = colorsInstance.WARNING))
    ongoingMatchPlayers = faceitApiInstance.collectLiveMatchesData(ongoingMatches["payload"], 1000, 3000, False) # Converting data recieved and filtering it to our requirements [payload, eloFrom, eloTo, membershipRequired]

    print("{c}[FACEIT-ADDER-SCRIPT] Starting to process collected players...".format(c = colorsInstance.WARNING))
    for player in ongoingMatchPlayers:
        # Throttling request to lolz team web api to 10 second intervals
        requestThrottler()
        playerInventoryPrice = lolzApiInstance.getInventoryPrice(player["steam_id"])
        matchFound = playerInventoryPrice >= REQUIRED_USER_INVENTORY_PRICE

        print("{c}[FACEIT-ADDER-SCRIPT] {faceit_url}, elo: {faceit_elo}, inventory price {inventory_price}".format(c = colorsInstance.OKGREEN if matchFound else colorsInstance.FAIL, faceit_url = player["faceit_url"], faceit_elo = player["faceit_elo"], inventory_price = playerInventoryPrice))

        if (not matchFound):
            continue

        print("{c}[FACEIT-ADDER-SCRIPT] Adding player...".format(c = colorsInstance.OKGREEN))
        addPlayer = faceitApiInstance.addFriend(player["faceit_id"])

if (__name__ == "__main__"):
    runScript()