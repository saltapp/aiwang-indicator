from abc import abstractmethod
import warnings
import pandas as pd

class BaseDataLoader:
    def __init__(self, start_date: str):
        self._start_date = start_date

    def get_start_date(self):
        if isinstance(self._start_date, str):
            return self._start_date
        else:
            raise ValueError("Start date must be a string representing YYYYMMDD.")
        
    @abstractmethod
    def get_stock_data(self, code, freq):
        pass

    #检查第一个时间是否是self._start_date, 然后根据开始时间对齐获得的stock数据。
    def get_stock_data_by_date(self, code, freq):
        """
        Get stock data for a specific code and frequency starting from a given date.
        """
        df = self.get_stock_data(code, freq)
        if df.empty:
            return df
        
        first_date = pd.to_datetime(df['Date'].iloc[0])
        if first_date > pd.to_datetime(self.get_start_date()):
            warnings.warn(f"Data source does not start from {self.get_start_date()}. Actual start date: {first_date}.")
            return df
        
        return df[df['Date'] >= self.get_start_date()]
    
    
