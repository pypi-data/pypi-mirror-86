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
from qualified_name_extractor.code_based.ASTParseCodeBasedWithGraphBaker import ASTParseCodeBasedWithGraphBaker


class TestASTParseCodeBasedWithGraphBaker(TestCase):

    def test_baker(self):
        graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
        r = ASTParseCodeBasedWithGraphBaker(graph=graph_path)
        code = r"""
            public class DummyClass{
            
                private Integer test_step = 1;
                private Integer step = new Integer(100);
                private Integer new_step = Integer.valueOf(10);
            
                public void dummyMethod(){
                    MessageDigest md = MessageDigest.getInstance(SHA);
                    String methodName = Thread.currentThread().getStackTrace()[1].getMethodName();
                    String[] countries = {"China", "United states"};
                    Document document = new Document();
                    document.add(new Paragraph(new Date().toString()));
                    try {
                        md.update(toChapter1);
                        MessageDigest tc1 = md.clone();
                        byte[] toChapter1Digest = tc1.digest();
                        md.update(toChapter2);
                    } catch (CloneNotSupportedException cnse) {
                        throw new DigestException(couldn);
                    }
                }
            }
            """
        result = r.baker(code)
        print(result)
