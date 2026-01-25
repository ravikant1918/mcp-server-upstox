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
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        # Upstox returns candles in reverse chronological order (newest first).
        # We usually want oldest first for TA.
        df = df.sort_values('timestamp', ascending=True).reset_index(drop=True)
        
        # Convert timestamp to string to avoid serialization issues with pandas Timestamp
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        return df

    @staticmethod
    def resample_candles(df: pd.DataFrame, interval: str) -> pd.DataFrame:
        """
        Resample 1-minute candles to a larger interval (e.g., '5min', '15min').
        Requires a DataFrame with a DatetimeIndex.
        """
        if df.empty or len(df) < 2:
            return df
            
        # Set timestamp as index for resampling
        df = df.set_index('timestamp')
        
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
        resampled = df.resample(rule).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
            'oi': 'last'
        }).dropna()
        
        return resampled.reset_index()

    @staticmethod
    def get_latest_candle(df: pd.DataFrame) -> Dict:
        if df.empty:
            return {}
        return df.iloc[-1].to_dict()
