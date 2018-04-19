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

