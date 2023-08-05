#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/03
------------------------------------------
@Modify: 2020/11/03
------------------------------------------
@Description:
"""
from pathlib import Path

import javalang

from definitions import DATA_DIR
from qualified_name_extractor.code_based.ASTParseBasedWithGraphBaker import ASTParseBasedWithGraphBaker
from qualified_name_extractor.code_based.base import BakerBaseClass

code = """
/**
 * 这段代码只在jdk6以下不报错，因为泛型是类型擦除规则来编译成字节码文件
 * @param age
 * @return
 */
public class DummyClass{

    // private String a = "1";
    private Integer test_step = 1;
    // private String b = "1";
    private Integer step = new Integer(100);
    /**
     * 这段代码只在jdk6以下不报错，因为泛型是类型擦除规则来编译成字节码文件
     * @param age
     * @return
     */
    boolean test2 = Boolean.valueOf(true);
    private Integer new_step = Integer.valueOf("100", 10);
    private Integer new_step_5 = Integer.valueOf("100");
    private Integer new_step_4 = Integer.valueOf(step);
    private Integer new_step_3 = Integer.valueOf(step.intValue());
    private Integer new_step_2 = Integer.valueOf(Integer.MIN_VALUE);
    private Integer new_step_1 = Integer.valueOf(Integer.toString(1));

    public void dummyMethod(){
        MessageDigest md = MessageDigest.getInstance("SHA");
        String methodName = Thread.currentThread().getStackTrace()[1].getMethodName();
        String[] countries = {"China", "United states"};
        Document document = new Document();
        document.createAttribute(new Date().toString());
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
# code = """
# public class DummyClass{
#     public void dummyMethod(){
#         MessageDigest md = MessageDigest.getInstance("SHA");
#         try {
#             byte toChapter1 = 1;
#             md.update(toChapter1);
#             MessageDigest tc1 = md.clone();
#             byte[] toChapter1Digest = tc1.digest();
#             md.update(toChapter1Digest);
#         } catch (CloneNotSupportedException cnse) {
#             throw new DigestException(couldn);
#         }
#     }
# }
# """

# code = """MessageDigest md = MessageDigest.getInstance("SHA");"""

graph_path = str(Path(DATA_DIR) / "graph" / "KG.V2.0.graph")
r = ASTParseBasedWithGraphBaker(graph=graph_path)

class_object_pair, class_method_dic = r.code_parser(code)
locate_class_method_dic = r.locate_class_api(code, class_method_dic)
result = r.new_graph_based_linker(locate_class_method_dic, code)
result = ASTParseBasedWithGraphBaker.format_api_qualified_name(result)
print(result)
# simple_name = r.point_name_2_simple_name('Thread.currentThread.getStackTrace')
# simple_name_1 = r.point_name_2_simple_name('Thread.currentThread')
# simple_name_2 = r.point_name_2_simple_name('Document.add')
# print(simple_name)
# tree = javalang.parse.parse(code)
# class_trees = tree.types
# for class_tree in class_trees:
#     for path, node in class_tree:
#         a = path
