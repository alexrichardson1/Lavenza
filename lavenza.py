from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


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
    persona_link = driver.find_element_by_xpath(
        "/html/body/div/ng-view/table/tbody/tr/td[2]/a")
    persona_link.click()
    # ensure the page is loaded
    sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    skill_table = soup.find("table", {"id": "skillTable"})
    skills = skill_table.find_all("a")
    for skill in skills:
        print(skill.text)
    driver.quit()


if __name__ == '__main__':
    main()
