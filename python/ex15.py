from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    driver = webdriver.Remote("http://192.168.1.219:4444/wd/hub", desired_capabilities={"browserName": "internet explorer"})
    try:
        driver.get("http://hostlitecard/litecart/")

        wait = WebDriverWait(driver, 10) # seconds
        wait.until(EC.title_contains("Online Store"))

        picts = driver.find_elements_by_class_name("product")

        for pict in picts:
            stickers = pict.find_elements_by_class_name("sticker")

            if len(stickers) != 1:
                raise Exception("Стикер не один")
            else:
                print ("Стикер один")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
