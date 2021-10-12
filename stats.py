import networkx as nx
import pandas as pd
import constants as cons
import random

random.seed(0)

channels = pd.read_csv(cons.CHANNELS_CSV)

graph = nx.from_pandas_edgelist(channels, cons.NODE_A, cons.NODE_B, [cons.SATOSHIS, cons.BASE_FEE, cons.RELATIVE_FEE])

print(f'Number of nodes {len(graph.nodes)}')
print(f'Number of edges {len(graph.edges)}')
print(f'Number of edges {len(graph.edges)}')

total = 0
for u,v,a in graph.edges(data=True):
    total += a[cons.SATOSHIS]

print(f'Total capacity {total/cons.SATOSHIS_IN_BTC}')