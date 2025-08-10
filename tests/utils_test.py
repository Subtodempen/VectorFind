import pytest
from src.utils.downloader import getHtml

def testHtmlGetter():
    testUrl = "https://httpbin.org/html"
    expectedResult = "Herman Melville - Moby-Dick"

    actualResults = getHtml(testUrl)

    assert expectedResult in actualResults


# write test for image getter
# ALSO USE WITH for image getter 

