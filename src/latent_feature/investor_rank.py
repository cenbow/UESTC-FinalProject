import os
from datetime import datetime
from cached import cached, cache_res
import networkx as nx
import pandas as pd


def ranking_summary(namelist_path, rank):
    with open(namelist_path, 'r', encoding='utf-8') as namelist:
        match_cnt = 0
        top5cnt = 0
        top10cnt = 0
        total_cnt = 0

        sorted_rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        sorted_rank = {name: rk for rk, (name, _) in enumerate(sorted_rank)}

        for ln in namelist.readlines():
            ln.strip()
            idx, fn, sn = ln.split()
            if fn in sorted_rank or sn in sorted_rank:
                pr = sorted_rank.get(fn, sorted_rank[sn])
                match_cnt += 1
                if pr < len(sorted_rank) * 0.05:
                    top5cnt += 1
                if pr < len(sorted_rank) * 0.1:
                    top10cnt += 1
            total_cnt += 1

        print('{::^78}'.format(namelist_path))

        print(':{:^19}'.format("Total"), end='')
        print('{:^19}'.format("Match"), end='')
        print('{:^19}'.format("Top 5%"), end='')
        print('{:^19}:'.format("Top 10%"))

        print(':{:^19}'.format(total_cnt), end='')
        print('{:^19}'.format(match_cnt), end='')
        print('{:^19}'.format(top5cnt), end='')
        print('{:^19}:'.format(top10cnt))

        print(':' * 78)


@cached('dictify')
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
    data = dict()
    companies = set()
    invests = set()

    for idx, row in dataframe.iterrows():
        # Date filter
        # dt = datetime.strptime(row['日期(time)'], "%Y.%m.%d")
        #
        # if dt.year > 2016:
        #     continue

        company = row['公司(company)']
        companies.add(company)
        round_ = row['融资轮数(round)']
        invests_ = eval(row['投资机构(invests)'])
        assert (isinstance(invests_, list))

        if '投资方未透露' in invests_:
            invests_ = []
        if company not in data:
            data[company] = dict()
        if round_ not in data[company]:
            data[company][round_] = invests_
            invests = invests.union(invests_)
    return data, companies, invests


@cached('company.bipartite')
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


@cached('round.bipartite')
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


@cached('company.projected.tao')
def tao_one_mode_projection(bigraph, projection):
    """
    :param g: networkx.Bipartite
    :param B: subset of nodes to project on
    :return: networkx.Graph
    """
    projected_graph = nx.DiGraph()
    projected_graph.add_nodes_from(projection)
    for u in projection:
        for v in projection:
            w = 0.0
            common_neighbors = set(bigraph.adj[u]).intersection(set(bigraph.adj[v]))
            for l in common_neighbors:
                # assume g is unweighted bigraph;
                w += 1 / len(bigraph[l])
            if len(common_neighbors) != 0:
                projected_graph.add_edge(u, v, weight=w)
    return projected_graph


df = pd.read_excel('InvestEvent_1.xlsx')
data, _, investors = dictify(df)
bipartite = build_graph(data)
graph = tao_one_mode_projection(bipartite, investors)

pagerank = cache_res('company.pagerank', nx.pagerank, graph, weight='weight')

# ranking_summary('./qingke_AG.txt', pagerank)
# ranking_summary('./qingke_VC.txt', pagerank)
# ranking_summary('./qingke_PE.txt', pagerank)

# katzrank = cache_res('company.katzrank', nx.katz_centrality, graph, 0.01, weight='weight')
#
# ranking_summary('./qingke_AG.txt', katzrank)
# ranking_summary('./qingke_VC.txt', katzrank)
# ranking_summary('./qingke_PE.txt', katzrank)

betweenessrank = cache_res('company.betweenness', nx.betweenness_centrality, graph, weight='weight')

# ranking_summary('./qingke_AG.txt', betweenessrank)
# ranking_summary('./qingke_VC.txt', betweenessrank)
# ranking_summary('./qingke_PE.txt', betweenessrank)

closeness = cache_res('company.closeness', nx.closeness_centrality, graph, distance='weight')
#
# ranking_summary('./qingke_AG.txt', closeness)
# ranking_summary('./qingke_VC.txt', closeness)
# ranking_summary('./qingke_PE.txt', closeness)
