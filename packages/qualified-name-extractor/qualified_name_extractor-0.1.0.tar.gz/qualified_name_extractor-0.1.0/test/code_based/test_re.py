#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/04
------------------------------------------
@Modify: 2020/11/04
------------------------------------------
@Description:
"""
import re
code = "code. code1 code2 code( code codes code[] code["
re_pattern = "%s[ [(.]" % "code"
for m in re.finditer(re_pattern, code):
    print(code[m.span()[0]:m.span()[1]])
    print(m.span())

# from pathlib import Path
#
# from sekg.graph.exporter.graph_data import GraphData
#
# from definitions import DATA_DIR

# graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
# api_graph: GraphData = GraphData.load(graph_path)
# a = api_graph.get_node_ids_by_label("primary type")
# print(api_graph.get_all_labels())
