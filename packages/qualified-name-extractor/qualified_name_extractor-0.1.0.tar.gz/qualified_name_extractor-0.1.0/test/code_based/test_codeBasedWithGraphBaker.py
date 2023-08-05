#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: zhaocy
@Email: 19110240027@fudan.edu.cn
@Created: 2020/2/16
------------------------------------------
@Modify: 2020/2/16
------------------------------------------
@Description: 
"""
from pathlib import Path
from unittest import TestCase
from definitions import DATA_DIR
from qualified_name_extractor.code_based.CodeBasedWithGraphBaker import CodeBasedWithGraphBaker


class TestCodeBasedWithGraphBaker(TestCase):

    def test_baker(self):
        graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
        r = CodeBasedWithGraphBaker(graph=graph_path)
        code = r"""MessageDigest md = MessageDigest.getInstance("SHA-256");
                     try {
                         md.update(toChapter1);
                         MessageDigest tc1 = md.clone();
                         byte[] toChapter1Digest = tc1.digest();
                         md.update(toChapter2);
                     } catch (CloneNotSupportedException cnse) {
                         throw new DigestException("couldn't make digest of partial content");
                     }"""
        r.baker(code)
