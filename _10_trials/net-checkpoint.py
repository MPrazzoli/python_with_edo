import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import yfinance as yf
from datetime import date

graph = nx.karate_club_graph()

plt.figure(figsize=(30, 30))
nx.draw_networkx(graph, with_labels=True)

dfnodes = pd.DataFrame(graph.nodes())

dfedges = pd.DataFrame(graph.edges())

bet_centrality = nx.betweenness_centrality(graph, normalized=True,
                                           endpoints=False)

close_centrality = nx.closeness_centrality(graph)

deg_centrality = nx.degree_centrality(graph)
