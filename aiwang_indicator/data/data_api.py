import numpy as np
from .loader.base_loader import BaseDataLoader

class DataApi:
    def __init__(self, data_loader: BaseDataLoader, default_stock_id: str, defaut_freq: str):
        self._data_loader = data_loader
        self._defaut_freq = defaut_freq
        self._default_stock_id = default_stock_id

    def close(self, code=None, freq=None):
        if code is None:
            code = self._default_stock_id
        if freq is None:
            freq = self._defaut_freq
        df = self._data_loader.get_stock_data_by_date(code, freq)
        if df.empty:
            return np.array([])
        return np.array(df['Close'], dtype=float)
    
    def high(self, code=None, freq=None):
        if code is None:
            code = self._default_stock_id
        if freq is None:
            freq = self._defaut_freq
        df = self._data_loader.get_stock_data_by_date(code, freq)
        if df.empty:
            return np.array([])
        return np.array(df['High'], dtype=float)
    
    def low(self, code=None, freq=None):
        if code is None:
            code = self._default_stock_id
        if freq is None:
            freq = self._defaut_freq
        df = self._data_loader.get_stock_data_by_date(code, freq)
        if df.empty:
            return np.array([])
        return np.array(df['Low'], dtype=float)
    
    def open(self, code=None, freq=None):   
        if code is None:
            code = self._default_stock_id
        if freq is None:
            freq = self._defaut_freq
        df = self._data_loader.get_stock_data_by_date(code, freq)
        if df.empty:
            return np.array([])
        return np.array(df['Open'], dtype=float)
    
    def date(self, code=None, freq=None):
        if code is None:
            code = self._default_stock_id
        if freq is None:
            freq = self._defaut_freq
        df = self._data_loader.get_stock_data_by_date(code, freq)
        if df.empty:
            return np.array([])
        return np.array(df['Date'], dtype=str)

    @property
    def close_default(self):
        return self.close(self._default_stock_id, self._defaut_freq)
    
    @property
    def high_default(self):
        return self.high(self._default_stock_id, self._defaut_freq)
    
    @property
    def low_default(self):
        return self.low(self._default_stock_id, self._defaut_freq)
    
    @property
    def open_default(self):
        return self.open(self._default_stock_id, self._defaut_freq)
    
    @property
    def date_default(self):
        return self.date(self._default_stock_id, self._defaut_freq)
