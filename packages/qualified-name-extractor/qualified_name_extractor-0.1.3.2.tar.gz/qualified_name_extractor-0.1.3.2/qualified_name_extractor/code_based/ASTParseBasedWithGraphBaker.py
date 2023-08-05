#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qualified_name_extractor.code_based.base import BakerBaseClass


class ASTParseBasedWithGraphBaker(BakerBaseClass):
    """
    baker based on AST parse with graph
    """
    def __init__(self, graph, graph_client=None):
        super().__init__(graph=graph, graph_client=graph_client)

    def baker(self, code):
        api_qualified_name = {}
        valid_code = self.recognize_valid_code(code)
        if valid_code is not None:
            # valid_code = code
            code_blocks = self.recognize_code_block(valid_code)
            if len(code_blocks) > 0:
                for code_block in code_blocks:
                    if self.code_parser(code_block) is not None:
                        class_object_pair, class_method_dic = self.code_parser(code_block)
                        locate_class_method_dic = self.locate_class_api(code_block, class_method_dic)
                        api_qualified_name = self.new_graph_based_linker(locate_class_method_dic, code_block)
                    else:
                        return
            else:
                code_block = self.code_completion(valid_code)
                if self.code_parser(code_block) is not None:
                    class_object_pair, class_method_dic = self.code_parser(code_block)
                    locate_class_method_dic = self.locate_class_api(valid_code, class_method_dic)
                    api_qualified_name = self.new_graph_based_linker(locate_class_method_dic, valid_code)
                    prefix_dummy_code_index = code_block.find(valid_code)
                    for item in api_qualified_name:
                        if "position" not in item:
                            item["start_index"] = item["start_index"] - prefix_dummy_code_index
                            item["end_index"] = item["end_index"] - prefix_dummy_code_index
                else:
                    return
        else:
            print("invalid code")
            return
        return ASTParseBasedWithGraphBaker.format_api_qualified_name(api_qualified_name)

    @staticmethod
    def format_api_qualified_name(api_qualified_name):
        new_api_qualified_name = {
            "parse_code": "AST",
            "api_num": 0
        }
        for item in api_qualified_name:
            qualified_name = item["qualified_name"]
            position_set = set()
            if "position" in item:
                position_set.update(item["position"])
                name_in_code = item["name_in_code"]
            else:
                position_set.add((item["start_index"], item["end_index"]))
                name_in_code = item["simple_method_name"]
            if qualified_name not in new_api_qualified_name:
                new_api_qualified_name[qualified_name] = {
                    "qualified_name": qualified_name,
                    "name_in_code": name_in_code,
                    "position": list(position_set),
                    "code": item["code"]
                }
            else:
                position_set.update(set(new_api_qualified_name[qualified_name]["position"]))
                new_api_qualified_name[qualified_name]["position"] = list(position_set)
        new_api_qualified_name["api_num"] = len(new_api_qualified_name.keys()) - 2
        return new_api_qualified_name
