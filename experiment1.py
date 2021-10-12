import networkx as nx
import pandas as pd
import constants as cons
import random
import statistics

random.seed(0)

## Load network from csv to networkx graph
channels = pd.read_csv(cons.CHANNELS_CSV)  # This csv comes from a snapshot from https://ln.fiatjaf.com/ from October 11, 2021

graph = nx.from_pandas_edgelist(channels, cons.NODE_A, cons.NODE_B, [cons.SATOSHIS, cons.BASE_FEE, cons.RELATIVE_FEE])

## Experiment parameters

watchtower_percentages = range(5,31,5)  # investigate for values 5,10,15,20,25,30
avg_runs = 100

## Simulation

num_nodes = len(graph.nodes)
nodes = list(graph.nodes)

pmap = []
for p in watchtower_percentages:
    data = []
    for r in range(0,avg_runs):
        watchtower_nodes = random.sample(nodes,int(num_nodes * p/100))
        total = 0
        for node in watchtower_nodes:
            for u,v in graph.edges(node):
                total += graph.get_edge_data(u,v)[cons.SATOSHIS]/2/cons.SATOSHIS_IN_BTC 
        data.append(total)
    mean = statistics.mean(data)
    stdev = statistics.stdev(data)
    pmap.append((p,mean,stdev))

## Results

for p,m,s in pmap:
    print(f'{p} {m} {s}')