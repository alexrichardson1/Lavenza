from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_persona_page(persona):
    """Obtains the html of the page for `peronsa`."""
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
        messagebox.showerror("Search Error", "Perona not found.")
        return None
        # exit("Persona " + persona + " not found.")
    persona_link.click()
    # ensure the page is loaded
    sleep(2)
    html = driver.page_source
    driver.quit()
    return html


def scrape_persona_info(soup):
    """Scrapes the pesona information using `soup`."""
    # persona name
    persona_title = soup.find("h2", {"class": "ng-binding"}).text
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
    return persona_title, elementals_table, skills, ingredients_table


def get_table_header_data(soup, tag, key):
    """Scrapes data from a table header."""
    table = soup.find(tag, key)
    table_header = table.find("thead")
    row = table_header.find_all("th")
    return [x.text for x in row]


def get_table_data(soup, tag, key, want_header):
    """Scrapes data from a table. If `want_header` is true, it will return data
     from the header as well."""
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
    """Clean the data regarding a perona in `row`."""
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


def format_table(data, headers):
    """Formats a table for pretty printing."""
    return tabulate(data, headers=headers, tablefmt="fancy_grid")


def save_data(persona_title, elementals_table, skills, ingredients_table):
    """Write persona information to a `persona_name`.txt file"""
    name = " ".join(persona_title.split()[:-3])
    name_display = "================================================ " + \
        name + \
        " ================================================"
    elementals_table = format_table(elementals_table, "firstrow")
    skills = format_table(skills, ["Skills"])
    # clean the data for each persona ingredient
    for i in range(len(ingredients_table)):
        ingredients_table[i] = clean_row(ingredients_table[i])
    headers = ["Cost"]
    for i in range(1, len(ingredients_table[0])):
        headers.append("Persona #" + str(i))
    ingredients_table = format_table(ingredients_table, headers)

    file = open(f"{name}.txt", "w")
    file.write(name_display)
    file.write("\n\n")
    file.write(elementals_table)
    file.write("\n\n")
    file.write(skills)
    file.write("\n\n")
    file.write(ingredients_table)
    file.close()


def scrape_persona(persona):
    """Scrape persona fusion information."""
    html = get_persona_page(persona)
    if html is None:
        return
    soup = BeautifulSoup(html, "html.parser")
    persona_title, elementals_table, skills, ingredients_table = scrape_persona_info(
        soup)
    save_data(persona_title, elementals_table, skills, ingredients_table)


def main():
    root = Tk()
    root.minsize(300, 200)
    root.title("Lavenza")
    label = Label(root, text="Persona Name")
    label.pack()
    entry = Entry(root,
                  width=30)
    entry.pack()
    button = Button(
        root,
        text="Search",
        command=lambda: scrape_persona(
            entry.get()))
    button.pack()

    # tkinter event loop
    root.mainloop()


if __name__ == '__main__':
    main()
