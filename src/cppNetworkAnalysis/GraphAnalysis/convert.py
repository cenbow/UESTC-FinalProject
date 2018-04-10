import sys, os
import pickle as pkl
from progressbar import ProgressBar
import time, q


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("please input the file to convert")
        exit(-1)

    str_d = {} # mapping company name to integer
    if os.path.exists('./companies_name_2_int.pkl'):
        with open('./companies_name_2_int.pkl', 'rb') as dic:
            str_d = pkl.load(dic, encoding='utf-8')
    cnt = len(str_d)
    total_lines = 0

    with open(sys.argv[1], "r", encoding='utf-8') as file:
        _, total_lines = file.readline().split()
        total_lines = int(total_lines)

    with open(sys.argv[1], "r", encoding='utf-8') as file:
        with open(sys.argv[2], 'w') as output:
            for idx, ln in enumerate(ProgressBar(file.readlines(), total_lines)):
                if idx == 0:
                    output.write(ln)
                    continue

                try:
                    a, b, c = ln.split('\t')
                except:
                    print('error found in line @ %s of file %s\n' % (idx, sys.argv[1]))
                    print('content: %s \n' % ln.split('\t'))
                    exit(-2)
                q(repr(a))
                q(repr(b))
                if a not in str_d:
                    str_d[a] = cnt
                    cnt += 1
                if b not in str_d:
                    str_d[b] = cnt
                    cnt += 1
                output.write("%s %s %s" % (str_d[a], str_d[b], c))

    with open('./companies_name_2_int.pkl', 'wb') as out:
        pkl.dump(str_d, out)
    print("finished")

