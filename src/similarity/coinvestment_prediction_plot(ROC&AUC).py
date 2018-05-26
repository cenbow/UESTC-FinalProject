# -- coding:utf-8 --
# !~/anaconda3/bin/python3

"""
Differentiate node (VC) involed time:
    VC before 2017
    VC in 2017 (old)
    VC in 2017 (new)
    
Manipulate different similarity index
    Using PySim
        CN
        AA
        KATZ
        LOCAL RAMDOM WALK


@author: lisa
"""
import sys
#sys.path.insert(0,"/home/lisa/anaconda3/lib/python3.6/site-packages/PyNetSim")
sys.path.insert(0,"/home/liaojingyi/anaconda3/lib/python3.6/site-packages/PyNetSim")
import pandas as pd
from collections import defaultdict
from datetime import datetime
import networkx as nx
import numpy as np
import math
import itertools as its
from sklearn import metrics
from sklearn.metrics import roc_auc_score
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from utils.cached import cached, cache_res
import PyNetSim

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
    invests7 = set()

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
            if round_ not in data7[company]:
                data7[company][round_] = invests_
                invests7 = invests7.union(invests_)

    return data, data7, companies, invests, invests7


def build_graph(data):
    g = nx.Graph()
    for company in data.keys():
        # g.add_node(company)
        rounds = data[company]
        for round_ in rounds.keys():
            # g.add_nodes_from(rounds[round_])
            g.add_edges_from([(company, invest) for invest in rounds[round_]])

    return g


def tao_one_mode_projection(bigraph, projection):
    """
    :param g: networkx.Bipartite
    :param B: subset of nodes to project on
    :return: networkx.Graph
    """
    projected_graph = nx.Graph()
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


def discreteGraph(G):
    # str -> int
    discrete_map = dict() 
    cnt = 0
    for node in G.nodes():
        if node not in discrete_map:
            discrete_map [node] = cnt
            cnt += 1
    
    nodes_num = nx.number_of_nodes(G)
    mat = np.zeros(shape=(nodes_num, nodes_num))
    for e in G.edges():
        a = e[0]
        b = e[1]
        a = discrete_map[a]
        b = discrete_map[b]
        mat[a][b] = mat[b][a] = 1
        

    A = np.mat(mat)
    return discrete_map, A

def discreteGraph_weight(G):
    # str -> int
    discrete_map = dict() 
    cnt = 0
    for node in G.nodes():
        if node not in discrete_map:
            discrete_map [node] = cnt
            cnt += 1
    
    nodes_num = nx.number_of_nodes(G)
    mat = np.zeros(shape=(nodes_num, nodes_num))
    for e in G.edges():
        a = e[0]
        b = e[1]
        a = discrete_map[a]
        b = discrete_map[b]
        mat[a][b] = mat[b][a] = train_graph.get_edge_data(e[0],e[1])['weight']

    A = np.mat(mat)
    return discrete_map, A

def sim_AAweight(G,u,v):
    alpha = 1
    common_neighbors = set(G.adj[u]).intersection(G.adj[v])
    assert(all(u in G.adj[w] for w in common_neighbors))
    assert(all(v in G.adj[w] for w in common_neighbors))
    return sum((math.pow(float(G.get_edge_data(u,w,default=0.0)['weight']),alpha) + math.pow(float(G.get_edge_data(w,v,default=0.0)['weight']),alpha)) 
            / math.log(1+sum(math.pow(float(G.get_edge_data(w,k,default=0.0)['weight']),alpha)for k in G.adj[w]),2)
                for w in common_neighbors)   
    

def calculate_sim_for_specified_pairs(sim_martix, discrete_map, test_graph, node):
    score = []
    true = []
    
    for pair in its.combinations(node, r=2):
        a = discrete_map[pair[0]]
        b = discrete_map[pair[1]]
        score.append(sim_martix[a,b])
        
        if (pair[0],pair[1]) in test_graph.edges(): true.append(1)
        else: true.append(0)
    
    score = np.array(score)
    true = np.array(true)
    return score, true

def calculate_sim_for_specified_pairs_single(train_graph, test_graph, node):
    score = []
    true = []
    
    for pair in its.combinations(node, r=2):
        score.append(sim_AAweight(train_graph, pair[0], pair[1]))
        if (pair[0],pair[1]) in test_graph.edges(): true.append(1)
        else: true.append(0)
    
    score = np.array(score)
    true = np.array(true)
    return score, true
    
    
def roc(score, true_value):
    fpr, tpr, thresholds = metrics.roc_curve(true_value, score)
    
    AUC = str(roc_auc_score(true_value, score))
    print ("AUC:" + AUC)
    return fpr,tpr
    
#===================================================
df = pd.read_excel('InvestEvent_1.xlsx')
traindata, testdata,  _, investors, investors7 = dictify(df)
'''
# sample
train_bipartite = build_graph(traindata)
train_graph = tao_one_mode_projection(train_bipartite, investors)

test_bipartite = build_graph(testdata)
test_graph = tao_one_mode_projection(test_bipartite, investors7)
'''


# sever
train_bipartite = cache_res("company.bipartite.train", build_graph, traindata)
train_graph = cache_res('company.projected.train', tao_one_mode_projection, train_bipartite, investors)

test_bipartite = cache_res('company.bipartite.test', build_graph, testdata)
test_graph = cache_res('company.projected.test', tao_one_mode_projection, test_bipartite, investors7)

# discrete

discrete_mapA, A = discreteGraph(train_graph)
PySim = PyNetSim.PyNetSim()
NetMartixA = PySim.ReadDataFromAdjacencyMatrix(A)
AA = PySim.AdamicAdarIndex()



'''
discrete_mapB, B = discreteGraph_weight(train_graph)
PySim = PyNetSim.PyNetSim()
NetMartixB = PySim.ReadDataFromAdjacencyMatrix(B)
Kw = PySim.Katz(lamda = 0.01)

CN = PySim.CommonNeighbor()
AA = PySim.AdamicAdarIndex()
K = PySim.Katz(lamda = 0.01)
'''

'''
# Take off isolated node
tempG = train_graph.copy()
tempG.remove_nodes_from(nx.isolates(train_graph))
discrete_mapB, B = discreteGraph(tempG)
PySim = PyNetSim.PyNetSim()
NetMartixB = PySim.ReadDataFromAdjacencyMatrix(B)
LRW = PySim.LocalRandomWalk(lamda = 0.9, steps = 3)

discrete_mapC, C = discreteGraph_weight(tempG)
PySim = PyNetSim.PyNetSim()
NetMartixC = PySim.ReadDataFromAdjacencyMatrix(C)
LRWw = PySim.LocalRandomWalk(lamda = 0.9, steps = 3)
'''

# pick out predicted node sim

VC_predict = investors & investors7
score_AA,true_value_AA = calculate_sim_for_specified_pairs(AA, discrete_mapA,test_graph, VC_predict)
score_AAw,true_value_AAw = calculate_sim_for_specified_pairs_single(train_graph, test_graph, VC_predict)

'''
score_AA,true_value_AA = calculate_sim_for_specified_pairs(AA, discrete_mapA,test_graph, VC_predict)
score_K,true_value_K = calculate_sim_for_specified_pairs(K, discrete_mapA,test_graph, VC_predict)

VC_predictB = (investors - set(nx.isolates(train_graph)) ) & investors7
score_LRW,true_value_LRW = calculate_sim_for_specified_pairs(LRW, discrete_mapB,test_graph, VC_predictB)
score_LRW[np.isnan(score_LRW)] = 0
score_LRWw,true_value_LRWw = calculate_sim_for_specified_pairs(LRWw, discrete_mapC,test_graph, VC_predictB)
score_LRWw[np.isnan(score_LRWw)] = 0
'''





# plot
fpr,tpr = roc(score_AA, true_value_AA)
plt.plot(fpr,tpr,color='b', linestyle='-', linewidth = '1')
fpr,tpr = roc(score_AAw, true_value_AAw)
plt.plot(fpr,tpr,color='r', linestyle='-', linewidth = '1')
'''
fpr,tpr = roc(score_AA, true_value_AA)
plt.plot(fpr,tpr,color='b', linestyle='-', linewidth = '1')
fpr,tpr = roc(score_K, true_value_K)
plt.plot(fpr,tpr,color='y', linestyle='-', linewidth = '1')
fpr,tpr = roc(score_LRW, true_value_LRW)
plt.plot(fpr,tpr,color='r', linestyle='-', linewidth = '1')
'''

plt.grid(True,linestyle=':', color='k',linewidth='1')
plt.savefig('LRWLRWw.png')
