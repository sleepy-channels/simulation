# We take the LN snapshot, and take an average node. This node has an attacker who knows that the honest node is coming online periodically (for example, once a day). This attacker now has certain chance to prevent the honest user from coming online, e.g. DoS attack. If the attack is successful, the attacker can post an old state, where he can potentially steal the balance of the honest user. We measure this risk over a given time span given a chance that the attacker successfully performs a DoS attack.
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

ln = True  # Set to True to investigate LN. Set to False to investigate Sleepy Channels
if ln:
    slots = 30
else:
    slots = 1
chance_to_fail = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]
avg_runs = 100

## Simulation

num_nodes = len(graph.nodes)
rmap = []
#bmap = []
for c in chance_to_fail:
    nodes = list(graph.nodes)
    channels = []
    btc = []
    for r in range(0,avg_runs):
        broken_nodes = []
        channels_at_risk = 0
        # btc_at_risk = 0
        for node in [x for x in nodes if x not in broken_nodes]: 
            for i in range(0,slots):
                if random.random() < c:
                    broken_nodes.append(node)
                    for u,v in graph.edges(node):
                        channels_at_risk += 1
                        # btc_at_risk += int (graph.get_edge_data(u,v)[cons.SATOSHIS]/2/cons.SATOSHIS_IN_BTC)
                continue
        channels.append(channels_at_risk)
        #btc.append(btc_at_risk)
    mean = statistics.mean(channels)
    stdev = statistics.stdev(channels)
    #btc_mean = statistics.mean(btc)
    #btc_stdev = statistics.stdev(btc)
    #bmap.append((c, btc_mean, btc_stdev))  # do for mean, stdev
    rmap.append((c, mean, stdev))

## Results

for c,m,s in rmap:
    print(f'{c} {m} {s}')