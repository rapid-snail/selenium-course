import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def test_litecart(driver):
    driver.get("http://localhost/litecart/admin/")
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_is("My Store"))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("111")
    driver.find_element_by_name("login").click()
    wait.until(EC.title_is("My Store"))

