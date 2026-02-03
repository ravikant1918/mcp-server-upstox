import pandas as pd
from typing import List, Dict
import logging

class CandleEngine:
    """Processes raw candle data into structured DataFrames."""
    
    @staticmethod
    def to_dataframe(candles_data: List[List]) -> pd.DataFrame:
        """
        Convert Upstox raw candle list to DataFrame.
        Expected format: [[timestamp, open, high, low, close, volume, oi], ...]
        """
        if not candles_data:
            return pd.DataFrame()
            
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'oi']
        df = pd.DataFrame(candles_data, columns=columns)
        
        # Ensure correct types
        # Upstox timestamps are often ISO strings or similar, converting to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        # Upstox returns candles in reverse chronological order (newest first).
        # We usually want oldest first for TA.
        df = df.sort_values('timestamp', ascending=True).reset_index(drop=True)
        
        # NOTE: We keep 'timestamp' as pd.Timestamp objects here to allow for 
        # proper resampling and time-based operations. 
        # Serialization to string happens in utils.format_response / utils.to_json_safe.
        
        return df

    @staticmethod
    def resample_candles(df: pd.DataFrame, interval: str) -> pd.DataFrame:
        """
        Resample 1-minute candles to a larger interval (e.g., '5min', '15min').
        Requires a DataFrame with a DatetimeIndex or a 'timestamp' column of datetime type.
        """
        if df.empty or len(df) < 2:
            return df
            
        # Ensure we work on a copy to avoid SettingWithCopy warnings on the original
        df = df.copy()

        # Set timestamp as index for resampling if it's not already
        if not isinstance(df.index, pd.DatetimeIndex):
            if 'timestamp' in df.columns:
                 df['timestamp'] = pd.to_datetime(df['timestamp']) # safety check
                 df = df.set_index('timestamp')
            else:
                # Can't resample without time index
                return df
        
        # Mapping common MCP intervals to pandas offset aliases
        # 1minute -> 1min, 5minute -> 5min, etc.
        resample_map = {
            "1minute": "1min",
            "3minute": "3min",
            "5minute": "5min",
            "10minute": "10min",
            "15minute": "15min",
            "30minute": "30min",
            "1hour": "1H",
            "1day": "1D"
        }
        
        rule = resample_map.get(interval, interval)
        if "minute" in rule: rule = rule.replace("minute", "min")
        
        # Resample logic
        # Aggregation: 
        # Open: first, High: max, Low: min, Close: last, Volume: sum, OI: last
        resampler = df.resample(rule)
        
        resampled = resampler.agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
            'oi': 'last'
        })
        
        # Drop bins with no data (e.g. market closed times if not expecting gaps)
        # However, for some charts we might want gaps. Defaulting to dropna() as per previous logic.
        resampled = resampled.dropna()
        
        return resampled.reset_index()

    @staticmethod
    def get_latest_candle(df: pd.DataFrame) -> Dict:
        if df.empty:
            return {}
        # utils.to_json_safe will handle timestamp conversion
        return df.iloc[-1].to_dict()
