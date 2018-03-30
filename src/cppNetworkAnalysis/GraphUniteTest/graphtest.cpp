#include "stdafx.h"
#include "CppUnitTest.h"
#include "../GraphAnalysis/graph.h"
#include <random>
#include <iostream>
#include <vector>
#include <fstream>
#include <ctime>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace GraphUniteTest
{		
	TEST_CLASS(UnitTest1)
	{
	public:
		
		TEST_METHOD(ArrayConstruction)
		{
			// TODO: Your test code here
			Array<int> a;
			for (int i = 0; i < 10000; i++)
			{
				a.push_back(rand() % 100000);
			}
			Assert::AreEqual(a.size(), 10000);
			sort(a.begin(), a.end());
			bool ordered = true;
			for (auto i = a.begin() + 1; i != a.end(); ++i)
				if (*(i - 1) > *i) ordered = false;
			Assert::IsTrue(ordered);
		}
		TEST_METHOD(GraphConstruction)
		{
			srand(time(0));
			Graph g(100);
			Assert::IsTrue(g.adjacency_list._array != nullptr);
			for (int i = 0; i < 1000; i++)
			{
				int u = rand() % 100;
				int v = rand() % 100;
				double w = rand() % 20;
				g.addEdge(Edge(u, v, w));
			}
			int total_edge = 0;
			for (int i = 0; i < g.size_node; i++)
			{
				total_edge += g.adjacency_list[i].size();
			}
			Assert::AreEqual(1000, total_edge);
			g.rearrage();
			int u = rand() % g.size_node;
			int idx = rand() % g.adjacency_list[u].size();
			int v = g.adjacency_list[u][idx].v;
			Assert::IsTrue(g.contain(Edge(u,v,0.1)));
			//Assert::IsFalse(g.contain(Edge(10, 84, 0.1)));
		}
		TEST_METHOD(BinarySearch)
		{
			Array<int> a;
			for (int i = 0; i < 10000; i++)
			{
				a.push_back(2 * (rand() % 1000000));
			}
			sort(a.begin(), a.end());
			for (int i = 0; i < 100; i++)
			{
				int pos = rand() % a.size();
				auto idx = bisearch(a.begin(), a.end(), a[pos], [](int a, int b) { return a - b; });
				Assert::AreEqual(*idx, a[pos]);
			}
			for (int i = 0; i < 100; i++)
			{
				int val = (rand() % 100000) * 2 + 1;
				auto idx = bisearch(a.begin(), a.end(), val, [](int a, int b) {return a - b; });
				Assert::IsFalse(*idx == val);
			}
		}
		TEST_METHOD(SimilarityTest)
		{
			ifstream file("C:\\Users\\Administrator\\UESTC-FinalProject\\src\\cppNetworkAnalysis\\GraphAnalysis\\test_graph1.txt");
			Assert::IsFalse(!file);
			int size_node, size_edge;
			file >> size_node >> size_edge;

			Graph projected_graph(size_node);
			int cnt = 0;
			for (int i = 0; i < size_edge; i++)
			{
				double w;
				int u, v;
				file >> u >> v >> w;
				projected_graph.addEdge(Edge(u, v, w));
			}
			file.close();
			projected_graph.rearrage();


			//calculating score for all pairs
			//double *mtr = new double[size_node*size_node];
			vector<double> mtr(size_node *size_node / 2, 0);
			//Array<double> mtr;
			//mtr.resize(size_node * size_node);
			//fill(mtr.begin(), mtr.end(), 0);
			//fill(mtr, mtr + size_node * size_node, 0.0);
			for (int nd = 0; nd < size_node; nd++)
			{
				int deg = projected_graph.adjacency_list[nd].size();
				double t = log2(deg);

				auto &adj = projected_graph.adjacency_list[nd];
				for (auto i = adj.begin(); i != adj.end(); i++)
					for (auto j = i + 1; j != adj.end(); j++)
					{
						mtr[(i->v) * size_node + (j->v)] += t;
					}
			}

			int u = rand() % (projected_graph.size_node - 1);
			int v = u + 1 + rand() % (projected_graph.size_node - u - 1);
			projected_graph.rearrage();
			
			auto &adj_u = projected_graph.adjacency_list[u];
			auto &adj_v = projected_graph.adjacency_list[v];
			double res = 0;
			for (auto ptr_e = adj_u.begin(); ptr_e != adj_u.end(); ptr_e++)
			{
				auto idx = bisearch(adj_v.begin(), adj_v.end(), *ptr_e, [](const Edge& a, const Edge& b) { return a.v - b.v; });
				//projected_graph.contain(Edge())
				if (idx->v != ptr_e->v) continue;
				int deg = projected_graph.adjacency_list[ptr_e->v].size();
				res += log2(double(deg));
			}
			Assert::AreEqual(res, mtr[u * projected_graph.size_node + v]);
		}
	};
}