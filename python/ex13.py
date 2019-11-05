from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10) # seconds
    try:
        for _ in range(3):
            driver.get("http://localhost/litecart/en/")
            wait.until(EC.title_contains("My Store"))
            link = driver.find_element_by_css_selector(".content .product a") # ссылка на первую утку
            link.click()
            wait.until(EC.title_contains("My Store"))
            driver.find_element_by_css_selector("#cart span[class=quantity]") # количество уток в корзине
            elm = driver.find_elements_by_name("options[Size]") # селект у желтой утки
            if len(elm) > 0:
                select = Select(elm[0])
                select.select_by_index(1) # установили размер утки - маленькая
            btn = driver.find_element_by_name("add_cart_product") # кнопка Добавить в корзину
            btn.click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cart span[class=quantity][style]"))) # количество уток в корзине изменилось
        print("Товары добавлены успешно")
        link = driver.find_element_by_css_selector("#cart a") # ссылка на корзину
        link.click()
        wait.until(EC.title_contains("My Store"))
        # в корзине
        buttons = driver.find_elements_by_name("remove_cart_item")
        for _ in range(len(buttons)):
            button = driver.find_element_by_name("remove_cart_item") # кнопка Удалить товар из корзины
            table = driver.find_element_by_css_selector(".dataTable") # таблица заказа
            wait.until(EC.visibility_of(button))
            button.click()
            wait.until(EC.staleness_of(table))
        print("Товары удалены успешно")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
