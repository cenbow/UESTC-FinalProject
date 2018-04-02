import os, sys, q
from datetime import datetime
from utils.cached import cached, cache_res
import networkx as nx
import pandas as pd
import numpy as np
from collections import defaultdict
import array, bisect, math
import itertools as its

sys.path.insert(0, '..')

def dictify(dataframe):
    """
    convert data format from pd.DataFrame to dict
    :param dataframe:
    :return:
    {
        company1: {
            round1: [invest1, invest2, ...],
            round2: [invest4, invest7,...]
        }
        company2:
        {
            ...
        }
    }
    """
    data = defaultdict(dict)
    data7 = defaultdict(dict)
    companies = set()
    invests = set()

    for idx, row in dataframe.iterrows():
        #Date filter
        try:
            dt = datetime.strptime(row['日期(time)'], "%Y.%m.%d")
        except ValueError as ve:
            print(ve, row['日期(time)'])

        company = row['公司(company)']
        companies.add(company)
        round_ = row['融资轮数(round)']
        invests_ = eval(row['投资机构(invests)'])
        assert (isinstance(invests_, list))

        if '投资方未透露' in invests_:
            invests_ = []

        if dt.year < 2017:
            if round_ not in data[company]:
                data[company][round_] = invests_
                invests = invests.union(invests_)
        else:
            if round_ not in data[company]:
                data7[company][round_] = invests_
                invests = invests.union(invests_)

    return data, data7, companies, invests


def build_graph(data):
    g = nx.Graph()
    for company in data.keys():
        # g.add_node(company)
        rounds = data[company]
        for round_ in rounds.keys():
            # g.add_nodes_from(rounds[round_])
            g.add_edges_from([(company, invest) for invest in rounds[round_]])

    return g
    # q(g.nodes())g


def build_graph_round(data):
    g = nx.Graph()
    # 二部图： L = {(company, round)}, R={investors}
    for company in data.keys():
        # g.add_node(company)
        rounds = data[company]
        for round_ in rounds.keys():
            # g.add_nodes_from(rounds[round_])
            g.add_edges_from([((company, round_), invest)
                              for invest in rounds[round_]])

    return g


def tao_one_mode_projection(bigraph, projection):
    """
    :param g: networkx.Bipartite
    :param B: subset of nodes to project on
    :return: networkx.Graph
    """
    projected_graph = nx.DiGraph()
    projected_graph.add_nodes_from(projection)
    projection &= bigraph.nodes()
    for u in projection:
        for v in projection:
            w = 0.0
            # common_neighbors = set(bigraph.adj[u]).intersection(set(bigraph.adj[v]))
            for l in nx.common_neighbors(bigraph, u, v):
                # assume g is unweighted bigraph;
                w += 1 / bigraph.degree(l)
            if w != 0.0:
                projected_graph.add_edge(u, v, weight=w)
    return projected_graph


def sim(G, u, v):
    common_neighbors = set(G.adj[u]).intersection(G.adj[v])
    assert(all(u in G.adj[w] for w in common_neighbors))
    assert(all(v in G.adj[w] for w in common_neighbors))
    return sum(1 / math.log(G.degree[w], 2) for w in common_neighbors)

def 

=========================================================
df = pd.read_excel('InvestEvent_1.xlsx')
dataX, dataY,  _, investors = dictify(df)

# filename开头用company的含义？
X_bipartite = cache_res("company.bipartite.X", build_graph, dataX)
X_graph = cache_res('company.projected.X', tao_one_mode_projection, X_bipartite, investors)

Y_bipartite = cache_res('company.bipartite.test', build_graph, dataY)
Y_graph = cache_res('company.projected.test', tao_one_mode_projection, Y_bipartite, investors)

X_set = array.array('d')
Y_set = array.array('d')

# 后面可以再算一下(u,v)存在连边和不存在的区别
for u in X_graph.nodes():
    for v in X_graph.nodes():
        if u == v : continue
        X_set.append(sim(X_graph, u, v))

for u in Y_graph.nodes():
    for v in Y_graph.nodes():
        if u == v : continue
        Y_set.append(sim(Y_graph, u, v))
