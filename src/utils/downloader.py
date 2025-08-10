import requests
from requests.adapters import HTTPAdapter, Retry

import tempfile

def getHtml(url):
        session = requests.Session()
        genericHeader = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }        

        # construct a request tiemout loop and try 5 more 
        MAX_RETRY = 5
        BACK_OFF = 1
        ERROR_CODES = [500, 502, 504]
        TIMEOUT = 10

        retries = Retry(
            total=MAX_RETRY, 
            backoff_factor=BACK_OFF,
            status_forcelist=ERROR_CODES
        )
            

        session.mount('http://', HTTPAdapter(max_retries=retries))

        try:
            response = session.get(url, timeout=TIMEOUT, headers=genericHeader)

        except requests.exceptions.TooManyRedirects:
            logging.warning("invalid URL, base crawler URL is invalid")
            return None

        except requests.exceptions.RequestException as e:
            logging.error("Catostrophic request error: %s", e)
            return None
        
        return response.text

def downloadTempImg(url):
    tmp = tempfile.NamedTemporaryFile(delete=False)

    imgData = requests.get(url).content
    imgFile = open(tmp.name, "wb")

    imgFile.write(imgData)

    return tmp


