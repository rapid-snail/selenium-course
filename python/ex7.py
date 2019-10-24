from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------------
def ensure_h1_present(driver):
    if not driver.find_elements_by_css_selector("td#content h1"):
        raise Exception("h1 not found")
    print("h1 found")

# -------------------------------------------------------------------------
def find_menu_by_name(drv, menu_name):
    menu = drv.find_element_by_css_selector("ul#box-apps-menu")
    pmenu = menu.find_elements_by_css_selector("li#app-")
    for elm in pmenu:
        a = elm.find_element_by_tag_name("a")
        if a.text == menu_name:
            return elm

    raise Exception("Menu '{}' not found".format(menu_name))

# -------------------------------------------------------------------------
def click_submenu(drv, menu_name, submenu_name):
    menu = find_menu_by_name(drv, menu_name)
    ul = menu.find_element_by_tag_name("ul") # тут под-меню
    lis = ul.find_elements_by_tag_name("li") # сами пункты под-меню
    for elm in lis:
        a = elm.find_element_by_tag_name("a")
        if a.text == submenu_name:
            print("click submenu {} - {}".format(menu_name, submenu_name))
            a.click()
            wait = WebDriverWait(drv, 10) # seconds
            wait.until(EC.title_contains("My Store"))

            # проверяем, что h1 есть
            ensure_h1_present(drv)

            return


# -------------------------------------------------------------------------
def click_menu(drv, menu_name):
    menu = find_menu_by_name(drv, menu_name)
    a = menu.find_element_by_tag_name("a")
    print("click menu {}".format(menu_name))
    a.click()
    wait = WebDriverWait(drv, 10) # seconds
    wait.until(EC.title_contains("My Store"))

    # проверяем, что h1 есть
    ensure_h1_present(drv)

    # опять находим меню
    menu = find_menu_by_name(drv, menu_name)
    uls = menu.find_elements_by_tag_name("ul")
    if not uls:
        # если нет подменю, то выходим
        return

    ul = uls[0]
    lis = ul.find_elements_by_tag_name("li") # сами пункты под-меню
    submenus = []
    for li in lis:
        a = li.find_element_by_tag_name("a")
        submenus.append(a.text)

    for sm in submenus:
        print("submenu = {}".format(sm))
        click_submenu(drv, menu_name, sm)


# -------------------------------------------------------------------------
def main():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost/litecart/admin/")

        wait = WebDriverWait(driver, 10) # seconds
        wait.until(EC.title_is("My Store"))

        fld = driver.find_element_by_name("username")
        fld.send_keys("admin")

        fld = driver.find_element_by_name("password")
        fld.send_keys("111")

        btn = driver.find_element_by_name("login")
        btn.click()

        wait.until(EC.title_is("My Store"))
        menu = driver.find_element_by_css_selector("ul#box-apps-menu")
        pmenu = menu.find_elements_by_css_selector("li#app-")

        items = []
        for elm in pmenu:
            items.append(elm.find_element_by_tag_name("a").text)

        for name in items:
            click_menu(driver, name)

    finally:
       driver.close()


if __name__ == "__main__":
    main()
