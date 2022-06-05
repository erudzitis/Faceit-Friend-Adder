import requests
import json

class FACEITAPI:
    def __init__(self, API_KEY, WEB_API_KEY, MY_FACEIT_ID):
        self.API_KEY = API_KEY
        self.WEB_API_KEY = WEB_API_KEY
        self.MY_FACEIT_ID = MY_FACEIT_ID

        self.LIVE_MATCHES_BASE_URL = "https://api.faceit.com/match/v1/matches/list?game=csgo&region=EU&state=SUBSTITUTION&state=CAPTAIN_PICK&state=VOTING&state=CONFIGURING&state=READY&state=ONGOING&state=MANUAL_RESULT&state=PAUSED&state=ABORTED&limit={limit}&entityType=matchmaking&offset={offset}"
        self.PLAYER_INFO_BASE_URL = "https://open.faceit.com/data/v4/players/{faceit_id}"
        self.ADD_FRIEND_BASE_URL = "https://api.faceit.com/friend-requests/v1/users/{faceit_id}/requests"
        
        self.API_HEADERS = {"Authorization": "Bearer {}".format(self.API_KEY)}
        self.WEB_HEADERS = {"Authorization": "Bearer {}".format(self.WEB_API_KEY), "Origin": "https://api.faceit.com", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36", "faceit-referer": "new-frontend", "Referer": "https://api.faceit.com/proxy.html"}

    def getLiveMatches(self, limit, offset):
        request = requests.get(self.LIVE_MATCHES_BASE_URL.format(limit = limit, offset = offset), headers = self.WEB_HEADERS)

        return json.loads(request.content)

    def collectLiveMatchesData(self, payload, eloFrom, eloTo, membershipRequired):
        data = []

        for match in payload:
            for teamFraction in match["teams"]:
                for playerData in match["teams"][teamFraction]["roster"]:
                    request = requests.get(self.PLAYER_INFO_BASE_URL.format(faceit_id = playerData["id"]), headers = self.API_HEADERS)
                    requestData = json.loads(request.content)

                    playerFaceitElo = requestData["games"]["csgo"]["faceit_elo"]
                    playerMemberships = requestData["memberships"]

                    # Filtering out players that are not in our required elo range
                    if (playerFaceitElo > eloTo or playerFaceitElo < eloFrom):
                        continue

                    # Filtering out players that don't meet membership criteria
                    if (membershipRequired and "free" in playerMemberships):
                        continue

                    data.append({"steam_id": requestData["steam_id_64"], "faceit_id": playerData["id"], "faceit_url": requestData["faceit_url"].format(lang = "en"), "faceit_elo": playerFaceitElo})

        return data

    def addFriend(self, friendFaceitId):
        data = {
            "users": [friendFaceitId],
            "conversionPoint": "profile"
        }

        request = requests.post(self.ADD_FRIEND_BASE_URL.format(faceit_id = self.MY_FACEIT_ID), data = json.dumps(data).encode("utf-8"), headers = self.WEB_HEADERS)

        return json.loads(request.content)
