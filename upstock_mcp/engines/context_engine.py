import pandas as pd
from typing import Dict, List

class ContextEngine:
    """"Generates high-level market context and trend summaries."""
    
    @staticmethod
    def analyze_trend(df: pd.DataFrame) -> Dict:
        """
        Analyze trend based on EMAs and Price Action.
        Returns: { 'trend': 'Bullish'|'Bearish'|'Sideways', 'strength': 'Strong'|'Weak' }
        """
        if df.empty or len(df) < 50:
            return {"trend": "Unknown", "strength": "None"}
            
        # Ensure EMAs are present (assuming IndicatorEngine added them or we calc here)
        # For robustness, we calculate simple ones here strictly for context if missing
        if 'EMA_20' not in df.columns:
            df.ta.ema(length=20, append=True)
        if 'EMA_50' not in df.columns:
            df.ta.ema(length=50, append=True)
        if 'EMA_200' not in df.columns:
            df.ta.ema(length=200, append=True)
            
        # Get latest values
        current = df.iloc[-1]
        price = current['close']
        ema20 = current.get('EMA_20', 0)
        ema50 = current.get('EMA_50', 0)
        ema200 = current.get('EMA_200', 0)
        
        trend = "Sideways"
        strength = "Weak"
        
        # Bullish Logic
        if price > ema20 > ema50:
            trend = "Bullish"
            if ema50 > ema200:
                strength = "Strong"
            else:
                strength = "Moderate"
        elif price < ema20 < ema50:
            trend = "Bearish"
            if ema50 < ema200:
                strength = "Strong"
            else:
                strength = "Moderate"
                
        # Volatility check using ATR if available, else visual range
        volatility = "Normal"
        if 'ATR_14' in df.columns:
             atr = current['ATR_14']
             # Simple heuristic: ATR > 1% of price is high volatility? logic varies.
             if atr > (price * 0.01):
                 volatility = "High"
             elif atr < (price * 0.002):
                 volatility = "Low"
                 
        return {
            "trend": trend,
            "strength": strength,
            "volatility": volatility,
            "bias_summary": f"{strength} {trend} trend with {volatility} volatility. Price is {'above' if price > ema50 else 'below'} 50 EMA."
        }

    @staticmethod
    def get_multi_timeframe_summary(daily_context: Dict, hourly_context: Dict) -> Dict:
        """ Synthesize bias from multiple timeframes. """
        bias = "Neutral"
        
        d_trend = daily_context.get("trend")
        h_trend = hourly_context.get("trend")
        
        if d_trend == "Bullish" and h_trend == "Bullish":
            bias = "Strongly Bullish"
        elif d_trend == "Bearish" and h_trend == "Bearish":
            bias = "Strongly Bearish"
        elif d_trend == "Bullish" and h_trend == "Bearish":
            bias = "Pullback in Uptrend"
        elif d_trend == "Bearish" and h_trend == "Bullish":
            bias = "Rally in Downtrend"
            
        return {
            "overall_bias": bias,
            "daily_alignment": d_trend,
            "intraday_alignment": h_trend
        }
