import numpy as np
import pandas as pd

class BaseDatedSeries:
    def __init__(self, values, dates):
        self.data = pd.Series(values, index=dates)
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.data + other, self.data.index)
        
        # 找出所有时间点的并集
        all_dates = self.data.index.union(other.data.index)
        
        # 用最后一个有效值向前填充
        series1 = self.data.reindex(all_dates, method='ffill')
        series2 = other.data.reindex(all_dates, method='ffill')
        
        # 计算结果
        result = series1 + series2
        
        return self.__class__(result.values, all_dates)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.data - other, self.data.index)
        
        # 找出所有时间点的并集
        all_dates = self.data.index.union(other.data.index)
        
        # 用最后一个有效值向前填充
        series1 = self.data.reindex(all_dates, method='ffill')
        series2 = other.data.reindex(all_dates, method='ffill')
        
        # 计算结果
        result = series1 - series2
        
        return self.__class__(result.values, all_dates)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.data * other, self.data.index)
        
        all_dates = self.data.index.union(other.data.index)
        series1 = self.data.reindex(all_dates, method='ffill')
        series2 = other.data.reindex(all_dates, method='ffill')
        result = series1 * series2
        return self.__class__(result.values, all_dates)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.data / other, self.data.index)
        
        all_dates = self.data.index.union(other.data.index)
        series1 = self.data.reindex(all_dates, method='ffill')
        series2 = other.data.reindex(all_dates, method='ffill')
        result = series1 / series2
        return self.__class__(result.values, all_dates)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __repr__(self):
        return repr(self.data)
    
    @property
    def values(self):
        return self.data.values
    
    @property
    def dates(self):
        return self.data.index