import scraper
import networkx as nx
import json

CHARACTERS = scraper.characters
NATIONS = scraper.nations
NPCS = scraper.npcs


def add_nodes(G, list_of_nodes):
    for sublist in list_of_nodes:
        G.add_nodes_from(sublist)


def add_edges(G, edges):
    for nation, subject_list in edges.items():
        for subject in subject_list:
            G.add_edge(nation, subject)


def graph():
    print("===")
    print("Generating graph")

    G = nx.DiGraph()

    add_nodes(G, scraper.list_of_nodes)
    add_edges(G, scraper.character_nations)
    return (G)


def color_nodes(G):
    node_colors = []
    for node in G.nodes():
        if node in NATIONS:
            group = "nation"
            color = "red"
        elif node in CHARACTERS:
            group = "character"
            color = "green"
        elif node in NPCS:
            group = "npc"
            color = "gray"
        node_colors.append(color)
        G.nodes[node]["group"] = group
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


def write_graph(G):
    nx.write_graphml(G, "./Graph/graph.graphml")
    data = nx.node_link_data(G)
    with open("./Graph/graph.json", "w") as f:
        json.dump(data, f, indent=4)


G = graph()
G, node_colors = color_nodes(G)
G, node_sizes = size_nodes(G)
print(G)
write_graph(G)
