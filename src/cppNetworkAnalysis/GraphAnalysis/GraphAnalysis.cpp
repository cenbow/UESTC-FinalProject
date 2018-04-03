// GraphAnalysis.cpp: 定义控制台应用程序的入口点。
//
//#include "stdafx.h"
#include <vector>
#include <cstring>
#include <fstream>
#include <cmath>
#include <random>
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <map>
#include <cstdlib>
#include <cassert>

#ifdef __GNUC__
#define sprintf_my sprintf
#else
#define sprintf_my sprintf_s
#endif

#include "graph.h"
#include "logger.h"
using namespace std;


class Result
{
public:
	int tp = 0, fp = 0, tn = 0, fn = 0;
	double pricision() { return double(tp) / (tp + fp); }
	double recall() { return double(tp) / (tp + fn); }
	double tpr() { return double(tp) / (tp + fn); }
	double fpr() { return double(fp) / (fp + tn); }
	pair<double, double> roc_pair() { return make_pair(fpr(), tpr()); }
};


int main()
{

	Logger logger("./log.txt", Logger::Level::DEBUG);
	logger.debug("starting program");
	/* 读取文件，构造图
	 * 文件第一行n,m表示图点和边的个数
	 * 之后每一行都包含三个数u,v,w表示一条有向边
	 */

	/*==========================
	construct graph for training
	===========================*/
	ifstream file("./train_graph1.txt");
	int size_node, size_edge;
	file >> size_node >> size_edge;
	Graph projected_graph(size_node);
	map <string, int> str2int;
	int cnt = 0;
	for (int i = 0; i < size_edge; i++)
	{
		double w;
		int u, v;
		file >> u >> v >> w;

		projected_graph.addEdge(Edge(u, v, w));
	}
	file.close();
	logger.debug("finished reading train graph file");
	projected_graph.rearrage();

	//calculating similarity for all pairs
	double *mtr = new double[size_node*size_node];
	fill(mtr, mtr + size_node * size_node, 0);
	for (int nd = 0; nd < size_node; nd++)
	{
		int deg = projected_graph.adjacency_list[nd].size();
		double t = log2(deg);

		auto &adj = projected_graph.adjacency_list[nd];
		for (auto i = adj.begin(); i != adj.end(); i++)
			for (auto j = i + 1; j != adj.end(); j++)
			{
				assert(i->v <= j->v); //FIXME:有重边？
				mtr[(i->v) * size_node + (j->v)] += t;
			}
	}
	logger.debug("finished calculating pairwise similarity!");

	//seperate score into positive and negative
	Array<double> positive;
	for (int u = 0; u < size_node; ++u)
	{
		for (int k = 0; k < projected_graph.adjacency_list[u].size(); ++k)
		{
			int v = projected_graph.adjacency_list[u][k].v;
			if (v <= u) continue;
			positive.push_back(mtr[u*size_node + v]);
		}
	}
	printf("size of positive samples %d\n", positive.size());
	Array<double> negative;
	int nsample_cnt = 0;
	while (nsample_cnt < positive.size())
	{
		nsample_cnt++;
		int a = rand() % (size_node - 1);
		int b = a + 1 + rand() % (size_node - a - 1);
		negative.push_back(mtr[a * size_node + b]);
	}

	//delete[] mtr;

	//figure out optimized threshold by indication -- TP_ratio * TN_ratio
	sort(positive.begin(), positive.end());
	sort(negative.begin(), negative.end());

	double max_score = 0;
	double threshold = 0;
	double tp_ratio, tn_ratio;
	for (int i = 0; i < positive.size(); ++i)
	{
		double* index = bisearch(negative.begin(), negative.end(), positive[i], [](double a, double b) { return a - b; });
		int tp = positive.size() - i;
		int tn = (index - negative.begin());

		double score = (double(tp) / positive.size()) * (double(tn) / negative.size());
		if (max_score < score)
		{
			threshold = positive[i];
			max_score = score;
			tp_ratio = double(tp) / positive.size();
			tn_ratio = double(tn) / negative.size();
		}
	}

	//debug info
	char tmp_buf[100];
	sprintf_my(tmp_buf, "max score: %.4lf", max_score);
	logger.debug(tmp_buf);
	sprintf_my(tmp_buf, "tp_ratio: %.4lf, tn_ratio: %.4lf\n", tp_ratio, tn_ratio);
	logger.debug(tmp_buf);


	/*===========================
	  construct graph for testing
	============================*/
	ifstream file2("./test_graph1.txt");
	int size_node2, size_edge2;
	file2 >> size_node2 >> size_edge2;
	Graph graph_after(size_node2);
	str2int.clear();
	for (int i = 0; i < size_edge2; i++)
	{
		int u, v;
		double w;
		file2 >> u >> v >> w;
		graph_after.addEdge(Edge(u, v, w));
	}
	file2.close();
	logger.debug("finished reading test graph file");


	graph_after.rearrage();
	//mtr = new double[size_node2*size_node2];
	//fill(mtr, mtr + size_node2 * size_node2, 0);
	//for (int nd = 0; nd < size_node2; nd++)
	//{
	//	int deg = graph_after.adjacency_list[nd].size();
	//	double t = log2(deg);
	//	auto &adj = graph_after.adjacency_list[nd];
	//	for (auto i = adj.begin(); i != adj.end(); i++)
	//		for (auto j = i + 1; j != adj.end(); j++)
	//		{
	//			mtr[(i->v) * size_node2 + (j->v)] += t;
	//		}
	//}

	int cnt_p = 0, cnt_n = 0, cnt_tp = 0, cnt_tn = 0;
	int cnt_tp0 = 0, cnt_tn0 = 0;
	for (int i = 0; i < 100000; i++)
	{
		int a = rand() % (size_node - 1);
		int b = a + 1 + rand() % (size_node - a - 1);
		//sample edge (a, b)
		if (graph_after.contain(Edge(a, b, 0.1)))
		{
			cnt_p++;
			//if similarity(train_graph, a, b) > threshold, set true
			if (mtr[a + size_node2 + b] > threshold)
				cnt_tp++;
			//predict true if a and b has edge before.
			if (projected_graph.contain(Edge(a, b, 0.1)))
				cnt_tp0++;
		}
		else {
			cnt_n++;
			if (mtr[a + size_node2 + b] < threshold)
				cnt_tn++;
			if (!projected_graph.contain(Edge(a, b, 0.1)))
				cnt_tn0++;
		}
	}

	sprintf_my(tmp_buf, "test -> tp: %d\n", cnt_tp);
	logger.debug(tmp_buf);
	sprintf_my(tmp_buf, "test -> tn: %d\n", cnt_tn);
	logger.debug(tmp_buf);
	sprintf_my(tmp_buf, "test -> p: %d\n", cnt_p);
	logger.debug(tmp_buf);
	sprintf_my(tmp_buf, "test -> n: %d\n", cnt_n);
	logger.debug(tmp_buf);

	
	printf("tp_ratio: %lf\n tn_ratio: %lf\n", double(cnt_tp) / cnt_p, double(cnt_tn) / cnt_n);
	printf("simple: tp_ratio: %lf\n tn_ratio: %lf\n", double(cnt_tp0) / cnt_p, double(cnt_tn0) / cnt_n);

	/*====================
	calculating AUC of ROC
	====================*/

	

	delete[] mtr;

	system("pause");
	return 0;
}
