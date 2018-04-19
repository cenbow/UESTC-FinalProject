import math
import array
import networkx as nx
import random as rd
import matplotlib.pyplot as plt

'''
Testing the relationship between PageRank and Adamic-Adai Index.
1. Computing the PageRank of the whole graph
2. Sample some node paris (u,v), let x be the difference of their PageRank, and let y be their Adamic-Ada Index.
3. plot the curve 


Result: They seem have not correlation.
'''

rd.seed()

NODE_NUM = 1000
###generation graph
random_graph = nx.Graph()
for i in range(NODE_NUM):
    for j in range(i):
        if rd.random() > 0.8:
            random_graph.add_edge(i, j)

pagerank = nx.pagerank(random_graph)


def similarity(u, v):
    common_adjacents = set(random_graph.adj[u]).intersection(random_graph.adj[v])
    sum = 0.0
    for w in common_adjacents:
        sum += 1 / math.log( len(random_graph.adj[w]) )
    return sum

print("dPR\tSim")

temp = []

def test():
    u = rd.randrange(1, NODE_NUM)
    v = rd.randrange(0, u)
    x = abs(pagerank[u]-pagerank[v])
    y = similarity(u, v)
    print('{0:.6f}\t{1:.3f}'.format(x, y))
    temp.append((x, y))


for _ in range(1000):
    test()

temp = sorted(temp, key=lambda item: item[0])
x = array.array('f', (x * 1000 for x, y in temp))
y = array.array('f', (y / 10 for x, y in temp))

plt.plot(x, y)
plt.show()
