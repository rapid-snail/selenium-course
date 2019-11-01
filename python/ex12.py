from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import datetime
import os
import random


def find_tab_by_name(drv, tab_name):
    tablinks = drv.find_elements_by_css_selector("#content .index a")
    for elm in tablinks:
        if elm.text == tab_name:
            return elm

    raise Exception("Tab '{}' not found".format(tab_name))


def find_menu_by_name(drv, menu_name):
    menu = drv.find_element_by_css_selector("ul#box-apps-menu")
    pmenu = menu.find_elements_by_css_selector("li#app-")
    for elm in pmenu:
        a = elm.find_element_by_tag_name("a")
        if a.text == menu_name:
            return elm

    raise Exception("Menu '{}' not found".format(menu_name))


def click_menu(drv, menu_name):
    menu = find_menu_by_name(drv, menu_name)
    a = menu.find_element_by_tag_name("a")
    a.click()
    wait = WebDriverWait(drv, 10) # seconds
    wait.until(EC.title_contains("My Store"))


def fill_general(driver):
    elm = driver.find_element_by_name("status")
    elm.click()
    elm = driver.find_element_by_name("name[en]")
    product_name = "Blue Duck Heart " + "".join(random.sample("0123456789",5))
    elm.send_keys(product_name)
    elm = driver.find_element_by_name("code")
    elm.send_keys("rdh0001")
    elm = driver.find_element_by_css_selector("[data-name=Root]")
    elm.click()
    elm = driver.find_element_by_css_selector("[data-name='Rubber Ducks']")
    elm.click()
    elm = driver.find_element_by_name("quantity")
    elm.clear()
    elm.send_keys("25")

    elm = driver.find_element_by_name("new_images[]")
    current_path = "../images/blueducknew.png"
    abs_path = os.path.abspath(current_path)
    elm.send_keys(abs_path)

    elm = driver.find_element_by_name("date_valid_from")
    date = datetime.date.today()
    elm.send_keys(Keys.HOME + date.strftime("%d.%m.%Y"))
    valid_to = date + datetime.timedelta(days=30)
    elm = driver.find_element_by_name("date_valid_to")
    elm.send_keys(Keys.HOME + valid_to.strftime("%d.%m.%Y"))
    return product_name


def fill_information(driver):
    find_tab_by_name(driver, "Information").click()
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))
    elm = driver.find_element_by_name("manufacturer_id")
    select = Select(elm)
    select.select_by_visible_text("ACME Corp.")
    driver.find_element_by_name("head_title[en]").send_keys("Rubber Duck with Heart")


def fill_prices(driver):
    find_tab_by_name(driver, "Prices").click()
    elm = driver.find_element_by_name("purchase_price")
    elm.clear()
    elm.send_keys("5")
    elm = driver.find_element_by_name("purchase_price_currency_code")
    select = Select(elm)
    select.select_by_visible_text("US Dollars")
    elm = driver.find_element_by_name("prices[USD]")
    elm.send_keys("20")


def ensure_product_saved(driver, product_name):
    elms = driver.find_elements_by_css_selector(".dataTable .row a:not([title=Edit])")
    for elm in elms:
        if elm.text == product_name:
            return

    raise Exception("Продукт не сохранен")


def main():
    driver = webdriver.Chrome()
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

    try:
        # нажали меню Catalog
        click_menu(driver, "Catalog")
        # нажали кнопку Add new product
        btns = driver.find_elements_by_css_selector("#content a.button")
        btns[1].click()
        # заполнили вкладку General
        product_name = fill_general(driver)
        # заполнили вкладку Information
        fill_information(driver)
        # заполнили вкладку Prices
        fill_prices(driver)
        # сохраняем товар
        driver.find_element_by_name("save").click()
        wait.until(EC.title_contains("My Store"))

        ensure_product_saved(driver, product_name)
        print("Продукт успешно сохранен")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
