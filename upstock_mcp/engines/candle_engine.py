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
        
        return df

    @staticmethod
    def get_latest_candle(df: pd.DataFrame) -> Dict:
        if df.empty:
            return {}
        return df.iloc[-1].to_dict()
