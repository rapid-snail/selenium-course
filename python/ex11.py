from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import random


def logout(driver, wait):
    elm = driver.find_element_by_id("box-account")
    links = elm.find_elements_by_tag_name("a")
    links[3].click()
    wait.until(EC.title_contains("My Store"))


def main():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/en/")
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))

    try:
        form = driver.find_element_by_name("login_form")
        a = form.find_element_by_tag_name("a")
        a.click()
        wait.until(EC.title_contains("My Store"))

        driver.find_element_by_name("firstname").send_keys("ivan")
        driver.find_element_by_name("lastname").send_keys("ivanov")
        driver.find_element_by_name("address1").send_keys("Trump ave 1")
        driver.find_element_by_name("postcode").send_keys("".join(random.sample("0123456789", 5)))
        driver.find_element_by_name("city").send_keys("Atlanta")

        country = driver.find_element_by_name("country_code")
        elm = Select(country)
        elm.select_by_visible_text("United States")

        zone = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name=zone_code]")))

        elm = Select(zone)
        zones_total = len(elm.options)
        elm.select_by_index(random.randint(0, zones_total - 1))

        elm = driver.find_element_by_name("email")
        email = "".join(random.sample("abcdefghijklABCDEFGHIGKL12345", 10)) + "@example.com"
        elm.send_keys(email)
        driver.find_element_by_name("phone").send_keys("+1"+"".join(random.sample("0123456789", 7)))
        driver.find_element_by_name("password").send_keys("1")
        driver.find_element_by_name("confirmed_password").send_keys("1")

        driver.find_element_by_name("create_account").click()
        wait.until(EC.title_contains("My Store"))

        logout(driver, wait)

        driver.find_element_by_name("email").send_keys(email)
        driver.find_element_by_name("password").send_keys("1")
        driver.find_element_by_name("login").click()
        wait.until(EC.title_contains("My Store"))

        logout(driver, wait)
        print("Успешно")

    finally:
        driver.close()


if __name__ == "__main__":
    main()

