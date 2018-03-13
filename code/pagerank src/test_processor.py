from unittest import TestCase
import pandas as pd
import networkx as nx
from investment_common_company import Processor

class TestProcessor(TestCase):
    def setUp(self):
        filename = "./InvestEvent_1.xlsx"
        self.df = pd.read_excel(filename)[:10]
        self.num_company = self.df['公司(company)'].drop_duplicates().count()
        self.processor = Processor()

    def test_convert_data(self):
        self.processor.convert_data(self.df)
        self.assertEqual(len(self.processor.companies), self.num_company)


    def test_build_graph(self):
        self.processor.build_graph()
        # nx.draw(self.processor.graph)

    def test_tao_one_mode_projection(self):
        self.processor.tao_one_mode_projection()
        # nx.draw(self.processor.projected_graph)