from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from tabulate import tabulate


def get_persona_page():
    persona = input("Enter name of persona: ")
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
    driver.quit()
    return html


def scrape_persona_info(soup):
    # persona name
    name = soup.find("h2", {"class": "ng-binding"}).text
    # elemental attributes
    elementals_table = get_table_data(
        soup, "table", {
            "class": "ui table unstackable striped mobile-hidden"}, True)
    # persona skills
    skill_table = soup.find("table", {"id": "skillTable"})
    skills = skill_table.find_all("a")
    skills = [[x.text] for x in skills]
    # persona fusion ingredients
    ingredients_table = get_table_data(
        soup, "table", {
            "class": "ui table unstackable striped recipesTable"}, False)
    return name, elementals_table, skills, ingredients_table


def get_table_header_data(soup, tag, key):
    table = soup.find(tag, key)
    table_header = table.find("thead")
    row = table_header.find_all("th")
    return [x.text for x in row]


def get_table_data(soup, tag, key, want_header):
    data = []
    if want_header:
        data.append(get_table_header_data(soup, tag, key))
    table = soup.find(tag, key)
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [e.text.strip() for e in cols]
        data.append(cols)
    return data


def clean_row(row):
    # remove number
    row = row[1:]
    # persona ingredients
    personas = row[1:]
    for i, persona in enumerate(personas, 1):
        persona_info = persona.split()
        # keep only the name
        if persona_info[-1] == '⚠':
            row[i] = " ".join(persona_info[:-4])
        else:
            row[i] = " ".join(persona_info[:-3])
    return row


def print_table(data, headers):
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


def print_data(name, elementals_table, skills, ingredients_table):
    print(
        "================================================ " +
        " ".join(
            name.split()[
                :-3]) +
        " ================================================")
    print_table(elementals_table, "firstrow")
    print_table(skills, ["Skills"])
    # clean the data for each ingredient persona
    for i in range(len(ingredients_table)):
        ingredients_table[i] = clean_row(ingredients_table[i])
    headers = ["Cost"]
    for i in range(1, len(ingredients_table[0])):
        headers.append("Persona #" + str(i))
    print_table(ingredients_table, headers)


def main():
    soup = BeautifulSoup(get_persona_page(), "html.parser")
    name, elementals_table, skills, ingredients_table = scrape_persona_info(
        soup)
    print_data(name, elementals_table, skills, ingredients_table)


if __name__ == '__main__':
    main()
