import requests, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class LOLZAPI:
    def __init__(self, currency, driverPath, profilePath):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"})

        self.currency = currency
        self.driverPath = driverPath
        self.profilePath = profilePath[:-8]
        self._xfToken = None

        self.BASE_DOMAIN_URL = "https://lolz.guru/"

        self.scrapeData()       

    def scrapeData(self):
        chromeOptions = Options()
        chromeOptions.add_argument(r"user-data-dir={}".format(self.profilePath))
        chromeOptions.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

        driver = webdriver.Chrome(executable_path=r"{}".format(self.driverPath), options=chromeOptions)
        driver.get(self.BASE_DOMAIN_URL + "market")

        # Waiting for page to load
        WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='XenForo']/body/script[1]")))   

        # Getting data
        data = driver.find_element_by_xpath("//*[@id='XenForo']/body/script[1]")
        dataSplit = data.get_attribute("innerHTML").split("\n")

        for item in dataSplit:
            if ("_csrfToken" in item):
                token = item.split(":")[1]
                token = token[:-1]
                token = token.replace('"', "")
                
                self._xfToken = token

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

        if (request.status_code != 200):
            return 0

        requestData = json.loads(request.content)
        requestDataHTML = requestData["templateHtml"] # FilteredInventoryCostValue
        requestDataHTMLBS = BeautifulSoup(requestDataHTML, "lxml")
        soupTargetDiv = requestDataHTMLBS.find("div", {"id": "FilteredInventoryCostValue"})

        if (soupTargetDiv is None):
            return 0

        return float(soupTargetDiv["data-value"])
