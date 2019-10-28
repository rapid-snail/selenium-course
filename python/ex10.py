from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def split_rgba(s):
    m = re.search(r"rgba?\((\d+), (\d+), (\d+)(, (\d+))?\)", s)
    if m:
        return [int(m.group(1)), int(m.group(2)), int(m.group(3))]
    return None


def ensure_view_ok(product):
    font_size_regular = float(product["regular_font_size"][:-2])
    font_size_campaign = float(product["campaign_font_size"][:-2])
    if font_size_campaign <= font_size_regular:
        raise Exception("Размер шрифта акционной цены не больше обычной")
    if not product["regular_text_decoration"].startswith("line-through"):
        raise Exception("Обычная цена не перечеркнута")
    x = split_rgba(product["regular_price_color"])
    if not (x[0] == x[1] and x[0] == x[2]):
        raise Exception("Обычная цена не серая")
    x = split_rgba(product["campaign_price_color"])
    if not (x[0] > 0 and x[1] == 0 and x[2] == 0):
        raise Exception("Акционная цена не красная")


def get_product_info(driver):
    product = {}
    driver.get("http://localhost/litecart/en/")
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))

    product["name"] = driver.find_element_by_css_selector("#box-campaigns .name").text
    rp_elm =  driver.find_element_by_css_selector("#box-campaigns .regular-price")
    product["regular_price"] = rp_elm.text
    product["regular_price_color"] = rp_elm.value_of_css_property("color")
    product["regular_font_size"] = rp_elm.value_of_css_property("font-size")
    product["regular_text_decoration"] = rp_elm.value_of_css_property("text-decoration")
    cp_elm = driver.find_element_by_css_selector("#box-campaigns strong.campaign-price")
    product["campaign_price"] = cp_elm.text
    product["campaign_price_color"] = cp_elm.value_of_css_property("color")
    product["campaign_font_size"] = cp_elm.value_of_css_property("font-size")
    product["link"] = driver.find_element_by_css_selector("#box-campaigns .link").get_attribute("href")

    # print(product)
    ensure_view_ok(product)
    return product

def get_cart_product_info(driver, link):
    product = {}
    driver.get(link)
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))

    product["name"] = driver.find_element_by_css_selector("#box-product .title").text
    rp_elm = driver.find_element_by_css_selector("#box-product .regular-price")
    product["regular_price"] = rp_elm.text
    product["regular_price_color"] = rp_elm.value_of_css_property("color")
    product["regular_font_size"] = rp_elm.value_of_css_property("font-size")
    product["regular_text_decoration"] = rp_elm.value_of_css_property("text-decoration")
    cp_elm = driver.find_element_by_css_selector("#box-product strong.campaign-price")
    product["campaign_price"] = cp_elm.text
    product["campaign_price_color"] = cp_elm.value_of_css_property("color")
    product["campaign_font_size"] = cp_elm.value_of_css_property("font-size")

    # print(product)
    ensure_view_ok(product)
    return product


def main():
    allowed_drivers = [webdriver.Chrome, webdriver.Firefox, webdriver.Ie]
    for drv in allowed_drivers:
        driver = drv()
        try:
            product_main = get_product_info(driver)

            product_cart = get_cart_product_info(driver, product_main["link"])

            compare_items = []
            compare_items.append(("name", "Название товара на главной странице не соответствует названию в карточке товара"))
            compare_items.append(("regular_price", "Цена товара на главной странице не соответствует цене в карточке товара"))
            compare_items.append(("campaign_price", "Акционная цена товара на главной странице не соответствует акционной цене в карточке товара"))

            for key, text in compare_items:
                if product_main[key] != product_cart[key]:
                    raise Exception(text)

            print("Браузер '{}' - успешно".format(driver.name))
        finally:
            driver.close()


if __name__ == "__main__":
    main()

