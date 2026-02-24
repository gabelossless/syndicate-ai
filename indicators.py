def calculate_ema(prices: list, period: int) -> list:
    """Calculates the Exponential Moving Average (EMA)."""
    if not prices or len(prices) < period:
        return []
    
    ema = []
    multiplier = 2 / (period + 1)
    
    # Simple Moving Average for the first EMA value
    sma = sum(prices[:period]) / period
    ema.append(sma)
    
    # Calculate EMA for the rest of the prices
    for price in prices[period:]:
        current_ema = (price - ema[-1]) * multiplier + ema[-1]
        ema.append(current_ema)
        
    # Pad the beginning with None to match the input length
    return [None] * (period - 1) + ema

def calculate_macd(prices: list, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> dict:
    """Calculates the MACD line, Signal line, and Histogram."""
    if not prices or len(prices) < slow_period + signal_period:
        return {"macd": [], "signal": [], "histogram": []}
        
    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)
    
    macd_line = []
    for i in range(len(prices)):
        if fast_ema[i] is not None and slow_ema[i] is not None:
            macd_line.append(fast_ema[i] - slow_ema[i])
        else:
            macd_line.append(None)
            
    # Calculate Signal line (EMA of MACD line)
    # Filter out None values for EMA calculation
    valid_macd = [x for x in macd_line if x is not None]
    signal_line_valid = calculate_ema(valid_macd, signal_period)
    
    signal_line = [None] * (len(prices) - len(signal_line_valid)) + signal_line_valid
    
    histogram = []
    for i in range(len(prices)):
        if macd_line[i] is not None and signal_line[i] is not None:
            histogram.append(macd_line[i] - signal_line[i])
        else:
            histogram.append(None)
            
    return {"macd": macd_line, "signal": signal_line, "histogram": histogram}

def calculate_rsi(prices: list, period: int = 14) -> list:
    """Calculates the Relative Strength Index (RSI)."""
    if not prices or len(prices) <= period:
        return []
        
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    rsi = [None] * period
    
    if avg_loss == 0:
        rsi.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi.append(100.0 - (100.0 / (1.0 + rs)))
        
    for i in range(period, len(prices) - 1):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period
        
        if avg_loss == 0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100.0 - (100.0 / (1.0 + rs)))
            
    return rsi

def generate_technical_score(prices: list) -> dict:
    """
    Combines RSI, MACD, and EMA to generate a technical score from -100 to 100.
    Returns the score and the latest indicator values.
    """
    if len(prices) < 35: # Need enough data for MACD
        return {"score": 0, "rsi": 50, "macd_hist": 0, "trend": "neutral"}
        
    rsi_values = calculate_rsi(prices, 14)
    macd_data = calculate_macd(prices)
    ema_50 = calculate_ema(prices, 50)
    
    latest_rsi = rsi_values[-1] if rsi_values[-1] is not None else 50
    latest_hist = macd_data["histogram"][-1] if macd_data["histogram"][-1] is not None else 0
    latest_price = prices[-1]
    latest_ema_50 = ema_50[-1] if ema_50[-1] is not None else latest_price
    
    score = 0
    
    # RSI Logic
    if latest_rsi < 30:
        score += 40 # Oversold, bullish
    elif latest_rsi > 70:
        score -= 40 # Overbought, bearish
    elif latest_rsi > 50:
        score += 10
    else:
        score -= 10
        
    # MACD Logic
    if latest_hist > 0:
        score += 30 # Bullish momentum
    else:
        score -= 30 # Bearish momentum
        
    # Trend Logic (Price vs 50 EMA)
    trend = "neutral"
    if latest_price > latest_ema_50:
        score += 30
        trend = "bullish"
    else:
        score -= 30
        trend = "bearish"
        
    # Cap score between -100 and 100
    score = max(-100, min(100, score))
    
    return {
        "score": score,
        "rsi": round(latest_rsi, 2),
        "macd_hist": round(latest_hist, 2),
        "trend": trend
    }
