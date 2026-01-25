import pandas as pd
import pandas_ta as ta
from typing import Dict, List

class PatternEngine:
    """Detects candlestick patterns."""
    
    @staticmethod
    def detect_patterns(df: pd.DataFrame) -> List[Dict]:
        """
        Run pattern detection on the latest data.
        Returns a list of detected patterns for the latest candle.
        """
        if df.empty:
            return []
            
        # We need to run pattern detection on the whole series then check the last row
        # pandas_ta supports 'cdl_pattern' method
        
        # Patterns to check
        patterns = ['doji', 'hammer', 'engulfing', 'morningstar', 'eveningstar', 'shootingstar']
        
        # Run detection
        # df.ta.cdl_pattern(name=patterns, append=True) creates columns like CDL_DOJI, CDL_HAMMER etc.
        # Values are usually non-zero (100 or -100) if pattern detected
        
        try:
             # Some pandas_ta versions expect 'name' to be a string or list
            pattern_result = df.ta.cdl_pattern(name=patterns, append=False)
        except Exception:
            # Fallback if specific pattern names fail, try 'all' or specific individual calls
            # For robustness, let's keep it simple or handle individually
            return []
            
        if pattern_result is None or pattern_result.empty:
            return []
            
        # Check the last row
        last_row = pattern_result.iloc[-1]
        detected = []
        
        for col in pattern_result.columns:
            val = last_row[col]
            if val != 0:
                # CDL_DOJI_10_0.1 -> parse name
                name = col.replace('CDL_', '').split('_')[0]
                
                # logic for strength/signal
                signal = "Bullish" if val > 0 else "Bearish"
                
                detected.append({
                    "pattern": name,
                    "signal": signal,
                    "strength": "Moderate", # Hard to determine from 100/-100 alone without more context
                    "value": int(val)
                })
                
        return detected
