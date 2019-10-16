import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://www.google.com/")
    wait = WebDriverWait(driver, 10) # seconds
