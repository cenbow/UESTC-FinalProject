# -*- coding: utf-8 -*-
import sys


class ProgressBar():
    def __init__(self, iter_, total=None):
        self._iter = iter_
        self.total = total if total else len(iter_)

    def __iter__(self):
        for idx, it in enumerate(self._iter):
            sys.stdout.write('\r{percentage:.1f}% {bar:<80}| {item}'.format(percentage=100 * idx / self.total,
                                                                            bar='█' * int(80 * idx / self.total),
                                                                            item=it).replace('\n', ''))
            sys.stdout.flush()
            yield it
