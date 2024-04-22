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
        list_webpages = {"Character_List": "https://genshin-impact.fandom.com/wiki/Character/List",
                         "Nation_List": "https://genshin-impact.fandom.com/wiki/Category:Nations",
                         "NPC_List": "https://genshin-impact.fandom.com/wiki/NPC/List"}
        webpages = {}
        characters = get_char_list(list_webpages["Character_List"])
        nations = get_nation_list(list_webpages["Nation_List"])
        npcs = get_npc_list(list_webpages["NPC_List"])
        for page in characters[0] + nations + npcs:
            page = page.replace(" ", "_")
            page = page.replace('"', "'")
            webpages[page] = "https://genshin-impact.fandom.com/wiki/%s" % page
        print("Scraping")
        for filename in list_webpages:
            data = list_webpages[filename]
            with open("webpages/lists/%s.html" % filename, "w+", encoding="utf-8") as f:
                f.write(str(soup(data)))
        for filename in webpages:
            data = webpages[filename]
            if filename in nations:
                with open("webpages/nations/%s.html" % filename, "w+", encoding="utf-8") as f:
                    f.write(str(soup(data)))
            elif filename in characters[0]:
                with open("webpages/characters/%s.html" % filename, "w+", encoding="utf-8") as f:
                    f.write(str(soup(data)))
            elif filename in npcs:
                with open("webpages/npcs/%s.html" % filename, "w+", encoding="utf-8") as f:
                    f.write(str(soup(data)))


def get_nation_list(webpage):
    webpage = soup(webpage)
    nations = [nation.text.strip() for nation in webpage.select(
        ".category-page__member-link")]
    return (nations)


def get_npc_list(webpage):
    webpage = soup(webpage)
    npc_list = list({npc.text.strip()
                     for npc in webpage.select(".columntemplate a")})
    print("===")
    print("Number of NPC's: ", len(npc_list))
    npc_list.sort()
    print("===")
    return (npc_list)


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
        webpage = soup("webpages/nations/%s.html" % nation)
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

# scraper(should_scrape)

nations = get_nation_list("webpages/lists/Nation_List.html")

print("List of nations:", nations)
print("===")

character_nations = get_nation_characters(characters, nations)

print("Characters related to each nation:")
print(character_nations)

npcs = get_npc_list("webpages/lists/NPC_List.html")


list_of_nodes = [characters, nations]
