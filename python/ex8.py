from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost/litecart/")

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
        driver.close()


if __name__ == "__main__":
    main()
