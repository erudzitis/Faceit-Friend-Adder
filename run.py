
import faceitapi
import lolzapi

class Application:
    def __init__(self, FAUI_ELO_FROM, FAUI_ELO_TO, FAUI_MEMBERSHIP_REQUIRED, FAUI_INVENTORY_VALUE, FAUI_LIVE_MATCH_LIMIT, FAUI_TARGET_COUNTRY_LIST, FAUI_CHROME_DRIVER_PATH, FAUI_CHROME_PROFILE_PATH):
        self.FAUI_ELO_FROM = int(FAUI_ELO_FROM)
        self.FAUI_ELO_TO = int(FAUI_ELO_TO)
        self.FAUI_MEMBERSHIP_REQUIRED = FAUI_MEMBERSHIP_REQUIRED
        self.FAUI_INVENTORY_VALUE = int(FAUI_INVENTORY_VALUE)
        self.FAUI_LIVE_MATCH_LIMIT = int(FAUI_LIVE_MATCH_LIMIT)
        self.FAUI_TARGET_COUNTRY_LIST = FAUI_TARGET_COUNTRY_LIST
        self.FAUI_CHROME_DRIVER_PATH = FAUI_CHROME_DRIVER_PATH
        self.FAUI_CHROME_PROFILE_PATH = FAUI_CHROME_PROFILE_PATH

        self.FACEITAPIINSTANCE = faceitapi.FACEITAPI("3ef86a93-cd01-4b5e-b79b-7f255107e8d4", self.FAUI_TARGET_COUNTRY_LIST, self.FAUI_CHROME_DRIVER_PATH, self.FAUI_CHROME_PROFILE_PATH)
        self.LOLZAPIINSTANCE = lolzapi.LOLZAPI("eur", self.FAUI_CHROME_DRIVER_PATH, self.FAUI_CHROME_PROFILE_PATH)

    def getPlayerCollection(self):
        # Getting ongoing matche
       ongoingMatches = self.FACEITAPIINSTANCE.getLiveMatches(self.FAUI_LIVE_MATCH_LIMIT, 0)
       # Converting data recieved and filtering it to our requirements [payload, eloFrom, eloTo, membershipRequired]
       ongoingMatchPlayers = self.FACEITAPIINSTANCE.collectLiveMatchesData(ongoingMatches["payload"], self.FAUI_ELO_FROM, self.FAUI_ELO_TO, self.FAUI_MEMBERSHIP_REQUIRED)

       return ongoingMatchPlayers

    def playerInventoryValue(self, steamId):
        return self.LOLZAPIINSTANCE.getInventoryPrice(steamId)

    def playerInventoryMatch(self, price):
        return price >= self.FAUI_INVENTORY_VALUE

    def playerFriendRequest(self, faceitId):
        self.FACEITAPIINSTANCE.addFriend(faceitId)
