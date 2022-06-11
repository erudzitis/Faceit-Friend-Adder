import requests, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LOLZAPI:
    def __init__(self, currency, _xfToken):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"})

        self.currency = currency
        self._xfToken = _xfToken

        self.BASE_DOMAIN_URL = "https://lolz.guru/"

        self.scrapeData()       

    def scrapeData(self):
        driver = webdriver.Chrome(executable_path=r"C:\Users\ernes\Desktop\chromedriver.exe")
        driver.get(self.BASE_DOMAIN_URL + "market")

        # Waiting for page to load
        WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='XenForo']/body/script[1]")))        

        # Setting request cookies
        self.setCookies(driver.get_cookies())

        # Closing driver
        driver.close()

    def setCookies(self, cookieData):
        for cookie in cookieData:
            self.session.cookies[cookie["name"]] = cookie["value"]

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
