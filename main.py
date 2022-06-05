import os
import requests
import json

from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

load_dotenv()

# enviroment variables
STORAGE_FILE_NAME = "storage.json"

FACEITAUTH_V = os.getenv("FACEITAPI_AUTHORIZATION")
FACEITHUB_V = os.getenv("FACEIT_HUB_ID")
FACEITUSER_A = os.getenv("FACEITUSER_AUTHORIZATION")

FACEITAPI_BASE_URL = "https://open.faceit.com/data/v4"
FACEITAPI_AUTHORIZATION_KEY = "Bearer {}".format(FACEITAUTH_V)
FACEITAPI_SEARCH_OFFSET = 5 # 1-100

FACEIT_ADD_USER_BASE_URL = "https://api.faceit.com/friend-requests/v1/users/{userId}/requests"
FACEITUSER_KEY = "Bearer {}".format(FACEITUSER_A)

STEAM_INVENTORY_API_BASE_URL = "https://steamcommunity.com/profiles/{steamId}/inventory/json/730/2"
STEAM_API_THROTTLE_DELAY_SECONDS = 60

# script variables
fetchedPlayers = []

def logData(text, type):
    if (type == "SUCCESS"):
        print("\033[92m {}".format(text))
    elif (type == "ERROR"):
        print("\033[91m {}".format(text))
    elif (type == "INFO"):
        print("\033[93m {}".format(text))

@sleep_and_retry
@limits(calls=1, period=STEAM_API_THROTTLE_DELAY_SECONDS)
def requestThrottler():
    return

def fetchFaceitProfiles():
    # Fetching HUB details
    REQUEST_OFFSET = 0

    with open(STORAGE_FILE_NAME, "r+") as storage:
        data = json.load(storage)

        if (FACEITHUB_V in data):
            REQUEST_OFFSET = data[FACEITHUB_V]
            data[FACEITHUB_V] += FACEITAPI_SEARCH_OFFSET
        else:
            data[FACEITHUB_V] = FACEITAPI_SEARCH_OFFSET

        storage.seek(0)
        json.dump(data, storage)

    logData("Updated faceit hub search offset...", "SUCCESS")

    HUBPlayersRequest = requests.get(FACEITAPI_BASE_URL + "/hubs/{}/members?offset={}&limit=5".format(FACEITHUB_V, REQUEST_OFFSET), headers = {"Authorization": FACEITAPI_AUTHORIZATION_KEY});

    if (HUBPlayersRequest.status_code != 200):
        logData("An error occured while searching for players", "ERROR")
        return

    # Fetching faceit players
    fetchedFaceitPlayers = []

    HUBPlayersParsedData = json.loads(HUBPlayersRequest.content);
    HUBPlayersData = HUBPlayersParsedData["items"]

    for playerData in HUBPlayersData:
        currentPlayerFaceitUrl = playerData["faceit_url"].format(lang = "en")
        currentPlayerFaceitId = playerData["user_id"]

        fetchedFaceitPlayers.append({
            "faceit_id": currentPlayerFaceitId,
            "faceit_url": currentPlayerFaceitUrl
        })

    logData("Successfully fetched faceit profiles...", "SUCCESS")

    # Fetching faceit players faceit profiles
    for faceitProfile in fetchedFaceitPlayers:
        faceitProfileRequest = requests.get(FACEITAPI_BASE_URL + "/players/{}".format(faceitProfile["faceit_id"]), headers = {"Authorization": FACEITAPI_AUTHORIZATION_KEY});

        if (faceitProfileRequest.status_code != 200):
            logData("An error occured while fetching faceit profile", "ERROR")
            return

        faceitProfileParsedData = json.loads(faceitProfileRequest.content);
        faceitProfileSteamId = faceitProfileParsedData["steam_id_64"]
        #faceitProfileFriendsIds = faceitProfileParsedData["friends_ids"]

        fetchedPlayers.append({
            "steam_id": faceitProfileSteamId,
            "faceit_id": faceitProfile["faceit_id"],
            "faceit_url": faceitProfile["faceit_url"]
        })

    logData("Successfully fetched player profiles...", "SUCCESS")

def fetchPlayersInventories():
    for player in fetchedPlayers:
        # throttling requests in order to not run into rate limit
        requestThrottler()
        
        logData("Searching inventory for user {}".format(player["steam_id"]), "INFO")
        playerInventoryRequest = requests.get(STEAM_INVENTORY_API_BASE_URL.format(steamId = player["steam_id"]));

        if (playerInventoryRequest.status_code != 200):
            logData("An error occured while fetching players inventory [1]", "ERROR")
            continue

        playerInventoryParsedData = json.loads(playerInventoryRequest.content);
        
        if (not playerInventoryParsedData["success"]):
            logData("An error occured while fetching players inventory [2]", "ERROR")
            continue
        
        playerInventoryDescription = playerInventoryParsedData["rgDescriptions"];

        for descriptionKey in playerInventoryDescription:
            currentDescription = playerInventoryDescription[descriptionKey]

            print(currentDescription["type"])

            if ("Covert" in currentDescription["type"]):
                logData("Found valuable item {}, adding user {}".format(currentDescription["name"], player["faceit_url"]), "SUCCESS");

                queryData = {
                    "users": [player["faceit_id"]],
                    "conversionPoint": "profile"
                }

                friendRequest = requests.post(FACEIT_ADD_USER_BASE_URL.format(player["faceit_id"]), data = queryData, headers = {"Authorization": FACEITUSER_KEY, "Origin": "https://api.faceit.com", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36", "faceit-referer": "new-frontend", "Referer": "https://api.faceit.com/proxy.html"})

                print(friendRequest)


if (__name__ == "__main__"):
    fetchFaceitProfiles()
    fetchPlayersInventories()
