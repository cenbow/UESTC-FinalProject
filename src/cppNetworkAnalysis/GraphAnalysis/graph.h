#include <functional>
#include "stdafx.h"
#include <algorithm>
#include <string>
using namespace std;

class Edge
{
public:
	int u, v;
	double w;
	Edge() {}
	Edge(int a, int b, double c) :u(a), v(b), w(c) {}
	bool operator==(const Edge &other)
	{
		return this->u == other.u && this->v == other.v;
	}
	bool operator!=(const Edge &other)
	{
		return !(*this == other);
	}
};
template<class T>
class Array
{
public:
	T * _array = nullptr;
	int max_size = 10;
	int size() { return size_; }
	Array()
	{
		_array = new T[max_size];
	}

	~Array()
	{
		if (_array != 0) delete[] _array;
	}
	void push_back(const T &other)
	{
		_array[size_++] = other;
		if (size_ == max_size)
		{
			auto _array_new = new T[max_size *= 1.3];
			memcpy(_array_new, _array, sizeof(T) * size_);
			delete[] _array;
			_array = _array_new;
		}
	}
	T &operator[](int idx)
	{
		return _array[idx];
	}
	void resize(size_t new_size)
	{
		//这里有个错误： resize后数组的大小size_没有改变，这样子导致size(), end()函数可能用法不对
		//不过我这里只有Graph创建邻接表才用到，而且只有外层用到，所以没有引发任何bug
		//FIXME:
		T* _array_new = new T[max_size = new_size];
		if (size_ != 0)
			memcpy(_array_new, _array, sizeof(T) * size_);
		delete[] _array;
		_array = _array_new;
	}

	T* begin()
	{
		return _array;
	}
	T* end()
	{
		return _array + size_;
	}
private:
	int size_ = 0;
};


template <class T, class Compare>
T* bisearch(T* first, T* last, const T& val, Compare cmp)
{
	while (first  < last - 1)
	{
		T* mid = first + (last - first) / 2;
		if (cmp(*mid, val) <= 0)
			first = mid;
		else
			last = mid;
	}
	// if last don't change, mean not found
	return first;
}


class Graph
{
public:
	int size_node = 0;
	Array< Array<Edge> > adjacency_list;

	//Graph(string filepath)
	//{
	//	ifstream file(filepath);
	//	int size_edge;
	//	file >> size_node >> size_edge; // size_node is member of Graph
	//	adjacency_list.resize(size_node);
	//	for (int i = 0; i < size_edge; i++)
	//	{
	//		double w;
	//		int u, v;
	//		file >> u >> v >> w;
	//		addEdge(Edge(u, v, w));
	//	}
	//	file.close();
	//	rearrage();
	//}
	Graph(int size_node_):adjacency_list()
	{
		adjacency_list.resize(size_node = size_node_);
	}
	void addEdge(const Edge &e)
	{
		adjacency_list[e.u].push_back(e);
	}
	void rearrage()
	{
		for (int i = 0; i < size_node; i++)
		{
			sort(adjacency_list[i].begin(), adjacency_list[i].end(), [](Edge &a, Edge &b) { return a.v < b.v; });
		}
	}
	bool contain(const Edge &edge)
	{
		auto index = bisearch<Edge>(
			adjacency_list[edge.u].begin(), 
			adjacency_list[edge.u].end(), 
			edge,
			[](const Edge& a, const Edge& b) { return a.v - b.v; });
		//if (index == adjacency_list[edge.u].end()) return false;
		if (index == adjacency_list[edge.u].end() || *index != edge) 
			return false;
		else 
			return true;
	}
};
