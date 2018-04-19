from investment_common_round import Processor
import numpy as np
from collections import namedtuple
import pandas as pd

DIMENSION = 100

if __name__ == "__main__":

    df = pd.read_excel('InvestEvent_1.xlsx')
    processor = Processor()
    processor.convert_data(df)

    print("build_graph")
    processor.build_graph()


    with open('./invest_list.txt', 'w', encoding='utf-8') as f:
        for name in processor.invests:
            f.write(name+'\n')

    PageRank = namedtuple('PageRank', 'name prank')
    ranklist = []
    with open('./prank_round.txt', 'r', encoding='utf-8') as f:
        for ln in f.readlines():
            name, _, pr = ln.partition(':')
            ranklist.append(PageRank(name, float(pr)))


    top100 = ranklist[: DIMENSION]

    columns = ["{}:{:.4}".format(inv, pr) for inv, pr in top100]

    mat = np.zeros(shape = (DIMENSION, DIMENSION))
    for idx, (inv, pr) in enumerate(top100):
        for idx2, (inv2, pr2) in enumerate(top100):
            if inv2 != inv:
                sim = processor.similarity(inv, inv2)
                mat[idx, idx2] = sim
    table = pd.DataFrame(data=mat, index=columns, columns=columns)
    table.to_csv('sim-rank.csv', sep=',')