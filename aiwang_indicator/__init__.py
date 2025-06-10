# -*- coding: utf-8 -*-
#

from .indicator import *
from .context import ExecutionContext

# 先定义全局变量
execution_context = None
CLOSE = None
OPEN = None
HIGH = None
LOW = None
DATE = None
C = None
O = None
H = None
L = None
D = None

def _is_freq_parameter(freq_param):
    """
    Check if the given parameter is a valid frequency parameter.
    """
    return isinstance(freq_param, str) and freq_param in ['30min', '60min', 'daily', 'weekly', 'monthly']

import functools

def _data_api_method(method_name, code=None, freq=None):
    api = execution_context.get_data_api()
    method = getattr(api, method_name)
    if _is_freq_parameter(code):
        return method(None, code)
    return method(code, freq)

def set_data_loader(data_loader, *, default_stock_id, default_freq='daily'):
    """
    Set the data loader for the execution context.
    """
    global execution_context, CLOSE, OPEN, HIGH, LOW, DATE, C, O, H, L, D
    execution_context = ExecutionContext(data_loader=data_loader, default_stock_id=default_stock_id, default_freq=default_freq)

    CLOSE = functools.partial(_data_api_method, 'close')
    HIGH = functools.partial(_data_api_method, 'high')
    LOW = functools.partial(_data_api_method, 'low')
    OPEN = functools.partial(_data_api_method, 'open')
    DATE = functools.partial(_data_api_method, 'date')

    C = execution_context.get_data_api().close_default
    O = execution_context.get_data_api().open_default
    H = execution_context.get_data_api().high_default
    L = execution_context.get_data_api().low_default
    D = execution_context.get_data_api().date_default


import types as _types
import sys as _sys

# 自动收集 indicator.py 中的所有函数名
_indicator_module = _sys.modules[__name__].__dict__
_indicator_funcs = [
    name for name, obj in _indicator_module.items()
    if isinstance(obj, _types.FunctionType) and obj.__module__.endswith("indicator")
]

__all__ = [
    # ...其它导出...
    "set_data_loader", "CLOSE", "OPEN", "HIGH", "LOW", "DATE", "C", "O", "H", "L", "D"
] + _indicator_funcs