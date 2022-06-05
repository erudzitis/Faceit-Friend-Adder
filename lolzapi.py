import requests, json
from bs4 import BeautifulSoup

class LOLZAPI:
    def __init__(self, currency, _xfToken):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"})
        self.setCookies()

        self.currency = currency
        self._xfToken = _xfToken

        self.BASE_DOMAIN_URL = "https://lolz.guru/"

    def setCookies(self):
        with open("cookies.txt") as file:
            for line in file:
                splitData = line.split()
                self.session.cookies[splitData[5]] = splitData[6]

    def getInventoryPrice(self, steamId):
        data = {
            "link": steamId,
            "currency": self.currency,
            "app_id": 730,
            "_xfRequestUri": "/market/steam-value",
            "_xfNoRedirect": 1,
            "_xfToken": self._xfToken,
            "_xfResponseType": "json"
        }

        request = self.session.post(self.BASE_DOMAIN_URL + "market/steam-value", data = data)
        requestData = json.loads(request.content)
        requestDataHTML = requestData["templateHtml"] # FilteredInventoryCostValue
        requestDataHTMLBS = BeautifulSoup(requestDataHTML, "lxml")
        soupTargetDiv = requestDataHTMLBS.find("div", {"id": "FilteredInventoryCostValue"})

        if (soupTargetDiv is None):
            return 0

        return float(soupTargetDiv["data-value"])
