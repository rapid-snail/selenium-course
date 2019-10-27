from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ensure_array_sorted(arr):
    sorted_arr = sorted(arr)
    for idx in range(len(arr)):
        found = arr[idx]
        expected = sorted_arr[idx]
        if found != expected:
            raise Exception("Неверная сортировка. Нашли='{}' Ожидали='{}'".format(found, expected))


def click_countries_onpage_countries(driver, country_name, link):
    driver.get(link)
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))
    table = driver.find_element_by_id("table-zones")
    rows = table.find_elements_by_css_selector("tr:not([class=header])")
    zones = []
    for row in rows:
        tds = row.find_elements_by_tag_name("td")
        if tds[0].text.strip() != "":
            zones.append(tds[2].text)

    if not zones:
        raise Exception("{} - нет зон".format(country_name))

    ensure_array_sorted(zones)
    print("{} - зоны отсортированы верно".format(country_name))

def click_countries_onpage_zones(driver, country_name, link):
    driver.get(link)
    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))
    table = driver.find_element_by_id("table-zones")
    rows = table.find_elements_by_css_selector("tr:not([class=header])")
    zones = []
    for row in rows:
        tds = row.find_elements_by_tag_name("td")
        if len(tds) == 4:
            select = tds[2].find_element_by_tag_name("select")
            zone_selected = select.find_element_by_css_selector("option[selected=selected]").text
            zones.append(zone_selected)

    ensure_array_sorted(zones)
    print("{} - зоны отсортированы верно".format(country_name))


def t1(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")

    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))

    fld = driver.find_element_by_name("username")
    fld.send_keys("admin")

    fld = driver.find_element_by_name("password")
    fld.send_keys("111")

    btn = driver.find_element_by_name("login")
    btn.click()

    wait.until(EC.title_contains("My Store"))

    table = driver.find_element_by_class_name("dataTable")
    rows = table.find_elements_by_class_name("row")
    nonempty_zones = []
    countries = []
    countries_links_by_name = {}
    for row in rows:
        tds = row.find_elements_by_tag_name("td")
        a = tds[4].find_element_by_tag_name("a")
        countries.append(a.text)
        countries_links_by_name[a.text] = a.get_attribute("href")

        if tds[5].text != "0":
            nonempty_zones.append(a.text)

    ensure_array_sorted(countries)
    print("Страны отсортированы верно")

    for country_name in nonempty_zones:
        click_countries_onpage_countries(driver, country_name, countries_links_by_name[country_name])


def t2(driver):
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")

    wait = WebDriverWait(driver, 10) # seconds
    wait.until(EC.title_contains("My Store"))

    table = driver.find_element_by_class_name("dataTable")
    rows = table.find_elements_by_class_name("row")
    countries = []
    for row in rows:
        a = row.find_element_by_tag_name("a")
        countries.append((a.text, a.get_attribute("href")))


    for country_name, country_link in countries:
        click_countries_onpage_zones(driver, country_name, country_link)


def main():
    driver = webdriver.Chrome()
    try:
        t1(driver)
        t2(driver)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
