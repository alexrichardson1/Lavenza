from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep


def get_table_data(soup, tag, key):
    data = []
    table = soup.find(tag, key)
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [e.text.strip() for e in cols]
        data.append(cols)
    return data


def main():
    persona = "Arsene"
    # using firefox-geckodriver
    driver = webdriver.Firefox()
    # Persona 5 Royal Fusion Calculator website
    driver.get(
        "https://chinhodado.github.io/persona5_calculator/indexRoyal.html#/list")
    searchbox = driver.find_element_by_xpath(
        "/html/body/div/ng-view/div/input")
    # search for persona
    searchbox.send_keys(persona)
    try:
        persona_link = driver.find_element_by_xpath(
            "/html/body/div/ng-view/table/tbody/tr/td[2]/a")
    except NoSuchElementException:
        driver.quit()
        exit("Persona " + persona + " not found.")
    persona_link.click()
    # ensure the page is loaded
    sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    name = soup.find("h2", {"class": "ng-binding"})
    skill_table = soup.find("table", {"id": "skillTable"})
    skills = skill_table.find_all("a")
    for skill in skills:
        print(skill.text)

    table = get_table_data(
        soup, "table", {
            "class": "ui table unstackable striped recipesTable"})
    driver.quit()


if __name__ == '__main__':
    main()
