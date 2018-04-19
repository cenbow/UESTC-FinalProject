#! py3
import sys, os, q
import threading

import numpy as np
import pickle

"""
Lantent Feature for Undirected
n: size of node
d: dimmension of feature
- make sure: mat is symmetric matrix
- make sure: diag element of mat is 1
- make sure: mat only contains element {0, 1}

every update use an element(node) to update its own feature
time complexity: n * d


loss function is F2 norm of difference between real matrix and output matrix
"""

class UndirectedLatentFeatureModel:
    eta = 0.02

    def __init__(self, feature_dimmension, node_size):
        self._d = feature_dimmension
        self._n = node_size
        self.U = np.random.uniform(low=0, high=1, size=(node_size, feature_dimmension))
        self.U /= np.linalg.norm(self.U, axis=1).reshape(node_size, 1)

    def update(self, i, y):
        self.U[i, :] += - self.eta * self.gradient(i, y)

    def loss(self, i, y):
        """F_2 norm"""
        feature = self.U[i, :]
        res = self.U @ feature.transpose()
        return np.linalg.norm(res - y, 2)

    def total_loss(self, mat):
        return np.linalg.norm(self.U @ self.U.transpose() - mat, 2)

    def gradient(self, i, y):
        """ time complexity : n * d """
        y = y.transpose()
        feature = self.U[i, :]
        delta = self.U @ np.transpose(feature) - y  # n * 1
        res = 2 * delta.transpose() @ self.U  # 1 * d
        res += 2 * delta[i] * feature
        return res / np.linalg.norm(res)

    def output(self):
        return self.U  @ np.transpose(self.U)


stopIter = False


def getkey():
    global stopIter
    while True:
        x = sys.stdin.read(1)[0]
        print(type(x))
        if x == 'q':
            stopIter = True
            return


if __name__ == "__main__":
    t = threading.Thread(target=getkey)
    t.start()

    node_size, edge_size = 0, 0
    mat = None
    with open('./projected.txt', "r") as file:
        for idx, ln in enumerate(file.readlines()):
            if idx == 0:
                node_size, edge_size = ln.split()
                node_size, edge_size = int(node_size), int(edge_size)
                mat = np.zeros(shape=(node_size, node_size), dtype='float')
                continue
            u, v = ln.split()
            u, v = int(u), int(v)
            mat[u][v] = 1
            mat[v][u] = 1
    for i in range(node_size):
        mat[i][i] = 1

    ulm = UndirectedLatentFeatureModel(100, node_size)
    for loop in range(1000):
        if stopIter: break
        for i in range(node_size):
            if stopIter: break
            ulm.update(i, mat[i])
        print("%s: %s" % (loop, ulm.total_loss(mat)))

    tmp = ulm.output()
    tmp = np.floor(tmp+0.5)
    with open("./paramenters_ulm.pkl", "w") as f:
        pickle.dump(ulm.U, f)

    print(mat[:20, :20])
    print(tmp[:20, :20])
    print(np.count_nonzero(tmp - mat)/(node_size*node_size))
