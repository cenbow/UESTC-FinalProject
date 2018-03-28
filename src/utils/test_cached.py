from unittest import TestCase
import os
import pickle as pkl
from cached import cached
import shutil


class TestCached(TestCase):
    def setUp(self):
        shutil.rmtree('./cache')
        os.mkdir('./cache')

    def test_cached(self):
        @cached('test')
        def build_tuple(n):
            return tuple(range(n))

        target = (0, 1, 2, 3, 4)
        self.assertTupleEqual(target, build_tuple(5))
        self.assertTrue(os.path.exists('./cache/test.pkl'))

        with open('./cache/test.pkl', 'rb') as file:
            tmp = pkl.load(file)
        self.assertEqual(target, tmp)