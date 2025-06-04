from .data.data_api import DataApi

class ExecutionContext(object):
    def __init__(self, data_loader, default_stock_id, default_freq):
        self._set_default_freq(default_freq)
        self._set_default_stock_id(default_stock_id)
        self._data_api = DataApi(data_loader, self._default_stock_id, self._default_freq)

    def _set_default_stock_id(self, stock_id):
        if not isinstance(stock_id, str):
            raise ValueError("Default stock ID must be a string.")
        self._default_stock_id = stock_id

    def _set_default_freq(self, freq):
        valid_freqs = ['30min', '60min', 'daily', 'weekly', 'monthly']
        if freq not in valid_freqs:
            raise ValueError(f"Invalid frequency: {freq}. Must be one of {valid_freqs}.")
        self._default_freq = freq

    def get_data_api(self):
        return self._data_api



