from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from tabulate import tabulate


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
    table = get_table_data(
        soup, "table", {
            "class": "ui table unstackable striped recipesTable"}, False)
    driver.quit()

    print("Persona name:", " ".join(name.split()[:-3]))
    print(
        tabulate(
            elementals_table,
            headers="firstrow",
            tablefmt="fancy_grid"))
    print(tabulate(skills, headers=["Skills"], tablefmt="fancy_grid"))
    for i in range(len(table)):
        table[i] = clean_row(table[i])
    headers = ["Cost"]
    for i in range(1, len(table)):
        headers.append("Persona #" + str(i))
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == '__main__':
    main()
