"""Author: Jaewon Jang, Chrissy Teng, David Zhong"""
import math
import sys


class WeightedGraph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        for edge in self.adj[node1]:
            if edge[0] == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2, weight):
        if node1 not in self.adj[node2]:
            self.adj[node1].append((node2, weight))
            self.adj[node2].append((node1, weight))

    def w(self, node1, node2):
        for edge_info in self.adj[node1]:
            if node2 == edge_info[0]:
                return edge_info[1]

    def number_of_nodes(self):
        return len(self.adj)





class MinHeap:
    length = 0
    data = []

    def __init__(self, L):
        self.data = L
        self.length = len(L)
        self.map = {}
        for i in range(len(L)):
            self.map[L[i].value] = i
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.sink(i)

    def sink(self, i):
        smallest_known = i
        if self.left(i) < self.length and self.data[self.left(i)].key < self.data[i].key:
            smallest_known = self.left(i)
        if self.right(i) < self.length and self.data[self.right(i)].key < self.data[smallest_known].key:
            smallest_known = self.right(i)
        if smallest_known != i:
            self.data[i], self.data[smallest_known] = self.data[smallest_known], self.data[i]
            self.map[self.data[i].value] = i
            self.map[self.data[smallest_known].value] = smallest_known
            self.sink(smallest_known)

    def insert(self, element):
        if len(self.data) == self.length:
            self.data.append(element)
        else:
            self.data[self.length] = element
        self.map[element.value] = self.length
        self.length += 1
        self.swim(self.length - 1)

    def insert_elements(self, L):
        for element in L:
            self.insert(element)

    def swim(self, i):
        while i > 0 and self.data[i].key < self.data[self.parent(i)].key:
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]
            self.map[self.data[i].value] = i
            self.map[self.data[self.parent(i)].value] = self.parent(i)
            i = self.parent(i)

    def get_min(self):
        if len(self.data) > 0:
            return self.data[0]

    def extract_min(self):
        self.data[0], self.data[self.length - 1] = self.data[self.length - 1], self.data[0]
        self.map[self.data[self.length - 1].value] = self.length - 1
        self.map[self.data[0].value] = 0
        min_element = self.data[self.length - 1]
        self.length -= 1
        self.map.pop(min_element.value)
        self.sink(0)
        return min_element

    def decrease_key(self, value, new_key):
        if new_key >= self.data[self.map[value]].key:
            return
        index = self.map[value]
        self.data[index].key = new_key
        self.swim(index)

    def get_element_from_value(self, value):
        return self.data[self.map[value]]

    def get_key_from_value(self, value):
        return self.data[self.map[value]].key

    def is_empty(self):
        return self.length == 0

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.data[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s


class Element:

    def __init__(self, value, key):
        self.value = value
        self.key = key

    def __str__(self):
        return "(" + str(self.value) + "," + str(self.key) + ")"


L = []
L.append(Element("A", 6))
L.append(Element("B", 1))
L.append(Element("C", 2))
L.append(Element("D", 8))
L.append(Element("E", 0))

heap = MinHeap(L)


def prim(G):
    A = [0]
    min = 1000
    min_node = 0
    min_node2 = 0
    mst = WeightedGraph(G.number_of_nodes())

    while len(A) != G.number_of_nodes():
        for node in A:
            for adj_node in G.adj[node]:
                if adj_node[0] not in A:
                    if adj_node[1] < min:
                        min = adj_node[1]
                        min_node = adj_node[0]
                        min_node2 = node
        print(min)
        mst.add_edge(min_node2, min_node, min)
        A.append(min_node)
        min = 1000
    return mst


def prim2(G):
    mst = WeightedGraph(G.number_of_nodes())
    L = []
    nodes_added = []
    parents = {}
    for node in list(G.adj.keys()):
        L.append(Element(node,sys.maxsize))
    heap = MinHeap(L)#construct a heap
    while heap.length > 1 : #stop when the size of the heap is 1
        smallest_node = heap.extract_min().value
        nodes_added.append(smallest_node)
        for adjacent_edge in G.adjacent_nodes(smallest_node):
            node2 = adjacent_edge[0]
            new_weight = adjacent_edge[1]
            if node2 not in nodes_added:
                old_key = heap.get_key_from_value(node2)
                heap.decrease_key(node2,new_weight)
                new_key = heap.get_key_from_value(node2)
                if (new_key!= old_key):# check if its parent has changed
                    parents[adjacent_edge[0]] = smallest_node
        parent = parents[heap.get_min().value]
        new_node = heap.get_min().value
        weight = heap.get_min().key
        mst.add_edge(parent,new_node,weight)
    return mst




G = WeightedGraph(5)
G.add_edge(0, 1, 8)
G.add_edge(0, 2, 5)
G.add_edge(1, 2, 9)
G.add_edge(1, 3, 11)
G.add_edge(2, 3, 15)
G.add_edge(2, 4, 10)
G.add_edge(3, 4, 7)
print(prim2(G).adj)

"""
             "0" 
          //     \\
          8       5
        //         \\
       "1" -- 9 -- "2" 
        |        /  ||
       11     15    10
        |  /        ||
       "3" == 7 == "4"


Double lines represent the MST

"""

print(heap)
print(heap.get_min())
