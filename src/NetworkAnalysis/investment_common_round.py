import os
import math
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import pandas as pd
# import q

# q("============new instance=============")


class Processor:
    def __init__(self):
        self.graph = nx.Graph()
        self.projected_graph = nx.DiGraph()
        self.data = dict()
        self.companies = set()
        self.invests = set()
        self.prank = dict()

    def convert_data(self, dataframe):
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
        self.data = dict()
        self.companies = set() #set of str
        self.invests = set() # set of str

        for idx, row in dataframe.iterrows():
            company = row['公司(company)']
            self.companies.add(company)
            round_ = row['融资轮数(round)']
            invests_ = eval(row['投资机构(invests)'])
            assert(isinstance(invests_, list))

            if '投资方未透露' in invests_:
                invests_ = []
            if company not in self.data:
                self.data[company] = dict()
            if round_ not in self.data[company]:
                self.data[company][round_] = invests_
                self.invests = self.invests.union(invests_)

    def build_graph(self):
        g = nx.Graph()
        # 二部图： L = {(company, round)}, R={investors}
        for company in self.data.keys():
            # g.add_node(company)
            rounds = self.data[company]
            for round_ in rounds.keys():
                # g.add_nodes_from(rounds[round_])
                g.add_edges_from([((company, round_), invest)
                    for invest in rounds[round_]])

                self.graph = g
        # q(g.nodes())

    def similarity(self, a, b):
        t = set(self.graph.adj[a]).intersection(self.graph.adj[b])
        sum = 0.0
        for v in t:
            deg = len(self.graph.adj[v])
            sum += 1/math.log(deg)
        return sum

    def tao_one_mode_projection(self):
        """
        :param g: networkx.Bipartite
        :param B: subset of nodes to project on
        :return: networkx.Graph
        """
        self.projected_graph = nx.DiGraph()
        self.projected_graph.add_nodes_from(self.invests)
        for u in self.invests:
            for v in self.invests:
                w = 0.0
                common_neighbors = set(self.graph.adj[u]).intersection(
                        set(self.graph.adj[v]))
                for l in common_neighbors:
                    # assume g is unweighted graph
                    w += 1 / len(self.graph[l])
                if len(common_neighbors) != 0:
                    self.projected_graph.add_edge(u, v, weight=w)

    def rank(self):
        self.prank = nx.pagerank(self.projected_graph, weight='weight')


print(__name__)

if __name__ == "__main__":
    print(os.path.dirname(__file__))
    os.path.exists('InvestEvent_1.xlsx')
    df = pd.read_excel('InvestEvent_1.xlsx')
    # q(df[:5])
    processor = Processor()
    processor.convert_data(df)

    processor.build_graph()

    processor.tao_one_mode_projection()

    # print('ranking')

    # g = processor.projected_graph
    # pos = nx.spring_layout(g, k=3, scale=10)
    # nx.draw_networkx_nodes(g, node_size=50, pos=pos)
    # nx.draw_networkx_edges(g, pos=pos)
    #
    # nx.draw(processor.projected_graph, pos)
    # labels = nx.get_edge_attributes(processor.projected_graph, 'weight')
    #
    # nx.draw_networkx_edge_labels(processor.projected_graph, pos, edge_labels=labels)
    # plt.show()

    processor.rank()
    # print(processor.projected_graph.edges())
    # print("page rank: %s" % processor.prank)
    #
