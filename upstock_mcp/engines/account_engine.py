from typing import Dict, List, Any

class AccountEngine:
    """"Processes user account data into agent-friendly formats."""
    
    @staticmethod
    def summarize_portfolio(holdings: List[Dict], positions: List[Dict]) -> Dict:
        """
        Aggregate holdings and positions to give a snapshot of exposure.
        """
        total_holdings_value = 0.0
        total_pnl = 0.0
        
        # Calculate Holdings metrics using safe fetching
        for h in holdings:
            # Check for keys, Upstox SDK might return different implementations.
            # Assuming dict here from the adapter.
            try:
                # keys might be 'last_price', 'average_price', 'quantity'
                # Note: Upstox SDK response keys are often snake_case or camelCase depending on version.
                # We will be defensive.
                qty = float(h.get('quantity', 0))
                ltp = float(h.get('last_price', 0))
                avg = float(h.get('average_price', 0))
                
                val = qty * ltp
                pnl = (ltp - avg) * qty
                
                total_holdings_value += val
                total_pnl += pnl
            except (ValueError, TypeError):
                continue
                
        # Calculate Positions metrics
        open_positions = 0
        intraday_pnl = 0.0
        
        for p in positions:
            try:
                qty = float(p.get('quantity', 0))
                if qty != 0:
                    open_positions += 1
                
                # realized + unrealized pnl usually
                pnl = float(p.get('pnl', 0)) # if available directly
                # otherwise calc: (sell_amt - buy_amt) + (net_qty * ltp)
                intraday_pnl += pnl
            except (ValueError, TypeError):
                continue
                
        return {
            "investment_value": round(total_holdings_value, 2),
            "holdings_pnl": round(total_pnl, 2),
            "active_positions_count": open_positions,
            "positions_pnl": round(intraday_pnl, 2),
            "total_account_exposure": round(total_holdings_value, 2) # simplified
        }
