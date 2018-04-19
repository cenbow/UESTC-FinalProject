import os, sys, q
import numpy as np
import pickle as pkl
import multiprocessing as mp
from collections import namedtuple

class LatentModel():
    eta = 0.001
    regularizer_l = 0.1
    regularizer_u = 0.1

    def __init__(self, feature_dimmension, node_size):
        np.random.seed()
        self._fd = feature_dimmension
        self._ns = node_size
        norm = np.math.sqrt(self._fd)
        # self.Lambda = np.random.uniform(low=0, high=1/norm, size=(self._fd, self._fd))
        self.Lambda = np.identity(self._fd)
        self.Feature = np.random.uniform(low=0, high=1, size=(self._ns, self._fd))

    def gradient(self, adjacency_matrix):
        """Calculate Gradient vector"""
        U = self.Feature
        L = self.Lambda
        G_ = U @ L @ np.transpose(U)
        G_delta = G_ - adjacency_matrix

        # main term
        delta_lambda = 0.1 * (np.transpose(U) @ np.transpose(G_delta) @ U)
        # minus term
        # tmp = sum(2 * G_delta[i, i] * np.tensordot(U[i, :], U[i, :], axes=0) for i in range(self._ns))
        # delta_lambda -= tmp
        # # regularizer term
        # tmp = np.array([np.inner(L[k, :], L[k, :]) - 1 for k in range(self._fd)]).reshape(self._fd, 1) * L
        # delta_lambda += tmp * self.regularizer_l
        # assert (delta_lambda.shape == tmp.shape)

        delta_feature = 2 * (L @ np.transpose(U) @ G_delta + np.transpose(L) @ np.transpose(U) @ np.transpose(G_delta))
        delta_feature = np.transpose(delta_feature)
        # tmp = np.array([G_delta[i, i] for i in range(self._ns)]).reshape(self._ns, 1)
        # delta_feature += -2 * tmp * (U @ (np.transpose(L) + L)) + 2 * U
        # tmp = np.diag([G_delta[i, i] for i in range(self._ns)])
        # delta_feature -= 2 * tmp @ (U @ (np.transpose(L) + L))
        # regularizer term
        # tmp = np.array([np.inner(U[k, :], U[k, :]) - 1 for k in range(self._ns)]).reshape(self._ns, 1) * U
        # delta_feature += tmp * self.regularizer_u
        return delta_lambda, delta_feature

    def debug_gradient_update(self, mat):
        delta_lambda, delta_feature = self.gradient(mat)
        self.Lambda += -self.eta * delta_lambda
        self.Feature += -self.eta * delta_feature

    def loss(self, data):
        res = np.linalg.norm(self.Feature @ self.Lambda @ np.transpose(self.Feature) - data, 2) ** 2
        # res += abs(np.linalg.norm(self.Lambda, 2) - self._fd) * self.regularizer_l
        # res += abs(np.linalg.norm(self.Feature, 2) - self._ns) * self.regularizer_u
        return res

    def save(self, filename):
        with open(filename, 'w') as file:
            pkl.dump((self.Lambda, self.Feature), file)

    def load(self, filename):
        with open(filename, 'r') as file:
            self.Lambda, self.Feature = pkl.load(filename)
        self._ns = self.Feature.shape[1]
        self._fd = self.Feature.shape[0]


if __name__ == '__main__':
    node_size, edge_size = 0, 0
    mat = None
    q('start reading graph')
    with open('./debug_graph.txt', 'r') as tgf:
        for idx, ln in enumerate(tgf.readlines()):
            q(ln)
            if idx == 0:
                node_size, edge_size = ln.split()
                node_size, edge_size = int(node_size), int(edge_size)
                mat = np.zeros(shape=(node_size, node_size), dtype='float')
                continue
            u, v, w = ln.split()
            u, v, w = int(u), int(v), float(w)
            mat[u][v] = w
    q('finish construct matrix')
    for i in range(node_size):
        mat[i][i] = 1.0

    lm = LatentModel(20, node_size)
    for loop in range(1500):
        q('updatign: %s/1000' % loop)
        lm.debug_gradient_update(mat)
        if loop % 100 == 0:
            print("index %s: loss = %.3f" % (loop, lm.loss(mat)))
    print("loss = %.3f" % lm.loss(mat))

    matrix_ = np.zeros(shape=(mat.shape))
    matrix_ = lm.Feature @ lm.Lambda @ lm.Feature.transpose()
    print(mat)
    print(matrix_)

    # lm.save('./latent_model_parameters.pkl')

    # matrix = np.zeros(shape=)
