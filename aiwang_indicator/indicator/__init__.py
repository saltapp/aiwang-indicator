# -*- coding: utf-8 -*-
from .decorators import process_series
from .indicator import *

# 获取所有indicator.py中的函数
import sys
import types

# 获取所有indicator模块中的函数
_indicator_module = sys.modules[__name__].__dict__
_indicator_funcs = {}

# 使用list()创建items的副本进行迭代
for name, obj in list(_indicator_module.items()):
    if isinstance(obj, types.FunctionType) and obj.__module__.endswith('indicator'):
        # 如果函数还没有被装饰器包装，则包装它
        if not hasattr(obj, '_decorated'):
            _indicator_funcs[name] = process_series(obj)
            _indicator_funcs[name]._decorated = True
        else:
            _indicator_funcs[name] = obj

# 更新模块的全局命名空间
globals().update(_indicator_funcs)

# 导出所有函数
__all__ = list(_indicator_funcs.keys())