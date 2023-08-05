#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qualified_name_extractor.code_based.base import BakerBaseClass


class CodeBasedWithGraphBaker(BakerBaseClass):
    """
    baker based on code recognize with graph
    """
    def __init__(self, graph, graph_client=None):
        super().__init__(graph=graph, graph_client=graph_client)

    def baker(self, code):
        class_recognitions, false_classes = self.extract_class_from_code(code)
        method_recognitions, class_object_pair = self.extract_method_from_code(code)
        # print("类：", class_recognitions)
        # print("方法：", method_recognitions)
        class_method_dic = {}
        for class_recognition in class_recognitions:
            class_method_dic[class_recognition] = []
        for method_recognition in method_recognitions:
            class_method_dic.setdefault(method_recognition.split('.')[0], []).append(method_recognition.split('.')[-1])
        # print("类及其方法：", class_method_dic)
        locate_class_method_dic = self.locate_api(code, class_method_dic)
        api_qualified_name = self.graph_based_linker(locate_class_method_dic, class_object_pair)
        return CodeBasedWithGraphBaker.format_api_qualified_name(api_qualified_name)

    @staticmethod
    def format_api_qualified_name(api_qualified_name):
        new_api_qualified_name = {
            "parse_code": "regulation",
            "api_num": 0
        }
        for key, item in api_qualified_name.items():
            simple_name = key.split("[")[0]
            pre_position_list = key.split("[")[1].split("]")[0].split("),")
            position_set = set()
            if item == 'java.security.MessageDigest.update':
                print(item)
            for pre_position in pre_position_list:
                position_tuple_item = (int(pre_position.split(",")[0].split("(")[1]), int(pre_position.split(",")[1].strip().split(")")[0]))
                position_set.add(position_tuple_item)
            if item not in new_api_qualified_name:
                new_api_qualified_name[item] = {
                    "qualified_name": item,
                    "name_in_code": simple_name,
                    "position": list(position_set)
                }
            else:
                position_set.update(set(new_api_qualified_name[item]["position"]))
                new_api_qualified_name[item]["position"] = list(position_set)
        new_api_qualified_name["api_num"] = len(new_api_qualified_name.keys()) - 2
        return new_api_qualified_name
