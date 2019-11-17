from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def main():
    desired = DesiredCapabilities.CHROME
    desired['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=desired)

    try:
        driver.get("http://localhost/litecart/admin/")
        wait = WebDriverWait(driver, 10) # seconds
        wait.until(EC.title_contains("My Store"))

        fld = driver.find_element_by_name("username")
        fld.send_keys("admin")

        fld = driver.find_element_by_name("password")
        fld.send_keys("111")

        btn = driver.find_element_by_name("login")
        btn.click()

        wait.until(EC.title_contains("My Store"))

        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        rows = driver.find_elements_by_css_selector(".dataTable .row")
        products = []

        for row in rows:
            elms = row.find_elements_by_css_selector("i.fa")
            if len(elms) == 2:
                products.append(row.find_element_by_css_selector("a:not([title])").get_attribute("href"))

        driver.get_log("browser")
        for product in products:
            driver.get(product)
            logs = driver.get_log("browser")
            if len(logs) > 0:
                print("Сообщения в логе браузера на странице " + product + " :")
                for l in logs:
                    print(l)

            wait.until(EC.title_contains("Edit Product"))

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
