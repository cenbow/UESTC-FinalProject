import os, sys, q
from datetime import datetime
from utils.cached import cached, cache_res
import networkx as nx
import pandas as pd
import numpy as np
from collections import defaultdict
import array, bisect, math
import itertools as its
# from numba import jit

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
            if u == v: continue
            w = 0.0
            # common_neighbors = set(bigraph.adj[u]).intersection(set(bigraph.adj[v]))
            has_cn = False
            for l in nx.common_neighbors(bigraph, u, v):
                # assume g is unweighted bigraph;
                has_cn = True
                w += 1 / bigraph.degree(l)
            w /= bigraph.degree(v);
            if has_cn:
                projected_graph.add_edge(u, v, weight=w)
    return projected_graph


# @jit
def sim(G, u, v):
    common_neighbors = set(G.adj[u]).intersection(G.adj[v])
    assert(all(u in G.adj[w] for w in common_neighbors))
    assert(all(v in G.adj[w] for w in common_neighbors))
    return sum(1 / math.log(G.degree(w), 2) for w in common_neighbors)


df = pd.read_excel('InvestEvent_1.xlsx')
traindata, testdata,  _, investors = dictify(df)

train_bipartite = cache_res("company.bipartite.train", build_graph, traindata)
# 有可能因为investors不一致而出错
train_graph = cache_res('company.projected.train', tao_one_mode_projection, train_bipartite, investors)

test_bipartite = cache_res('company.bipartite.test', build_graph, testdata)
test_graph = cache_res('company.projected.test', tao_one_mode_projection, test_bipartite, investors)


# store graph edges for cpp analysis
with open('test_graph.txt', 'w') as output:
    output.write('%d\t%d\n' % (nx.number_of_nodes(test_graph), nx.number_of_edges(test_graph)))
    for e in test_graph.edges():
        output.write("%s\t%s\t%s\n"%(e[0], e[1], nx.get_edge_attributes(test_graph, 'weight')[e]))

with open('train_graph.txt', 'w') as output:
    output.write('%d\t%d' % (nx.number_of_nodes(train_graph), nx.number_of_edges(train_graph)))

    for e in train_graph.edges():
        output.write("%s\t%s\t%s\n"%(e[0], e[1], nx.get_edge_attributes(train_graph, 'weight')[e]))

print("finished writing test_graph.txt and train_graph.txt")
exit()

positive = array.array('d')
negative = array.array('d')

q("all graphs have been constructed")

# calculating similarity for all pairs
# store similarity value for the pair which has edge into array `positive`
# ...


loopCnt = 0
temp_res = defaultdict(int)

# @jit
def calculate_sim_for_all_pairs(graph, res):
    for u in graph.nodes():
        if graph.degree(u) < 1: continue
        delta = math.log(graph.degree(u), 2)
        for pair in its.combinations(graph.adj[u], r=2):
            if pair[0] > pair[1]:
                pair = (pair[1], pair[0])
                # q('unordered')
            res[pair] += delta
            # loopCnt += 1


calculate_sim_for_all_pairs(train_graph, temp_res)
# q(loopCnt)

# for u in train_graph.nodes():
#     for v in train_graph.nodes():
#         if u == v: continue
#         if (u,v) in train_graph.edges():
#             positive.append(sim(train_graph, u,v))
#         else:
#             negative.append(sim(train_graph, u,v))

for edge, s in temp_res.items():
    if edge in train_graph.edges():
        positive.append(s)
    else:
        negative.append(s)

q('before sort')
q(len(positive))
positive = array.array('d', sorted(positive))
negative = array.array('d', sorted(negative))
scores = []
q('after sort')
q(len(positive))

# calculate all scores for all possible threshold value in `positve` array

for idx, thr in enumerate(positive):
    n_idx = bisect.bisect(negative, thr)
    tp_ratio = (len(positive) - idx) / len(positive)
    tn_ratio = n_idx / len(negative)
    # scores = [(threshold, score), (threshold1, score1), ...]
    scores.append((thr, tp_ratio * tn_ratio))

q(len(scores))

import operator
# get the threshold with max scores
opt_threshold, _ = max(scores, key=operator.itemgetter(1))
print(_)


TP, FP, TN, FN = 0, 0, 0, 0
for edge in test_graph.edges(): # positive
    if sim(test_graph, *edge) > opt_threshold:
        TP += 1
    else:
        FP += 1

for u in test_graph.nodes():
    for v in test_graph.nodes():
        if u == v: continue
        if sim(test_graph, u, v) < opt_threshold:
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

print(fmt % (TP, FP, TP+FP, TN, FN, TN+FN, TP+TN, FP+FN, TP+FP+TN+FN))
