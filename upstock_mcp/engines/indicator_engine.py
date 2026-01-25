import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Optional

class IndicatorEngine:
    """Calculates technical indicators using pandas-ta."""
    
    @staticmethod
    def add_indicators(df: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
        """
        Add requested indicators to the DataFrame.
        Supported: RSI, EMA, SMA, MACD, VWAP, ATR, BBANDS
        """
        if df.empty:
            return df
            
        # Ensure we have a working copy
        df = df.copy()
        
        # Helper to parse complex requests like 'EMA_50' if we wanted to support it dynamic ally
        # For now, we support standard default params or specific presets
        
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
                # Handle EMA or EMA_20
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
                
        return df

    @staticmethod
    def get_support_resistance(df: pd.DataFrame) -> Dict[str, List[float]]:
        """
        Basic support/resistance detection using local min/max or pivots.
        Uses a simple window approach.
        """
        if len(df) < 20:
            return {"support": [], "resistance": []}
            
        # Simple Pivot High/Low
        # window of 5
        pivot_highs = df['high'][df['high'] == df['high'].rolling(10, center=True).max()]
        pivot_lows = df['low'][df['low'] == df['low'].rolling(10, center=True).min()]
        
        # Filter recent ones or significant ones? 
        # Return unique sorted values
        return {
            "support": sorted(pivot_lows.unique().tolist()),
            "resistance": sorted(pivot_highs.unique().tolist())
        }
