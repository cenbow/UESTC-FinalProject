# -- coding:utf-8 --
# !~/anaconda3/bin/python3
import os, sys
from datetime import datetime
from utils.cached import cached, cache_res
import networkx as nx
import pandas as pd
import numpy as np
from collections import defaultdict
import array, bisect, math
import itertools as its
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

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
            w = w/bigraph.degree(v)
            if w != 0.0:
                projected_graph.add_edge(u, v, weight=w)
    return projected_graph


def simAA(G, u, v):
    common_neighbors = set(G.adj[u]).intersection(G.adj[v])
    assert(all(u in G.adj[w] for w in common_neighbors))
    assert(all(v in G.adj[w] for w in common_neighbors))
    return sum(1 / math.log(G.degree[w], 2) for w in common_neighbors)

def simAA_weight(G,u,v,alpha):
    common_neighbors = set(G.adj[u]).intersection(G.adj[v])
    assert(all(u in G.adj[w] for w in common_neighbors))
    assert(all(v in G.adj[w] for w in common_neighbors))
    return sum((math.pow(float(G.get_edge_data(u,w,default=0.0)['weight']),alpha) + math.pow(float(G.get_edge_data(w,v,default=0.0)['weight']),alpha)) 
            / math.log(1+sum(math.pow(float(G.get_edge_data(w,k,default=0.0)['weight']),alpha)for k in G.adj[w]),2)
                for w in common_neighbors)                                                                                                                    
    
    
def linear_model(dataX,dataY):
    reg = LinearRegression()
    reg.fit(dataX,dataY)

    LinearModel = {}
    # 截距值
    LinearModel['intercept'] = reg.intercept_
    # 回归系数（斜率值）
    LinearModel['coefficient'] = reg.coef_
    # error
    LinearModel[' coefficient_R^2'] = reg.score(dataX,dataY)

    plt.scatter(dataX,dataY,color = 'blue')
    plt.plot(dataX,reg.predict(dataX),color = 'red',linewidth = 4)
    plt.title('VC pair')
    plt.xlabel('before2017')
    plt.ylabel('after2017')
    plt.savefig("Correlation_AA_weight.png")
    print ("Finish ploting")
    return LinearModel
    
def logRegression_model(sim_train,sim_test,coinvest_train,coinvest_test):
    #标准化特征值
    sc = StandardScaler()
    sc.fit(sim_train)
    X_train_std = sc.transform(sim_train)
    X_test_std = sc.transform(sim_test)
    
    #训练逻辑回归模型
    logreg = LogisticRegression()
    logreg.fit(sim_train,coinvest_train)
    logRegressionModel = {}
    
    logRegressionModel['predict_proba'] = logreg.predict_proba(X_test_std)
    logRegressionModel['score'] = logreg.score(X_test_std,coinvest_test)
    
    plt.scatter(sim_test,predict(sim_test),color = 'blue')
    plt.scatter(sim_train,predict(sim_train),color = 'red')
    plt.title('VC pair')
    plt.xlabel('simAA')
    plt.ylabel('coinvest')
    plt.savefig("simAA_coinvest.png")
    print ("Finish ploting")   
    return logRegressionModel
    

# =========================================================
df = pd.read_excel('InvestEvent_1.xlsx')
dataX, dataY,  _, investors = dictify(df)

# filename开头用company的含义？
X_bipartite = cache_res("company.bipartite.X", build_graph, dataX)
X_graph = cache_res('company.projected.X', tao_one_mode_projection, X_bipartite, investors)

Y_bipartite = cache_res('company.bipartite.test', build_graph, dataY)
Y_graph = cache_res('company.projected.test', tao_one_mode_projection, Y_bipartite, investors)

sim_train = array.array('d')
sim_test = array.array('d')
coinvest_train = array.array('d')
coinvest_test = array.array('d')

for u in X_graph.nodes():
    for v in X_graph.nodes():
        if u == v : continue
        if (u not in Y_graph.nodes() or v not in Y_graph.nodes()):
            continue
        sim_train.append(simAA(X_graph, u, v))
        sim_test.append(simAA(Y_graph, u, v))
        if (u,v) in X_graph.edges():coinvest_train.append(1)
        else: coinvest_train.append(0)
        if (u,v) in Y_graph.edges():coinvest_test.append(1)
        else: coinvest_test.append(0)
    
sim_train = np.array(sim_train.tolist())
sim_train = np.reshape(sim_train,(-1,1))
logRegressionModel = logRegression_model(sim_train, sim_test, coinvest_train, coinvest_test)
with open('simAA_coinvest.txt', 'w') as output:
    for key,value in logRegressionModel.items():
        output.write('{0}:{1}'.format(key,value))



# alpha = np.arange(-1.0,1.0,0.05)
# for i in alpha:
    #取交集
    # for u in X_graph.nodes():
        # for v in X_graph.nodes():
            # if u == v : continue
            # if (u not in Y_graph.nodes() or v not in Y_graph.nodes()):
                # continue
            # X_set.append(simAA_weight(X_graph, u, v,i))
            # Y_set.append(simAA_weight(Y_graph, u, v,i))
    
    # X_set = np.array(X_set.tolist())
    # X_set = np.reshape(X_set,(-1,1))
    # LinearModel = linear_model(X_set,Y_set)
    # with open('Correlation_AA_weight.txt', 'w') as output:
        # for key,value in LinearModel.items():
            # output.write('{0}:{1}'.format(key,value))

        
