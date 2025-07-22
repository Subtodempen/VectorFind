from bs4 import BeautifulSoup 
from selenium import webdriver

import requests

# scraper should have a hiarachial structure by first being able to scrape the simplest page with the addres image combo
# And then functionailty to find and locate the pages deal with securty roatte ips etc..

# First create a single function that parses a page like: https://www.rightmove.co.uk/house-prices/details/ed1ef3cd-37dd-45c1-8a70-8fdb18391462?id=media0

# ALl scraping functionailty will extend from this function
def parseBasicPage(pageHTML) -> tuple[str, list]:
    soupEngine = BeautifulSoup(pageHTML, 'html.parser')

    firstImg = soupEngine.find(itemprop="image")
    images = []

    # first image is a url like http://rightmove/image__000 indexed with 0s so we need to keep updating the index until their are no images left and we reach an error\
    while imagesLeft:
        nextImgUrl = incrementUrl(firstImg)
        imgValid = isValidImg(nextImgUrl)

        if not imgValid:
            imagesLeft = False
            break

        images.append(nextImgUrl)

    return (address, image)

        
driver = webdriver.Chrome()
driver.get("https://www.rightmove.co.uk/house-prices/details/ed1ef3cd-37dd-45c1-8a70-8fdb18391462?id=media0")

htmlDoc = driver.page_source
parseBasicPage(htmlDoc)

driver.quit()
