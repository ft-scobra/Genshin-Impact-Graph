import scraper
import networkx as nx
import json


def add_nodes(G, list_of_nodes):
    for list in list_of_nodes:
        G.add_nodes_from(list)


def add_edges(G, edges):
    for nation, nation_character_list in edges.items():
        for character in nation_character_list:
            G.add_edge(nation, character)


def graph():
    print("===")
    print("Generating graph")

    G = nx.DiGraph()

    add_nodes(G, scraper.list_of_nodes)
    add_edges(G, scraper.character_nations)
    return (G)


def color_nodes(G, nations, characters, npcs):
    node_colors = []
    for node in G.nodes():
        if node in nations:
            color = "red"
        elif node in characters:
            color = "lightblue"
        elif node in npcs:
            color = "gray"
        node_colors.append(color)
        G.nodes[node]["color"] = color
    return (G, node_colors)


def size_nodes(G):
    node_sizes = []
    degrees = dict(G.degree())

    min_size = 20
    max_size = 100
    scaling_factor = (max_size - min_size) / \
        (max(degrees.values()) - min(degrees.values()))
    node_sizes = [(min_size + (degrees[node] - min(degrees.values()))
                   * scaling_factor)for node in G.nodes()]
    for node, size in zip(G.nodes(), node_sizes):
        G.nodes[node]['size'] = size
    return (G, node_sizes)


def write_graph(G, name):
    nx.write_graphml(G, name+".graphml")
    data = nx.node_link_data(G)
    with open("graph.json", "w") as f:
        json.dump(data, f, indent=4)


G = graph()
G, node_colors = color_nodes(
    G, scraper.nations, scraper.characters, scraper.npcs)
G, node_sizes = size_nodes(G)
print(G)
print(node_colors)
print(node_sizes)

write_graph(G, "graph")
