from bs4 import BeautifulSoup
import requests
import json


def soup(url):
    if url[0:4] == "http":
        return (BeautifulSoup(requests.get(url).text, "lxml"))
    else:
        return (BeautifulSoup(open(url, "r", encoding="utf-8"), "lxml"))


def get_char_list(url):
    webpage = soup(url)
    playable = [character.text.strip() for character in webpage.select(
        "table:nth-of-type(1) td:nth-of-type(2)")]
    with open("characters.json", "r") as f:
        existing = json.load(f)
        if existing == playable:
            return (existing, False)
        else:
            json.dump(playable, open("characters.json", "w"))
            return (playable, True)


def scraper(scrape):
    if scrape == True:
        webpages = {
            "Character_List": "https://genshin-impact.fandom.com/wiki/Character/List",
            "Nation_List": "https://genshin-impact.fandom.com/wiki/Category:Nations"
        }
        characters = get_char_list(webpages["Character_List"])
        nations = [nation for nation in get_nation_list(
            webpages["Nation_List"])]
        print(nations)
        for page in characters[0] + nations:
            page = page.replace(" ", "_")
            webpages[page] = "https://genshin-impact.fandom.com/wiki/%s" % page
        print("Scraping")
        for filename in webpages:
            data = webpages[filename]
            with open("webpages/%s.html" % filename, "w+", encoding="utf-8") as f:
                f.write(str(soup(data)))


def get_nation_list(webpage):
    webpage = soup(webpage)
    nations = [nation.text.strip() for nation in webpage.select(
        ".category-page__member-link")]
    return (nations)


def get_related_characters(character_list, table_number, nation, webpage, character_nations):
    characters_of_nation = webpage.select(
        "table:nth-of-type(%s) td:nth-of-type(2)" % table_number)
    for character in range(len(characters_of_nation)):
        if characters_of_nation[character].text.strip() in character_list:
            character_nations[nation].append(
                characters_of_nation[character].text.strip())
    return (characters_of_nation)


def get_nation_characters(characters_list, nations_list):
    character_nations = {nation: [] for nation in nations_list}
    for nation in nations_list:
        webpage = soup("webpages/%s.html" % nation)
        get_related_characters(characters_list, 1, nation,
                               webpage, character_nations)
        get_related_characters(characters_list, 2, nation,
                               webpage, character_nations)
        if nation == "Snezhnaya":
            get_related_characters(
                characters_list, 3, nation, webpage, character_nations)
    return (character_nations)


characters, should_scrape = get_char_list(
    "https://genshin-impact.fandom.com/wiki/Character/List")

print("List of characters:", characters)
print("===")
print("Scrape: ", should_scrape)
print("===")

scraper(should_scrape)

nations = get_nation_list("webpages/Nation_List.html")

print("List of nations:", nations)
print("===")

character_nations = get_nation_characters(characters, nations)

print("Characters related to each nation:")
print(character_nations)
