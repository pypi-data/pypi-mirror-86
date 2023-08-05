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
from sekg.graph.exporter.graph_data import GraphData
from tqdm import tqdm

from definitions import DATA_DIR


def add_page_rank_score_2_graph(input_graph_path, output_graph_path):
    graph_data: GraphData = GraphData.load(input_graph_path)
    nx_graph = nx.Graph(graph_data.graph)
    pr = nx.pagerank(nx_graph)
    for key, item in tqdm(pr.items()):
        node_info = graph_data.get_node_info_dict(key)
        node_info["properties"]["page_rank_score"] = item
    graph_data.save(output_graph_path)
    print("graph保存完毕")


if __name__ == "__main__":
    graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
    out_graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.1.graph")
    add_page_rank_score_2_graph(graph_path, out_graph_path)
