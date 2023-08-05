#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/17
------------------------------------------
@Modify: 2020/11/17
------------------------------------------
@Description:
"""
from qualified_name_extractor.code_based.base import BakerBaseClass

print(BakerBaseClass.is_float(".01f"))
print(BakerBaseClass.is_float("-.01f"))
print(BakerBaseClass.is_float("10.01f"))
print(BakerBaseClass.is_float("0.01"))
print(BakerBaseClass.is_float("-10f"))

print("-" * 50)
print(BakerBaseClass.is_double(".01f"))
print(BakerBaseClass.is_double("-.01f"))
print(BakerBaseClass.is_double("10.01f"))
print(BakerBaseClass.is_double("10f"))
print(BakerBaseClass.is_double("-10f"))

print("-" * 50)
print(BakerBaseClass.is_double(".01"))
print(BakerBaseClass.is_double("-.01"))
print(BakerBaseClass.is_double("10.01"))
print(BakerBaseClass.is_double("10"))
print(BakerBaseClass.is_double("-10"))
