from bs4 import BeautifulSoup 
from selenium import webdriver

import requests
import logging

# scraper should have a hiarachial structure by first being able to scrape the simplest page with the addres image combo
# And then functionailty to find and locate the pages deal with securty roatte ips etc..

# First create a single function that parses a page like: https://www.rightmove.co.uk/house-prices/details/ed1ef3cd-37dd-45c1-8a70-8fdb18391462?id=media0

# ALl scraping functionailty will extend from this function
def parseBasicPage(pageHTML) -> tuple[str, list]:
    soupEngine = BeautifulSoup(pageHTML, 'html.parser')

    imgRawHtml = soupEngine.find(itemprop="image")
    images = []

    if imgRawHtml is None:
        logging.warning("Invalid HTML Doc being parsed, %s", pageHTML)
        return

    nextImgUrl = imgRawHtml['content']

    imagesLeft = True
    address = soupEngine.find('h1')
    # first image is a url like http://rightmove/image__000 indexed with 0s so we need to keep updating the index until their are no images left and we reach an error
    nextImgUrl = _getFirstImgUrl(nextImgUrl)

    while imagesLeft:
        nextImgUrl = _incrementUrl(nextImgUrl)
        imgValid = _isValidImg(nextImgUrl)
         
        if not imgValid:
            imagesLeft = False
            break

        images.append(nextImgUrl)

    return (address, images)

def _incrementUrl(url):
    indexLocation = _findImageIndex(url)

    imgIndex = url[indexLocation] + url[indexLocation + 1] # reads a two digit integer from the url will increment and then write it back
    imgIndex = int(imgIndex) + 1 # increments the index to find the next image

    url = _writeImageIndex(url, imgIndex, indexLocation)

    return url

def _isValidImg(imageUrl):
    if not imageUrl:
        return False
    
    response = requests.head(imageUrl)
    validStatusCode = 200
    
    if response.status_code == validStatusCode: # MAGIC NUMBER but 200 very obviously represents a valid status code in this context
        return True
    
    return False

#finds the first image, sometimes rightmove wont display images in order so index first one then  we can increment properly
def _getFirstImgUrl(url):
    indexLocation = _findImageIndex(url)

    return _writeImageIndex(url, 0, indexLocation) 

def _findImageIndex(url):
    identifier = '_IMG_'
    identifierLocation = url.find(identifier)

    indexLocation = identifierLocation + len(identifier)

    if identifierLocation == -1:
        logging.error("Invalid URL being parsed...")
        return None
    
    return indexLocation


def _writeImageIndex(url, imgIndex, indexLocation):
    imgIndexString = str(imgIndex).zfill(2) # keep the 2 leading zeros in the origional url
    url = url[:indexLocation] + imgIndexString + url[indexLocation + len(imgIndexString):]

    return url

