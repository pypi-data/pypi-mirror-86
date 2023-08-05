#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: lvgang
@Email: 1547554745@qq.com
@Created: 2020/10/22
------------------------------------------
@Modify: 2020/10/22
------------------------------------------
@Description:
"""
from pathlib import Path

from definitions import DATA_DIR
from qualified_name_extractor.code_based.ASTParseBasedWithGraphBaker import ASTParseBasedWithGraphBaker

graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
r = ASTParseBasedWithGraphBaker(graph=graph_path)
code = r"""MessageDigest md = MessageDigest.getInstance("SHA-256");
             try {
                 md.update(toChapter1);
                 MessageDigest tc1 = md.clone();
                 byte[] toChapter1Digest = tc1.digest();
                 md.update(toChapter2);
             } catch (CloneNotSupportedException cnse) {
                 throw new DigestException("couldn't make digest of partial content");
             }"""
api_dict = r.baker(code)
print(api_dict)
