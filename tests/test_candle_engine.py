import sys
import os
import pandas as pd
import pytest
from datetime import datetime

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../upstock_mcp')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from upstock_mcp.engines.candle_engine import CandleEngine

class TestCandleEngine:
    
    def test_to_dataframe_conversion(self):
        # timestamp, open, high, low, close, volume, oi
        raw_data = [
            ["2024-01-01T10:00:00", 100.0, 105.0, 99.0, 102.0, 1000, 50],
            ["2024-01-01T10:01:00", 102.0, 103.0, 101.0, 102.5, 500, 55],
        ]
        
        df = CandleEngine.to_dataframe(raw_data)
        
        assert not df.empty
        assert len(df) == 2
        # Check types
        assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])
        assert pd.api.types.is_float_dtype(df['open'])
        
        # Check sorting (oldest first)
        assert df.iloc[0]['timestamp'] == pd.Timestamp("2024-01-01T10:00:00")
        
    def test_resample_candles(self):
        # Create 5 minutes of 1-minute data
        raw_data = [
            ["2024-01-01T10:00:00", 100, 105, 95, 101, 100, 0], # min: 95, max: 105
            ["2024-01-01T10:01:00", 101, 102, 100, 102, 100, 0],
            ["2024-01-01T10:02:00", 102, 104, 101, 103, 100, 0],
            ["2024-01-01T10:03:00", 103, 103, 102, 102, 100, 0],
            ["2024-01-01T10:04:00", 102, 106, 102, 105, 100, 0], # max: 106, close: 105
        ]
        df = CandleEngine.to_dataframe(raw_data)
        
        # Resample to 5 minutes
        resampled_df = CandleEngine.resample_candles(df, "5minute")
        
        assert len(resampled_df) == 1
        candle = resampled_df.iloc[0]
        
        assert candle['timestamp'] == pd.Timestamp("2024-01-01T10:00:00")
        assert candle['open'] == 100.0
        assert candle['high'] == 106.0  # Max of the period
        assert candle['low'] == 95.0    # Min of the period
        assert candle['close'] == 105.0 # Last close
        assert candle['volume'] == 500  # Sum
