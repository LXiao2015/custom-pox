# -*- coding: utf-8 -*-

hostNum= 27
switchNum = 13
nfNum = 5
pri = 2

def _init():
    global graph
    graph = {i: {} for i in range(hostNum + switchNum + nfNum + 1)}


def set_links(m, n, port):
    graph[m][n] = port


def get_port(m, n, default=-1):
    try:
	return graph[m][n]
    except KeyError:
	return default


def get_pri():
    global pri
    pri = pri + 1
    return pri


def del_node(node):
    del graph[node]


def print_links():
    print(graph)
