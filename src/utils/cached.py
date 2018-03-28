# -*- coding:utf-8 -*-
import pickle as pkl
import os

"""
cahced可以把一个函数的输出缓存起来，然后下次调用的时候直接返回缓存的结果。
注意：仅适用于函数返回值一直不变的情况
"""


def cached(filename):
    def decorator_(method):
        def wrapper(*args, **kargs):
            fp = './cache/'+filename+'.pkl'
            if not os.path.exists(fp):
                tmp = method(*args, **kargs)
                with open(fp, mode='wb') as file:
                    pkl.dump(tmp, file)
                return tmp
            else:
                with open(fp, 'rb') as file:
                    return pkl.load(file)
        return wrapper
    return decorator_


def cache_res(filename, func, *args, **kargs):
    filename = './cache/'+filename+'.pkl'
    if not os.path.exists(filename):
        tmp = func(*args, **kargs)
        with open(filename, mode='wb') as file:
            pkl.dump(tmp, file)
        return tmp
    else:
        with open(filename, 'rb') as file:
            return pkl.load(file)

