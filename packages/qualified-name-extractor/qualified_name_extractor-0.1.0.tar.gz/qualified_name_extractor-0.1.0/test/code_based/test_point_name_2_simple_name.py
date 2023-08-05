#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/18
------------------------------------------
@Modify: 2020/11/18
------------------------------------------
@Description:
"""
from pathlib import Path

from definitions import DATA_DIR
from qualified_name_extractor.code_based.ASTParseBasedWithGraphBaker import ASTParseBasedWithGraphBaker

graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
r = ASTParseBasedWithGraphBaker(graph=graph_path)
print(r.point_name_2_simple_name('Thread.currentThread'))
print(r.point_name_2_simple_name('Thread.currentThread.getStackTrace'))
print(r.point_name_2_simple_name('Thread.currentThread', True))
print(r.point_name_2_simple_name('Thread.currentThread.getStackTrace', True))
