import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Optional

class IndicatorEngine:
    """Calculates technical indicators using pandas-ta."""
    
    @staticmethod
    def add_indicators(df: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
        """
        Add requested indicators to the DataFrame.
        Supported: RSI, EMA, SMA, MACD, VWAP, ATR, BBANDS, ADX, STOCH, WILLR
        """
        if df.empty:
            return df
            
        # Ensure we have a working copy
        df = df.copy()
        
        for ind in indicators:
            ind_upper = ind.upper()
            
            if ind_upper == 'RSI':
                df.ta.rsi(append=True)
            elif ind_upper == 'MACD':
                df.ta.macd(append=True)
            elif ind_upper == 'VWAP':
                if 'volume' in df.columns:
                    df.ta.vwap(append=True)
            elif ind_upper.startswith('EMA'):
                length = 14
                if '_' in ind_upper:
                    try:
                        length = int(ind_upper.split('_')[1])
                    except:
                        pass
                df.ta.ema(length=length, append=True)
            elif ind_upper.startswith('SMA'):
                length = 14
                if '_' in ind_upper:
                    try:
                        length = int(ind_upper.split('_')[1])
                    except:
                        pass
                df.ta.sma(length=length, append=True)
            elif ind_upper == 'BBANDS':
                df.ta.bbands(append=True)
            elif ind_upper == 'ATR':
                df.ta.atr(append=True)
            elif ind_upper == 'ADX':
                df.ta.adx(append=True)
            elif ind_upper == 'STOCH':
                df.ta.stoch(append=True)
            elif ind_upper == 'WILLR':
                df.ta.willr(append=True)
                
        return df

    @staticmethod
    def calculate_fibonacci_levels(df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate Fibonacci retracement levels based on the high/low of the period.
        """
        if df.empty:
            return {}
            
        max_price = df['high'].max()
        min_price = df['low'].min()
        diff = max_price - min_price
        
        return {
            "0.0": float(max_price),
            "23.6": float(max_price - 0.236 * diff),
            "38.2": float(max_price - 0.382 * diff),
            "50.0": float(max_price - 0.5 * diff),
            "61.8": float(max_price - 0.618 * diff),
            "78.6": float(max_price - 0.786 * diff),
            "100.0": float(min_price)
        }

    @staticmethod
    def get_support_resistance(df: pd.DataFrame) -> Dict[str, List[float]]:
        """
        Basic support/resistance detection using local min/max or pivots.
        Uses a simple window approach.
        """
        if len(df) < 20:
            return {"support": [], "resistance": []}
            
        # Simple Pivot High/Low
        # window of 10
        pivot_highs = df['high'][df['high'] == df['high'].rolling(10, center=True).max()]
        pivot_lows = df['low'][df['low'] == df['low'].rolling(10, center=True).min()]
        
        # Return unique sorted values, converted to float for JSON serialization
        return {
            "support": [float(v) for v in sorted(pivot_lows.unique().tolist())],
            "resistance": [float(v) for v in sorted(pivot_highs.unique().tolist())]
        }
