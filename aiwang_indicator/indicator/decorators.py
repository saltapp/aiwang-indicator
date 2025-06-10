from functools import wraps
import numpy as np
from ..model.series import BaseDatedSeries

def process_series(func):
    """装饰器：处理输入和输出的序列类型"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 处理输入参数
        processed_args = []
        dates = None
        for arg in args:
            if isinstance(arg, BaseDatedSeries):
                processed_args.append(arg.values)
                if dates is None:
                    dates = arg.dates
            else:
                processed_args.append(arg)
        
        # 调用原始函数
        result = func(*processed_args, **kwargs)
        
        # 处理输出
        if dates is not None and isinstance(result, (np.ndarray, list)):
            return BaseDatedSeries(result, dates)
        return result
    
    return wrapper