from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def find_opened_window_handle(driver, existing_handles):
    opened_handles = driver.window_handles
    for handle in opened_handles:
        if not (handle in existing_handles):
            return handle
    raise Exception("Новое окно не открылось")


def main():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
        wait = WebDriverWait(driver, 10) # seconds
        wait.until(EC.title_contains("My Store"))

        fld = driver.find_element_by_name("username")
        fld.send_keys("admin")

        fld = driver.find_element_by_name("password")
        fld.send_keys("111")

        btn = driver.find_element_by_name("login")
        btn.click()

        wait.until(EC.title_contains("Countries"))

        btn = driver.find_element_by_css_selector("#content a.button") # кнопка Добавить страну
        time.sleep(1) # без этого в Chrome кликается не всегда
        btn.click()
        wait.until(EC.title_contains("Add New Country"))
        links = driver.find_elements_by_css_selector("#content a[target=_blank]:not([title])")

        if not links:
            raise Exception("Ссылок в другие окна нет")

        original_window = driver.current_window_handle
        for lnk in links:
            existing_windows = driver.window_handles
            lnk.click()
            if wait.until(EC.new_window_is_opened(existing_windows)):
                new_window = find_opened_window_handle(driver, existing_windows)
                driver.switch_to.window(new_window)
                print("Открыто " + driver.title)
                driver.close()
                driver.switch_to.window(original_window)
            else:
                raise Exception("Новое окно не открылось")
        print("Успешно")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
