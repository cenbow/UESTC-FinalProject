// GraphAnalysis.cpp: 定义控制台应用程序的入口点。
//
#include "stdafx.h"
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


class Measurement
{
public:
	int tp = 0, fp = 0, tn = 0, fn = 0;
	double precision() { return double(tp) / (tp + fp); }
	double recall() { return double(tp) / (tp + fn); }
	double tpr() { return recall(); }
	double fpr() { return double(fp) / (fp + tn); }
	pair<double, double> roc_pair() { return make_pair(fpr(), tpr()); }
	double F1() { return 2 * precision() * recall() / (precision() + recall()); }
	void summary(string title = "")
	{

		printf("-----------------------------\n\
Summary: %s\n \t\t\t Condition Positive \t Condition Negative\n\
Predicted Positive\t %10d \t\t %10d\n\
Predicted Negative\t %10d \t\t %10d\n",
			title.c_str(),
			tp, fp,
			fn, tn
		);
		printf("Pricision: %.4lf\nRecall : %.4lf\n", precision(), recall());
		printf("TP ratio: %.4lf\nFP ratio: %.4lf\n", tpr(), fpr());
		puts("----------------------------\n");
	}
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
	Graph training_graph("./train_graph1.txt");

	//calculating similarity for all pairs
	int size_node = training_graph.size_node;
	double *mtr = new double[size_node * size_node];
	fill(mtr, mtr + size_node * size_node, 0);
	for (int nd = 0; nd < size_node; nd++)
	{
		int deg = training_graph.adjacency_list[nd].size();
		// Adamic-Adar Index
		double t = log2(deg);
		// Resource Allocation Index (RA)
		//double t = double(1) / deg;

		auto &adj = training_graph.adjacency_list[nd];
		double sum_weight = 0;
		for (auto i = adj.begin(); i != adj.end(); i++)
			sum_weight += i->w;
		//assert(sum_weight > 1); //FIXME: 权重和小于1
		for (auto i = adj.begin(); i != adj.end(); i++)
			for (auto j = i + 1; j != adj.end(); j++)
			{
				//double t = i->w * j->w; // nd 到另外两个点的权重。 FIXME:方向反了
				//i(resp. i) is edge from nd to i->v (resp. j->v)
				assert(i->v <= j->v); //FIXME:有重边？

				//those are used to calculating weighted Adamic-Adar Index
				double avg_w = 0;
				try {
					auto e = training_graph.get_edge(i->v, nd);
					avg_w += e.w;
					e = training_graph.get_edge(j->v, nd);
					avg_w += e.w;
					avg_w /= 2;
				}
				catch (const out_of_range& oor)
				{
					cout << oor.what() << endl;
					exit(-1);
				}

				mtr[(i->v) * size_node + (j->v)] += avg_w / log2(1+sum_weight);
			}
	}
	logger.debug("finished calculating pairwise similarity!");


	//seperate score into positive and negative
	//positive: the similarity value for pair (u, v) which is edge in training graph
	//negative: the similarity value for pair (u, v) which is not edge in trainingg graph
	Array<double> positive;
	for (int u = 0; u < size_node; ++u)
	{
		for (int k = 0; k < training_graph.adjacency_list[u].size(); ++k)
		{
			int v = training_graph.adjacency_list[u][k].v;
			if (v <= u) continue;
			positive.push_back(mtr[u*size_node + v]);
		}
	}
	printf("size of positive samples %d\n", positive.size());
	Array<double> negative;
	int nsample_cnt = 0;
	while (nsample_cnt < positive.size())
	{

		int a = rand() % (size_node - 1);
		int b = a + 1 + rand() % (size_node - a - 1);
		if (training_graph.contain(Edge(a, b, 0.1)))
			continue;
		nsample_cnt++;
		negative.push_back(mtr[a * size_node + b]);
	}

	//delete[] mtr;

	//figure out optimized threshold by indication -- TP_ratio * TN_ratio
	sort(positive.begin(), positive.end());
	sort(negative.begin(), negative.end());

	double max_score = 0;
	double threshold = 0;
	Measurement eval_aai;
	for (int i = 0; i < positive.size(); ++i)
	{
		double* index = bisearch(negative.begin(), negative.end(), positive[i], [](double a, double b) { return a - b; });
		eval_aai.tp = positive.size() - i;
		eval_aai.fn = i;
		eval_aai.tn = index - negative.begin();
		eval_aai.fp = negative.end() - index;

		double score = eval_aai.F1();
		if (max_score < score)
		{
			threshold = positive[i];
			max_score = score;
			eval_aai.summary("test");
		}
	}

	//debug info
	char tmp_buf[100];
	sprintf_my(tmp_buf, "max score: %.4lf", max_score);
	logger.debug(tmp_buf);




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

	Measurement Adamic_Adar_Index, simple;

	/*===========================
	construct graph for testing
	============================*/
	Graph test_graph("./test_graph1.txt");


	int size_node2 = test_graph.size_node;

	for (int i = 0; i < 1000000; i++)
	{
		int a = rand() % (size_node - 1);
		int b = a + 1 + rand() % (size_node - a - 1);
		//sample edge (a, b)
		if (test_graph.contain(Edge(a, b, 0.1))) // Condition Positive
		{
			//if similarity(train_graph, a, b) > threshold, set true
			if (mtr[a + size_node2 + b] > threshold) // Predicted Positive
			{
				Adamic_Adar_Index.tp++;
			}
			else // Predicted Negative
			{
				Adamic_Adar_Index.fn++;
			}

			//predict true if a and b has edge before.
			if (training_graph.contain(Edge(a, b, 0.1)))
				simple.tp++;
			else
				simple.fn++;
		}
		else { // Condition Negative
			if (rand() % 100 > 1) continue;
			if (mtr[a + size_node2 + b] < threshold) // Predicted Negative
			{
				Adamic_Adar_Index.tn++;
			}
			else // Predicted Positive
			{
				Adamic_Adar_Index.fp++;
			}
			if (!training_graph.contain(Edge(a, b, 0.1)))
				simple.fp++;
			else
				simple.tn++;
		}
	}


	/*==========================
	DONE: 两张图同样的点编号不一样
	解决思路： 用两张图的结点并作为两张图的结点
	============================*/

	simple.summary("simple");


	Adamic_Adar_Index.summary("Adamic-Adar Index");

	/*====================
	calculating AUC of ROC
	====================*/



	delete[] mtr;

	system("pause");
	return 0;
}
