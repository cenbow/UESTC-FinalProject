# !utf-8
"""统计2016年度股权投资排名中的VC在我们算法中的排名"""

MY_SORTED_FILE = 'pagerank_comp.txt'
QINGKE_FILE = 'qingke_PE.txt'

rk_dict = dict()
with open(MY_SORTED_FILE, 'r', encoding='utf-8') as f:
    for idx, ln in enumerate(f.readlines()):
        name = ln.split(':')[0]
        rk_dict[name] = idx + 1

qk_rk_list = list()
with open(QINGKE_FILE, 'r', encoding='utf-8') as f:
    for ln in f.readlines():
        ar = ln[:-1].split(' ')
        t = tuple(ar)
        # rank fullname shortname
        qk_rk_list.append(t)

for rk, fn, sn in qk_rk_list:
    if sn in rk_dict.keys() or fn in rk_dict.keys():
        print("{name}\t{rk}\t{our_rk}".format(name=fn, rk=rk, our_rk=rk_dict[fn] if fn in rk_dict.keys() else rk_dict[sn]))