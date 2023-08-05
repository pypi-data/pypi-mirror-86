#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/12
------------------------------------------
@Modify: 2020/11/12
------------------------------------------
@Description:
"""
from pathlib import Path

import networkx as nx
from sekg.graph.exporter.graph_data import GraphData, NodeInfo

from definitions import DATA_DIR

G = nx.DiGraph(nx.path_graph(4))
pr = nx.pagerank(G, alpha=0.9)
graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.1.graph")
graph_data: GraphData = GraphData.load(graph_path)
b = graph_data.get_node_info_dict(1000)
a = 1
