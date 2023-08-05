#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from abc import abstractmethod
import re
import javalang
import javalang.tree as Tree
from javalang.tokenizer import Position
from nltk import word_tokenize
from sekg.graph.exporter.graph_data import GraphData
from sekg.util.code import CodeElementNameUtil
from qualified_name_extractor.code_based.BakerGraphAccessor import BakerGraphAccessor


class BakerBaseClass:

    BYTE_TYPE = ["byte", "java.lang.Byte"]
    BOOLEAN_TYPE = ["boolean", "java.lang.Boolean"]
    INT_NUM_TYPE = ["short", "int", "long", "java.lang.Short", "java.lang.Integer", "java.lang.Long"]
    FLOAT_NUM_TYPE = ["float", "java.lang.Float"]
    DOUBLE_NUM_TYPE = ["double", "java.lang.Double"]
    CHAR_TYPE = ["char", "java.lang.Character"]
    STRING_TYPE = ["string", "java.lang.String"]
    OBJECT_TYPE = ["java.lang.Object"]

    PRIMARY_TYPE_DICT = {
        "byte": BYTE_TYPE,
        "boolean": BOOLEAN_TYPE,
        "short": INT_NUM_TYPE,
        "int": INT_NUM_TYPE,
        "long": INT_NUM_TYPE,
        "float": FLOAT_NUM_TYPE,
        "double": DOUBLE_NUM_TYPE,
        "char": CHAR_TYPE,
        "string": STRING_TYPE,
    }

    def __init__(self, graph, graph_client):
        self.graph_accessor = BakerGraphAccessor(graph_client)
        self.qualified_name_set = set()
        self.long_name_dic = {}
        self.short_name_dic = {}
        self.api_graph = None
        if isinstance(graph, str):
            self.init_from_graph_data(graph)
        elif isinstance(graph, GraphData):
            self.api_graph = graph
            self.init_api_table()
        self.CODE_NAME_UTIL = CodeElementNameUtil()
        self.code_patterns = [
            re.compile(r'^(?P<ELE>[a-zA-Z0-9_]*[a-z0-9][A-Z][a-z]+[a-zA-Z0-9_]*)(<.*>)?$'),
            re.compile(r'^(?P<ELE>[a-zA-Z0-9_\.<>]+)\)[a-zA-Z0-9_\,.<>)]*?$'),
            re.compile(r'^(?P<ELE>[a-zA-Z]{2,}(\.[a-zA-Z0-9_]+)+)(<.*>)?$'),
            re.compile(r'^(?P<ELE>((([a-zA-Z0-9_]+)(\.))+)([a-zA-Z0-9_]+))?$'),
            re.compile(r'^(?P<ELE>[a-zA-Z0-9_]+(\([a-zA-Z0-9_]*\))?\.)+[a-zA-Z0-9_]+(\([a-zA-Z0-9_]*\))$')
        ]
        self.data_type = {'boolean', 'byte', 'char', 'short', 'int', 'long', 'float', 'double', 'Boolean', 'Byte',
                          'Character', 'Short', 'Integer', 'Long', 'Float', 'Double', 'void', 'enum'}

    def init_from_graph_data(self, graph_path):
        self.api_graph: GraphData = GraphData.load(graph_path)
        self.init_api_table()

    def init_api_table(self,):
        api_node_ids = self.api_graph.get_node_ids_by_label("class")
        api_node_ids.update(self.api_graph.get_node_ids_by_label("method"))
        api_node_ids.update(self.api_graph.get_node_ids_by_label("interface"))
        api_node_ids.update(self.api_graph.get_node_ids_by_label("primary type"))
        for node_id in api_node_ids:
            api_node = self.api_graph.get_node_info_dict(node_id)
            qualified_name = api_node["properties"]["qualified_name"]
            long_name, short_name, parameter_list = self.process_api(qualified_name)
            self.qualified_name_set.add(qualified_name)
            if long_name not in self.long_name_dic.keys():
                self.long_name_dic[long_name] = {qualified_name}
            else:
                self.long_name_dic[long_name].add(qualified_name)
            if short_name not in self.short_name_dic.keys():
                self.short_name_dic[short_name] = {qualified_name}
            else:
                self.short_name_dic[short_name].add(qualified_name)

    @abstractmethod
    def baker(self, code):
        return set()

    def extract_code_element(self, sent):
        elements = set()
        raw_words = word_tokenize(sent)
        words = []
        for raw_word in raw_words:
            words.append(raw_word.strip())
        # 去除words中的空格
        words = list(filter(lambda x: x != '', words))
        for word in words:
            flag = False
            for index, pattern in enumerate(self.code_patterns):
                search_rs = pattern.search(word)
                if search_rs is not None and search_rs.group("ELE"):
                    elements.add(search_rs.group("ELE"))
                    flag = True
                # 若是不符合上述任何一种pattern,则考虑当前分词中是否存在驼峰式
                elif index == len(self.code_patterns) - 1 and not flag:
                    p = re.compile(r'(([a-z_]+([A-Z])[a-z_]+)+)|(([A-Z_]([a-z_]+))+)')
                    search_rs = p.match(word)
                    if search_rs is not None:
                        elements.add(search_rs.group(0))
        return elements, words

    def extract_class_from_code(self, sent):
        candidate_classes = set()
        code_elements, words = self.extract_code_element(sent)
        pattern_qualified_name = re.compile(r'(java.)|(javax.)|(org.)')
        pattern_simple_name = re.compile(r'([A-Z])')
        for code_element in code_elements:
            match_qualified_name = pattern_qualified_name.match(code_element)
            match_simple_name = pattern_simple_name.match(code_element)
            if match_qualified_name is not None:
                candidate_classes.add(code_element)
            if match_simple_name is not None:
                candidate_classes.add(code_element.split('.')[0])
        false_classes = set()
        for index, word in enumerate(words):
            if index == len(words) - 1:
                break
            if word == "class" or word == "@":
                false_classes.add(words[index + 1])
        for candidate_class in candidate_classes.copy():
            for false_class in false_classes:
                if candidate_class.startswith(false_class):
                    if candidate_class not in candidate_classes:
                        continue
                    candidate_classes.remove(candidate_class)
        return candidate_classes, false_classes

    def extract_method_from_code(self, sent):
        candidate_methods = set()
        code_methods = set()
        methods = set()
        class_object_pair = {}
        code_elements, words = self.extract_code_element(sent)
        code_classes, false_classes = self.extract_class_from_code(sent)
        p = re.compile(r'([a-z]+[a-zA-Z0-9_]*)')
        for code_element in code_elements:
            match_rs = p.match(code_element)
            if match_rs is not None:
                candidate_methods.add(code_element)
            for code_class in code_classes:
                if code_element.startswith(code_class + '.'):
                    candidate_methods.add(code_element)
        for code_class in code_classes.copy():
            code_classes.add(self.CODE_NAME_UTIL.simplify(code_class))
        false_method = set()
        false_mothod_from_false_classes = set()
        p2 = re.compile(r'([a-zA-Z0-9_]+)')
        for index, word in enumerate(words[:-1]):
            if word in false_classes:
                false_mothod_from_false_classes.add(words[index + 1])
                false_method.add(words[index + 1])
            elif word in code_classes | self.data_type:
                false_method.add(words[index + 1])
                if p2.match(words[index + 1]) is not None:
                    class_object_pair.setdefault(word, []).append(words[index + 1])
        # print("类和对象配对：", class_object_pair)
        for candidate_method in candidate_methods - false_method - code_classes:
            if candidate_method.split('.')[0] not in false_mothod_from_false_classes and \
                    candidate_method.split('.')[-1][0].islower() and candidate_method.__contains__('.'):
                code_methods.add(candidate_method)
        for code_method in code_methods.copy():
            class_name = code_method.split('.')[0]
            if class_name in class_object_pair.keys():
                methods.add(code_method)
            else:
                for class_object_pair_value in class_object_pair.values():
                    if class_name in class_object_pair_value:
                        methods.add(str(list(class_object_pair.keys())[
                            list(class_object_pair.values()).index(
                                class_object_pair_value)]) + '.' + str(code_method.split('.', 1)[1]))
        return methods, class_object_pair

    def recognize_valid_code(self, code):
        """
        去除code中的注释
        :param code: 原始代码片段
        :return: 修改后的合法代码片段
        """
        self.pattern_line = "\/\/[^\n]*"
        self.pattern_block = "\/\*(\s|.)*?\*\/"
        self.pattern_code = re.compile("[a-zA-Z0-9_ ]")
        self.pattern_method = re.compile("\([^()]+\)")
        self.pattern_parameter = re.compile('([a-zA-Z0-9_ ]+)([^a-zA-Z0-9_ ])')
        try:
            # 单行注释删除
            code = re.sub(self.pattern_line, '', code, flags=re.I)
            # 多行注释删除
            code = re.sub(self.pattern_block, '', code, flags=re.M)
            # 删除多余空白行
            code = re.sub("\n[\s]*\n", '\n', code, flags=re.I)
        except Exception as e:
            print(str(e))
        code_lines = code.split('\n')
        # 去除code_lines中的空格和import语句
        code_lines = list(filter(lambda x: x != '' and not x.isspace() and not x.startswith('import'), code_lines))
        for code_line in code_lines:
            if code_line.__contains__('...'):
                return
            elif code_line.strip()[-1] not in ['{', '}', ')', ';'] and code_line.strip()[0] not in ['@']:
                return
            elif code_line.strip()[-1] in ['{', '}', ')', ';'] and not self.pattern_code.match(code_line) and not code_line.strip()[0] in ['{', '}', ')', ';']:
                return
        for index, code_line in enumerate(code_lines.copy()):
            if not code_line.startswith('if') and code_line.endswith(')'):
                code_lines[index] = code_lines[index] + ';'
            results = self.pattern_method.findall(code_line)
            if len(results) > 0:
                for i, result in enumerate(results.copy()):
                    parameters = result.lstrip('(').rstrip(')').split(',')
                    for j, parameter in enumerate(parameters.copy()):
                        if self.pattern_parameter.search(parameter) is not None:
                            parameters[j] = self.pattern_parameter.search(parameter).group(1)
                        else:
                            parameters[j] = parameter
                    results[i] = ','.join(parameters)
                    results[i] = '(' + results[i] + ')'
                    code_lines[index] = code_lines[index].replace(result, results[i])
        code = '\n'.join(code_lines)
        return code

    def recognize_code_block(self, code):
        code_blocks = []
        code_lines = code.split('\n')
        line_index = 0
        while line_index < len(code_lines):
            if code_lines[line_index].__contains__('class ' or 'interface '):
                start_index = line_index
                brackets = []
                if code_lines[line_index].__contains__('{' and '}'):
                    code_blocks.append(code_lines[line_index])
                    line_index = line_index + 1
                    continue
                if code_lines[line_index].__contains__('{'):
                    brackets.append("{")
                line_index = line_index + 1
                if line_index >= len(code_lines):
                    break
                code = ''
                while True:
                    if code_lines[line_index].__contains__('{'):
                        brackets.append('{')
                    if code_lines[line_index].__contains__('}'):
                        brackets.pop()
                    end_index = line_index + 1
                    line_index = line_index + 1
                    if len(brackets) <= 0:
                        break
                    if line_index >= len(code_lines):
                        break
                for code_index in range(start_index, end_index):
                    code = code + code_lines[code_index] + '\n'
                if len(brackets) > 0:
                    code += "}" * len(brackets)
                code_blocks.append(code)
            line_index = line_index + 1
        return code_blocks

    @staticmethod
    def recognize_method_or_field_signature(code):
        method_signature_patterns = [
            re.compile(
                r'(public |private |protected |)(void |abstract |static |final |native |synchronized )?(?!=throw |throws |new )[a-zA-Z_][a-zA-Z0-9_ ]*(\([a-zA-Z0-9_, ]*\))', re.I | re.S),
            re.compile(r'(public |private |protected )[^\n]+;', re.I | re.S)
        ]
        code_lines = code.split('\n')
        for code_line in code_lines:
            for index, pattern in enumerate(method_signature_patterns):
                search_rs = pattern.match(code_line.strip())
                if search_rs is not None:
                    if code_line[-1] in [";"] and index in [0]:
                        continue
                    return True
        return False

    def code_completion(self, code):
        if self.recognize_method_or_field_signature(code):
            return "public class DummyClass{\n" + code + "\n }"
        else:
            return "public class DummyClass{\n" + " public void dummyMethod(){\n" + code + " }\n" + "}"

    @staticmethod
    def AST_position_2_index(position: Position, api_name, code):
        start_index = 0
        if position.line > 1:
            split_code_list = code.split("\n")
            for i in range(position.line - 1):
                start_index += len(split_code_list[i]) + len("\n")
            start_index += position.column
        else:
            start_index = position.column
        if api_name != code[start_index:start_index + len(api_name)]:
            start_index = code.find(api_name, start_index)
        return start_index, start_index + len(api_name)

    def code_parser(self, code):
        class_object_pair = {}
        class_method_dic = {}
        class_extends_implements = ''
        try:
            tree = javalang.parse.parse(code)
            class_trees = tree.types
            for class_tree in class_trees:
                for path, node in class_tree:
                    if isinstance(node, Tree.ClassDeclaration):
                        if node.extends is not None:
                            class_extends_implements = node.extends.name
                            class_method_dic.setdefault(class_extends_implements, [])
                        elif node.implements is not None:
                            class_extends_implements = node.implements.name
                            class_method_dic.setdefault(class_extends_implements, [])
                    elif isinstance(node, Tree.MethodDeclaration):
                        if node.annotations is not None:
                            for annotation in node.annotations:
                                if annotation.name == 'Override':
                                    start_index, end_index = BakerBaseClass.AST_position_2_index(node.position,
                                                                                                 node.name, code)
                                    class_method_dic.setdefault(class_extends_implements, []).append({
                                        "simple_method_name": node.name,
                                        "parameters_num": len(node.parameters),
                                        "start_index": start_index,
                                        "end_index": end_index,
                                        "parameters_type": [BakerBaseClass.OBJECT_TYPE] * len(node.parameters)
                                    })
                    elif isinstance(node, Tree.SuperMethodInvocation):
                        class_method_dic.setdefault(class_extends_implements, []).append(self.arrange_arguments_for_method(node, code, class_object_pair, class_method_dic))
                    elif isinstance(node, Tree.ClassCreator):
                        class_method_dic.setdefault(node.type.name, [])
                        if node.selectors is not None and len(node.selectors) > 0:
                            parent_node = node.type.name
                            for selector in node.selectors:
                                if isinstance(selector, Tree.MethodInvocation):
                                    class_method_dic.setdefault(parent_node, []).append(self.arrange_arguments_for_method(selector, code, class_object_pair, class_method_dic))
                                    parent_node += "." + selector.member
                    elif isinstance(node, Tree.LocalVariableDeclaration) or isinstance(node, Tree.FieldDeclaration):
                        for declarator in node.declarators:
                            node_type_name = node.type.name
                            if 'dimensions' in node.type.attrs and isinstance(node.type.dimensions, list):
                                node_type_name += "[]" * len(node.type.dimensions)
                            class_object_pair.setdefault(node_type_name, []).append(declarator.name)
                        class_method_dic.setdefault(node.type.name, [])
                    elif isinstance(node, Tree.ReferenceType):
                        if node.name not in class_method_dic.keys():
                            class_method_dic[node.name] = []
                    elif isinstance(node, Tree.MethodInvocation) and node.qualifier is not None:
                        if len(class_object_pair) > 0:
                            append_flag = False
                            for key, class_object_pair_value in class_object_pair.items():
                                if node.qualifier in class_object_pair_value:
                                    class_method_dic.setdefault(key.split("[")[0], []).append(self.arrange_arguments_for_method(node, code, class_object_pair, class_method_dic))
                                    append_flag = True
                            if not append_flag:
                                class_method_dic.setdefault(node.qualifier, []).append(self.arrange_arguments_for_method(node, code, class_object_pair, class_method_dic))
                        else:
                            class_method_dic.setdefault(node.qualifier, []).append(self.arrange_arguments_for_method(node, code, class_object_pair, class_method_dic))
                        # 处理Thread.currentThread().getStackTrace()[1].getMethodName()
                        if node.selectors is not None and len(node.selectors) > 0:
                            parent_class_name = node.qualifier
                            if parent_class_name not in class_method_dic:
                                for key, class_object_pair_value in class_object_pair.items():
                                    if node.qualifier in class_object_pair_value:
                                        parent_class_name = key.split("[")[0]
                            parent_node = parent_class_name + '.' + node.member
                            for selector in node.selectors:
                                if isinstance(selector, Tree.MethodInvocation):
                                    class_method_dic.setdefault(parent_node, []).append(self.arrange_arguments_for_method(selector, code, class_object_pair, class_method_dic))
                                    parent_node += "." + selector.member
            # print("类和对象配对:", class_object_pair)
            # print("javalang解析:", class_method_dic)
        except Exception as e:
            print('the code can not be parsed')
            return
        return class_object_pair, class_method_dic

    def arrange_arguments_for_method(self, node, code, class_object_pair, class_method_dic):
        start_index, end_index = BakerBaseClass.AST_position_2_index(node.position, node.member, code)
        method_dic = {
            "simple_method_name": node.member,
            "parameters_num": len(node.arguments),
            "start_index": start_index,
            "end_index": end_index,
            "parameters_type": []
        }
        # 参数类型设置为java.lang.Object就是这个参数类型暂时随意
        # Literal, MemberReference, MethodInvocation, ClassCreator（字面量、成员变量、局部变量、类变量-类静态变量、函数调用、先new对象再函数调用）
        for argument in node.arguments:
            if isinstance(argument, Tree.Literal):
                if "'" in argument.value:
                    method_dic["parameters_type"].append(BakerBaseClass.CHAR_TYPE)
                elif '"' in argument.value:
                    method_dic["parameters_type"].append(BakerBaseClass.STRING_TYPE)
                elif argument.value in ["true", "false"]:
                    method_dic["parameters_type"].append(BakerBaseClass.BOOLEAN_TYPE)
                elif argument.value.isdigit():
                    method_dic["parameters_type"].append(BakerBaseClass.INT_NUM_TYPE)
                elif BakerBaseClass.is_float(argument.value):
                    method_dic["parameters_type"].append(BakerBaseClass.FLOAT_NUM_TYPE)
                elif BakerBaseClass.is_double(argument.value):
                    method_dic["parameters_type"].append(BakerBaseClass.DOUBLE_NUM_TYPE)
                else:
                    method_dic["parameters_type"].append(BakerBaseClass.OBJECT_TYPE)
            elif isinstance(argument, Tree.MemberReference):
                member_name = argument.member
                argument_type_append_flag = False
                for key, class_object_pair_value in class_object_pair.items():
                    if member_name in class_object_pair_value:
                        # 一个是判断全限定名的parameter类型在判断片段代码的parameter type list中，一个是判断片段代码的parameter type string在全限定名的parameter类型中
                        if key in BakerBaseClass.PRIMARY_TYPE_DICT:
                            method_dic["parameters_type"].append(BakerBaseClass.PRIMARY_TYPE_DICT[key])
                        else:
                            method_dic["parameters_type"].append(key)
                        argument_type_append_flag = True
                        break
                if not argument_type_append_flag:
                    if argument.qualifier is not None and argument.qualifier != "":
                        method_dic["parameters_type"].append(argument.qualifier)
                    else:
                        method_dic["parameters_type"].append(BakerBaseClass.OBJECT_TYPE)
            elif isinstance(argument, Tree.MethodInvocation):
                class_point_method_name = argument.qualifier
                if class_point_method_name not in class_method_dic:
                    for key, class_object_pair_value in class_object_pair.items():
                        if argument.qualifier in class_object_pair_value:
                            class_point_method_name = key.split("[")[0]
                class_point_method_name = class_point_method_name + '.' + argument.member
                for selector in argument.selectors:
                    if isinstance(selector, Tree.MethodInvocation):
                        class_point_method_name += "." + selector.member
                class_qualified_name = self.point_name_2_simple_name(class_point_method_name, True)
                if class_qualified_name != "":
                    if class_qualified_name in self.PRIMARY_TYPE_DICT:
                        method_dic["parameters_type"].append(self.PRIMARY_TYPE_DICT[class_qualified_name])
                    else:
                        method_dic["parameters_type"].append(class_qualified_name)
                else:
                    method_dic["parameters_type"].append(self.OBJECT_TYPE)
            elif isinstance(argument, Tree.ClassCreator):
                class_point_method_name = argument.type.name
                for selector in argument.selectors:
                    if isinstance(selector, Tree.MethodInvocation):
                        class_point_method_name += "." + selector.member
                class_qualified_name = self.point_name_2_simple_name(class_point_method_name, True)
                if class_qualified_name != "":
                    if class_qualified_name in self.PRIMARY_TYPE_DICT:
                        method_dic["parameters_type"].append(self.PRIMARY_TYPE_DICT[class_qualified_name])
                    else:
                        method_dic["parameters_type"].append(class_qualified_name)
                else:
                    method_dic["parameters_type"].append(self.OBJECT_TYPE)
            else:
                method_dic["parameters_type"].append(self.OBJECT_TYPE)
        return method_dic

    @staticmethod
    def is_float(num):
        pattern = re.compile(r'^[-+]?\d*\.?\d*f$')
        result = pattern.match(num)
        if result:
            return True
        else:
            return False

    @staticmethod
    def is_double(num):
        pattern = re.compile(r'^[-+]?\d*\.?\d*[^f]$')
        result = pattern.match(num)
        if result:
            return True
        else:
            return False

    @staticmethod
    def locate_class_api(code, class_method_dic):
        new_class_method_dic = {}
        for class_name in class_method_dic.keys():
            re_pattern = "%s[ [(.]" % class_name
            position_set = {(m.span()[0], m.span()[1] - 1) for m in re.finditer(re_pattern, code)}
            new_class_method_dic[class_name] = {
                "position": position_set,
                "simple_name": class_name,
                "method_info": class_method_dic[class_name]
            }
        return new_class_method_dic

    def locate_api(self, code, class_method_dic):
        locate_class_method_dic = {}
        for key in class_method_dic.keys():
            tmp_method = []
            new_key = key + str([m.span() for m in re.finditer(key, code)])
            locate_class_method_dic.setdefault(new_key, [])
            for value in class_method_dic[key]:
                if value not in tmp_method:
                    indexes = [m.span() for m in re.finditer(value, code)]
                    if len(indexes) > 1:
                        tmp_method.append(value)
                        for index in indexes:
                            new_value = str(value) + '[' + str(index) + ']'
                            locate_class_method_dic.setdefault(new_key, []).append(new_value)
                    else:
                        locate_class_method_dic.setdefault(new_key, []).append(str(value) + str(indexes))
        # print("locate信息: ", locate_class_method_dic)
        return locate_class_method_dic

    def neo4j_based_linker(self, locate_class_method_dic, class_object_pair):
        api_qualified_name = {}
        locate_class_apis = locate_class_method_dic.keys()
        for locate_class_api in locate_class_apis:
            class_api = locate_class_api.split('[')[0]
            if not class_api.__contains__('.'):
                locate_method_apis = locate_class_method_dic[locate_class_api]
                simple_methods = []
                for locate_method_api in locate_method_apis:
                    method_api = locate_method_api.split('[')[0]
                    simple_methods.append(self.CODE_NAME_UTIL.simplify(method_api))
                # qualified name完全匹配--严格匹配
                if self.graph_accessor.find_node(primary_label="entity", primary_property="qualified_name", primary_property_value=class_api):
                    api_qualified_name[locate_class_api] = class_api
                    for index, locate_method_api in enumerate(locate_method_apis):
                        api_qualified_name[locate_method_api] = class_api + '.' + locate_method_api.split('[')[0]
                    continue
                candidate_classes = set()
                short_name_node = self.graph_accessor.find_node(primary_label="entity", primary_property="short_name",
                                                                primary_property_value=class_api)
                if short_name_node is not None:
                    candidate_classes.add(short_name_node["qualified_name"])
                long_name_node = self.graph_accessor.find_node(primary_label="entity", primary_property="long_name",
                                                               primary_property_value=class_api)
                if long_name_node is not None:
                    candidate_classes.add(long_name_node["qualified_name"])
                tmp_api_qualified_name = dict()
                for candidate_class in candidate_classes:
                    qualified_name_node = self.graph_accessor.find_node(primary_label="entity", primary_property="qualified_name", primary_property_value=candidate_class)
                    if qualified_name_node is not None:
                        graph_id = qualified_name_node.identity
                        in_relations_tuples = self.graph_accessor.get_all_in_relations(graph_id)
                        all_methods = []
                        for in_relations_tuple in in_relations_tuples:
                            if in_relations_tuple[1] == 'belong to':
                                all_methods.append(in_relations_tuple[2])
                        all_simple_methods = []
                        for all_method in all_methods:
                            all_simple_methods.append(self.CODE_NAME_UTIL.simplify(all_method))
                        if set(simple_methods) < set(all_simple_methods):
                            tmp_api_qualified_name.setdefault(candidate_class, [])
                            for simple_method in simple_methods:
                                tmp_api_qualified_name.setdefault(candidate_class, []).append(
                                    candidate_class + '.' + simple_method)
                if len(tmp_api_qualified_name) == 1:
                    class_qualified_name = list(tmp_api_qualified_name.keys())[0]
                    method_qualified_name = tmp_api_qualified_name[class_qualified_name]
                    api_qualified_name[locate_class_api] = class_qualified_name
                    for index, locate_method_api in enumerate(locate_method_apis):
                        api_qualified_name[locate_method_api] = method_qualified_name[index]
            else:
                object_name = class_api.split('.')[0]
                class_name = ''
                qualified_names = set()
                for key in class_object_pair.keys():
                    if object_name in class_object_pair[key]:
                        class_name = key
                for key in api_qualified_name.keys():
                    if key.__contains__(class_name):
                        return_value_type_name = api_qualified_name[key] + '.' + class_api.split('.')[1]
                        short_name_node = self.graph_accessor.find_node(primary_label="entity",
                                                                        primary_property="short_name",
                                                                        primary_property_value=return_value_type_name)
                        if short_name_node is not None:
                            qualified_names = short_name_node["qualified_name"]
                        long_name_node = self.graph_accessor.find_node(primary_label="entity",
                                                                       primary_property="long_name",
                                                                       primary_property_value=return_value_type_name)
                        if long_name_node is not None:
                            qualified_names = long_name_node["qualified_name"]
                        first_flag = False
                        for qualified_name in qualified_names:
                            api_node = self.graph_accessor.find_node(primary_label="entity", primary_property="qualified_name", primary_property_value=qualified_name)
                            if api_node is not None:
                                graph_id = api_node.identity
                                out_relations_tuples = self.graph_accessor.get_all_out_relations(graph_id)
                                for out_relations_tuple in out_relations_tuples:
                                    if out_relations_tuple[1] == 'return value type' or out_relations_tuple[1] == 'has return value':
                                        first_flag = True
                                        return_value_type = out_relations_tuple[2]
                                        for method_name in locate_class_method_dic[locate_class_api]:
                                            api_qualified_name[method_name] = str(return_value_type) + '.' + str(method_name.split('[')[0])
                                        break
                                if first_flag:
                                    break
                        break
        # print("baker链接: ", api_qualified_name)
        return api_qualified_name

    def link_method_by_qualified_class(self, method_info_list, class_node_id, code):
        candidate_method_method_list = []
        out_relation = self.api_graph.get_all_out_relations(class_node_id)
        for start_id, relation, end_id in out_relation:
            if relation == "has method":
                method_node = self.api_graph.get_node_info_dict(end_id)
                method_qualified_name = method_node["properties"]["qualified_name"]
                method_simple_name = method_qualified_name.split("(")[0].split(".")[-1].strip()
                parameter_num = 0
                parameter_list = []
                if method_qualified_name.split("(")[1].split(")")[0].strip() != "":
                    parameter_list = method_qualified_name.split("(")[1].split(")")[0].split(",")
                    parameter_num = len(parameter_list)
                for method_info in method_info_list:
                    if "qualified_name" not in method_info:
                        if method_simple_name.lower() == method_info["simple_method_name"].lower() and parameter_num == method_info["parameters_num"]:
                            match_label = True
                            for i in range(parameter_num):
                                if isinstance(method_info["parameters_type"][i], list):
                                    if method_info["parameters_type"][i] == self.OBJECT_TYPE:
                                        pass
                                    elif parameter_list[i] not in method_info["parameters_type"][i]:
                                        match_label = False
                                        break
                                else:
                                    if '[]' in method_info["parameters_type"][i] and method_info["parameters_type"][i].lower() not in parameter_list[i].lower():
                                        match_label = False
                                        break
                                    if method_info["parameters_type"][i].lower() not in parameter_list[i].lower() and parameter_list[i].lower() not in method_info["parameters_type"][i].lower():
                                        match_label = False
                                        break
                            if match_label:
                                method_info["qualified_name"] = method_qualified_name
                                method_info["code"] = code
                                candidate_method_method_list.append(method_info)
        return candidate_method_method_list

    @staticmethod
    def arrange_method_info_list(locate_class_method_dic):
        class_method_list = []
        for class_name in locate_class_method_dic.keys():
            if "." not in class_name:
                class_method_list.append(locate_class_method_dic[class_name])
                class_method_list.extend(locate_class_method_dic[class_name]["method_info"])
            else:
                class_method_list.extend(locate_class_method_dic[class_name]["method_info"])
        return class_method_list

    def new_graph_based_linker(self, locate_class_method_dic, code):
        api_qualified_name = []
        new_class_method_dic = self.arrange_simple_name(locate_class_method_dic)
        # 测试结果用
        # api_test_name = BakerBaseClass.arrange_method_info_list(new_class_method_dic)
        for original_class_name in new_class_method_dic.keys():
            if "." not in original_class_name:
                class_name = original_class_name
            else:
                class_name = new_class_method_dic[original_class_name]["return_value_class"]
            if class_name in self.short_name_dic:
                candidate_class_qualified_name = ""
                qualified_method_list = []
                for qualified_class_name in self.short_name_dic[class_name]:
                    class_info = self.api_graph.find_one_node_by_property("qualified_name", qualified_class_name)
                    if "class" in class_info["labels"] or "interface" in class_info["labels"] or "primary type" in class_info["labels"]:
                        if candidate_class_qualified_name == "":
                            candidate_class_qualified_name = qualified_class_name
                        class_id = class_info["id"]
                        candidate_method_list = self.link_method_by_qualified_class(copy.deepcopy(new_class_method_dic[original_class_name]["method_info"]), class_id, code)
                        if len(candidate_method_list) == len(new_class_method_dic[original_class_name]["method_info"]):
                            qualified_method_list = candidate_method_list
                            candidate_class_qualified_name = qualified_class_name
                            break
                        if len(candidate_method_list) > len(qualified_method_list):
                            qualified_method_list = candidate_method_list
                            candidate_class_qualified_name = qualified_class_name
                if candidate_class_qualified_name != "" and "." not in original_class_name:
                    api_qualified_name.append({
                        "qualified_name": candidate_class_qualified_name,
                        "name_in_code": original_class_name,
                        "position": new_class_method_dic[original_class_name]["position"],
                        "code": code
                    })
                api_qualified_name.extend(qualified_method_list)
        return api_qualified_name

    # 连续方法调用转换成返回值类型，比如Thread.currentThread转换成它的返回值类型Thread
    def arrange_simple_name(self, class_method_dic):
        new_class_method_dic = {}
        for class_name in class_method_dic.keys():
            if "." not in class_name:
                new_class_method_dic[class_name] = class_method_dic[class_name]
            else:
                simple_class_name = self.point_name_2_simple_name(class_name)
                if simple_class_name != "":
                    new_class_method_dic[class_name] = class_method_dic[class_name]
                    new_class_method_dic[class_name]["return_value_class"] = simple_class_name
        return new_class_method_dic

    # 得到Thread.currentThread.getStackTrace的返回值的简单名或者全限定名
    def point_name_2_simple_name(self, point_class_name, return_qualified_name=False):
        simple_class_name = ""
        class_name = point_class_name.split(".")[0].strip()
        method_name = point_class_name.split(".")[1].strip()
        if class_name in self.short_name_dic:
            for qualified_class_name in self.short_name_dic[class_name]:
                class_info = self.api_graph.find_one_node_by_property("qualified_name", qualified_class_name)
                if "class" in class_info["labels"] or "interface" in class_info["labels"] or "primary type" in class_info["labels"]:
                    class_id = class_info["id"]
                    out_relation = self.api_graph.get_all_out_relations(class_id)
                    for start_id, relation, end_id in out_relation:
                        if relation == "has method":
                            method_node = self.api_graph.get_node_info_dict(end_id)
                            method_qualified_name = method_node["properties"]["qualified_name"]
                            method_simple_name = method_qualified_name.split("(")[0].split(".")[-1].strip()
                            if method_simple_name.lower() == method_name.lower():
                                method_out_relation = self.api_graph.get_all_out_relations(end_id)
                                for s, r, e in method_out_relation:
                                    if r == 'has return value':
                                        for s1, r1, e1 in self.api_graph.get_all_out_relations(e):
                                            if r1 == "type of":
                                                return_class_qualified_name = self.api_graph.get_node_info_dict(e1)["properties"]["qualified_name"]
                                                return_class_simple_name = return_class_qualified_name.split(".")[-1]
                                                if len(point_class_name.split(".")) == 2:
                                                    if return_qualified_name:
                                                        return return_class_qualified_name
                                                    return return_class_simple_name
                                                else:
                                                    new_point_class_name = return_class_simple_name + "." + point_class_name.split(".", 2)[2]
                                                    return_class_simple_name = self.point_name_2_simple_name(new_point_class_name, return_qualified_name)
                                                    if len(return_class_simple_name.split(".")) == 1 or return_qualified_name:
                                                        return return_class_simple_name
        return simple_class_name

    def graph_based_linker(self, locate_class_method_dic, class_object_pair):
        api_qualified_name = {}
        locate_class_apis = locate_class_method_dic.keys()
        for locate_class_api in locate_class_apis:
            class_api = locate_class_api.split('[')[0]
            if not class_api.__contains__('.'):
                locate_method_apis = locate_class_method_dic[locate_class_api]
                simple_methods = []
                for locate_method_api in locate_method_apis:
                    method_api = locate_method_api.split('[')[0]
                    simple_methods.append(self.CODE_NAME_UTIL.simplify(method_api))
                if class_api in self.qualified_name_set:
                    api_qualified_name[locate_class_api] = class_api
                    for index, locate_method_api in enumerate(locate_method_apis):
                        api_qualified_name[locate_method_api] = class_api + '.' + locate_method_api.split('[')[0]
                    continue
                candidate_classes = set()
                if class_api in self.short_name_dic:
                    candidate_classes.update(self.short_name_dic[class_api])
                if class_api in self.long_name_dic:
                    candidate_classes.update(self.long_name_dic[class_api])
                tmp_api_qualified_name = dict()
                for candidate_class in candidate_classes:
                    candidate_class_node = self.api_graph.find_one_node_by_property("qualified_name", candidate_class)
                    if candidate_class_node is None:
                        continue
                    if "class" not in candidate_class_node["labels"]:
                        continue
                    node_id = candidate_class_node['id']
                    out_relations_tuples = self.api_graph.get_all_out_relations(node_id)
                    all_methods = []
                    for out_relations_tuple in out_relations_tuples:
                        if out_relations_tuple[1] == 'has method':
                            all_methods.append(
                                self.api_graph.get_node_info_dict(out_relations_tuple[2])["properties"]["qualified_name"])
                    all_simple_methods = []
                    for all_method in all_methods:
                        all_simple_methods.append(self.CODE_NAME_UTIL.simplify(all_method))
                    if set(simple_methods) < set(all_simple_methods):
                        tmp_api_qualified_name.setdefault(candidate_class, [])
                        for simple_method in simple_methods:
                            tmp_api_qualified_name.setdefault(candidate_class, []).append(
                                candidate_class + '.' + simple_method)
                if len(tmp_api_qualified_name) >= 1:
                    class_qualified_name = list(tmp_api_qualified_name.keys())[0]
                    method_qualified_name = tmp_api_qualified_name[class_qualified_name]
                    api_qualified_name[locate_class_api] = class_qualified_name
                    for index, locate_method_api in enumerate(locate_method_apis):
                        api_qualified_name[locate_method_api] = method_qualified_name[index]
            else:
                object_name = class_api.split('.')[0]
                class_name = ''
                qualified_names = set()
                for key in class_object_pair.keys():
                    if object_name in class_object_pair[key]:
                        class_name = key
                for key in api_qualified_name.keys():
                    if class_name == "":
                        pass
                    elif key.__contains__(class_name):
                        return_value_type_name = api_qualified_name[key] + '.' + class_api.split('.')[1]
                        if return_value_type_name in self.short_name_dic:
                            qualified_names = self.short_name_dic[return_value_type_name]
                        if return_value_type_name in self.long_name_dic:
                            qualified_names = self.long_name_dic[return_value_type_name]
                        first_flag = False
                        for qualified_name in qualified_names:
                            api_node = self.api_graph.find_one_node_by_property("qualified_name", qualified_name)
                            node_id = api_node['id']
                            out_relations_tuples = self.api_graph.get_all_out_relations(node_id)
                            for out_relations_tuple in out_relations_tuples:
                                if out_relations_tuple[1] == 'return value type' or out_relations_tuple[1] == 'has return value':
                                    first_flag = True
                                    return_value_type = self.api_graph.get_node_info_dict(out_relations_tuple[2])["properties"]["qualified_name"]
                                    for method_name in locate_class_method_dic[locate_class_api]:
                                        api_qualified_name[method_name] = str(return_value_type) + '.' + str(method_name.split('[')[0])
                                    break
                            if first_flag:
                                break
                        break
        # print("baker链接: ", api_qualified_name)
        return api_qualified_name

    def process_api(self, api):
        api_split_parentheses = api.split("(")
        long_name = api_split_parentheses[0].strip()
        short_name = long_name.split(".")[-1].strip()
        parameter_list_for_api = []
        if "(" in api and ")" in api:
            parameter_list_for_api = api_split_parentheses[1].split(")")[0].strip().split(",")
        parameter_list_result = []
        for item in parameter_list_for_api:
            item = item.strip()
            if item:
                p = item.split(" ")[0]
                parameter_list_result.append(p)
        return long_name, short_name, parameter_list_result
