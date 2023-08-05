#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/19
------------------------------------------
@Modify: 2020/11/19
------------------------------------------
@Description:
"""
from pathlib import Path

from definitions import DATA_DIR


code = """
public class DummyClass{
    public void dummyMethod(){
        MessageDigest md = MessageDigest.getInstance("SHA");
        try {
            byte toChapter1 = 1;
            md.update(toChapter1);
            MessageDigest tc1 = md.clone();
            byte[] toChapter1Digest = tc1.digest();
            md.update(toChapter1Digest);
        } catch (CloneNotSupportedException cnse) {
            throw new DigestException(couldn);
        }
    }
}
"""
graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
r = ASTParseBasedWithGraphBaker(graph=graph_path)

class_object_pair, class_method_dic = r.code_parser(code)
locate_class_method_dic = r.locate_class_api(code, class_method_dic)
result = r.new_graph_based_linker(locate_class_method_dic, code)
result = ASTParseBasedWithGraphBaker.format_api_qualified_name(result)
print(result)
