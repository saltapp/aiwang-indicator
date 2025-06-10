from .base_loader import BaseDataLoader
import pandas as pd
import akshare as ak

class AkLoader(BaseDataLoader):

    def __init__(self, start_date):
        super().__init__(start_date)

    def get_stock_data(self, code : str, freq: str):
        if freq in ['30min', '60min']:
            full_code = f'sh{code}' if code.startswith('6') else f'sz{code}'
            freq_para = '30' if freq == '30min' else '60'
            df = ak.stock_zh_a_minute(symbol=full_code, period=freq_para, adjust="qfq")
        else:
            if code.startswith('HS'):
                df = ak.stock_hk_daily(symbol=code[2:], adjust="qfq")
            else:
                df = ak.stock_zh_a_hist(symbol=code, period=freq, start_date=self.get_start_date(), adjust="qfq")
        return self._convert_to_standard_df(df, freq)

    def _convert_to_standard_df(self, df, freq):
        """
        Convert a fetched dataframe to a standard format with columns:
        ['Date', 'Open', 'High', 'Low', 'Close'].

        The function handles two types of input dataframes:
        1. Chinese column names: ['日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量']
        where '日期' -> 'Date', '开盘' -> 'Open', '最高' -> 'High',
        '最低' -> 'Low', '收盘' -> 'Close'.

        2. English column names: ['day', 'open', 'high', 'low', 'close', 'volume']
        where 'day' -> 'Date', 'open' -> 'Open', 'high' -> 'High',
        'low' -> 'Low', 'close' -> 'Close'.
        """
        if '日期' in df.columns:
            df = df.rename(columns={
                '日期': 'Date',
                '开盘': 'Open',
                '最高': 'High',
                '最低': 'Low',
                '收盘': 'Close'
            })
        elif 'day' in df.columns:
            df = df.rename(columns={
                'day': 'Date',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close'
            })
        elif 'date' in df.columns:
            df = df.rename(columns={
                'date': 'Date',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close'
            })
        else:
            raise ValueError("DataFrame schema not recognized.")
        
        # Select only the standard columns.
        df = df[['Date', 'Open', 'High', 'Low', 'Close']]
        # Convert OHLC columns to numeric types
        df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].apply(pd.to_numeric, errors='coerce')
        if freq in ['30min', '60min']:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y%m%d %H:%M:%S')
        else:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y%m%d')
        return df