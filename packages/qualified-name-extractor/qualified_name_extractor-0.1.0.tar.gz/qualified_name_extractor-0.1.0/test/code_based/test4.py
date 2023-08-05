#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/11
------------------------------------------
@Modify: 2020/11/11
------------------------------------------
@Description:
"""
from pathlib import Path

from definitions import DATA_DIR
from qualified_name_extractor.code_based.ASTParseBasedWithGraphBaker import ASTParseBasedWithGraphBaker

code = """MessageDigest md = MessageDigest.getInstance(SHA);"""
graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
r = ASTParseBasedWithGraphBaker(graph=graph_path)
print(r.code_completion(code))
