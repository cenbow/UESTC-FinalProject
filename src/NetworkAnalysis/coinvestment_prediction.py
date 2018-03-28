import os
from datetime import datetime
from cached import cached, cache_res
import networkx as nx
import pandas as pd
import numpy as np
from collections import defaultdict
import array, bisect, math

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
                w += 1 / len(bigraph[l])
            else:
                continue # continue wrapper loop
            projected_graph.add_edge(u, v, weight=w)
    return projected_graph


def sim(G, u, v):
    return sum(1 / math.log(len(G.adj(w)), 2) for w in nx.common_neighbors(G,u,v))


df = pd.read_excel('InvestEvent_1.xlsx')
traindata, testdata,  _, investors = dictify(df)

train_bipartite = cache_res("company.bipartite.train", build_graph,traindata)
# 有可能因为investors不一致而出错
train_graph = cache_res('company.projected.train', tao_one_mode_projection, train_bipartite, investors)

test_bipartite = cache_res('company.bipartite.test', build_graph, testdata)
test_graph = cache_res('company.projected.test', tao_one_mode_projection, test_bipartite, investors)

positive = array.array('d')
negative = array.array('d')

# calculating similarity for all pairs
# store similarity value for the pair which has edge into array `positive`
# ...

for u in train_graph.nodes():
    for v in train_graph.nodes():
        if u == v: continue
        if (u,v) in train_graph.edges():
            positive.append(sim(u,v))
        else:
            negative.append(sim(u,v))

positive = array.array('d', sorted(positive))
negative = array.array('d', sorted(negative))
scores = array.array('d')

# calculate all scores for all possible threshold value in `positve` array

for idx, thr in enumerate(positive):
    n_idx = bisect.bisec(negative, thr)
    tp_ratio = (len(positive) - idx) / len(positive)
    tn_ratio = n_idx / len(negative)
    # scores = [(threshold, score), (threshold1, score1), ...]
    scores.append((thr, tp_ratio * tn_ratio))

import operator
# get the threshold with max scores
opt_threshold, _ = max(scores, key=operator.getter(1))


TP, FP, TN, FN = 0, 0, 0, 0
for edge in test_graph.edges(): # positive
    if sim(*edge) > opt_threshold:
        TP += 1
    else:
        FP += 1

for u in test_graph.nodes():
    for v in test_graph.nodes():
        if u == v: continue
        if sim(u, v) < opt_threshold:
            TN += 1
        else:
            FN += 1

fmt ="""
TP	FP	P
%s	%s	%s
TN	FN	N
%s	%s	%s
T	F	SUM
%s	%s	%s
"""

print(fmt%(TP, FP, TP+FP, TN, FN, TN+FN, TP+TN, FP+FN, TP+FP+TN+FN))