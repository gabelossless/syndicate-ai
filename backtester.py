import asyncio
import logging
from exchange_client import exchange_client
from indicators import generate_technical_score

logger = logging.getLogger("Backtester")

class BacktestResult:
    def __init__(self):
        self.trades: list[dict] = []
        self.equity_curve: list[float] = []
        self.starting_balance = 0.0
        self.final_balance = 0.0

    @property
    def total_return_pct(self) -> float:
        if self.starting_balance == 0:
            return 0.0
        return round(((self.final_balance - self.starting_balance) / self.starting_balance) * 100, 2)

    @property
    def win_rate(self) -> float:
        if not self.trades:
            return 0.0
        wins = sum(1 for t in self.trades if t.get("pnl", 0) > 0)
        return round((wins / len(self.trades)) * 100, 1)

    @property
    def max_drawdown(self) -> float:
        if not self.equity_curve:
            return 0.0
        peak = self.equity_curve[0]
        max_dd = 0.0
        for val in self.equity_curve:
            if val > peak:
                peak = val
            dd = (peak - val) / peak * 100 if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd
        return round(max_dd, 2)

    @property
    def sharpe_ratio(self) -> float:
        """Simplified Sharpe using daily returns."""
        if len(self.equity_curve) < 2:
            return 0.0
        returns = [
            (self.equity_curve[i] - self.equity_curve[i - 1]) / self.equity_curve[i - 1]
            for i in range(1, len(self.equity_curve))
            if self.equity_curve[i - 1] > 0
        ]
        if not returns:
            return 0.0
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        return round((avg_return / std_dev) * (252 ** 0.5), 2) if std_dev > 0 else 0.0


class Backtester:
    """
    Replays historical OHLCV data through the technical indicator strategy
    to evaluate performance before risking real capital.
    """

    def __init__(self, starting_balance: float = 10000.0, risk_per_trade: float = 0.25):
        self.starting_balance = starting_balance
        self.risk_per_trade = risk_per_trade  # 25% of balance per trade

    async def run(self, symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 500) -> BacktestResult:
        """
        Fetches historical data and runs a simulated trading loop.
        Uses a rolling window of 60 candles to calculate indicators.
        """
        result = BacktestResult()
        result.starting_balance = self.starting_balance

        logger.info(f"Starting backtest: {symbol} | {timeframe} | {limit} candles")
        ohlcv = await exchange_client.fetch_ohlcv(symbol, timeframe, limit=limit)

        if not ohlcv or len(ohlcv) < 70:
            logger.warning("Not enough OHLCV data for backtesting.")
            return result

        balance = self.starting_balance
        position = None  # {"entry_price": float, "qty": float, "side": "BUY"}
        result.equity_curve.append(balance)

        window = 60  # Minimum candles needed to compute indicators

        for i in range(window, len(ohlcv)):
            candles_window = ohlcv[i - window : i]
            prices = [float(c[4]) for c in candles_window]  # Close prices
            current_price = float(ohlcv[i][4])

            score_data = generate_technical_score(prices)
            score = score_data.get("score", 0)

            # Strategy Logic: Enter on strong signals, exit on reversal
            if position is None:
                if score >= 60:  # Strong BUY signal
                    qty = (balance * self.risk_per_trade) / current_price
                    position = {"entry_price": current_price, "qty": qty, "side": "BUY", "candle": i}
                elif score <= -60:  # Strong SELL/SHORT signal (simulated)
                    qty = (balance * self.risk_per_trade) / current_price
                    position = {"entry_price": current_price, "qty": qty, "side": "SELL", "candle": i}
            else:
                # Exit conditions: reversal signal or stop loss
                should_exit = False
                pnl = 0.0

                if position["side"] == "BUY":
                    pnl = (current_price - position["entry_price"]) * position["qty"]
                    # Exit on bearish reversal or 5% stop loss
                    if score <= -30 or pnl < -(balance * 0.05):
                        should_exit = True
                elif position["side"] == "SELL":
                    pnl = (position["entry_price"] - current_price) * position["qty"]
                    # Exit on bullish reversal or 5% stop loss
                    if score >= 30 or pnl < -(balance * 0.05):
                        should_exit = True

                if should_exit:
                    balance += pnl
                    result.trades.append({
                        "symbol": symbol,
                        "side": position["side"],
                        "entry": round(position["entry_price"], 4),
                        "exit": round(current_price, 4),
                        "pnl": round(pnl, 2),
                        "balance_after": round(balance, 2),
                    })
                    position = None

            result.equity_curve.append(round(balance, 2))

        # Close any open position at end
        if position:
            current_price = float(ohlcv[-1][4])
            pnl = (current_price - position["entry_price"]) * position["qty"] if position["side"] == "BUY" \
                else (position["entry_price"] - current_price) * position["qty"]
            balance += pnl
            result.trades.append({
                "symbol": symbol,
                "side": position["side"],
                "entry": round(position["entry_price"], 4),
                "exit": round(current_price, 4),
                "pnl": round(pnl, 2),
                "balance_after": round(balance, 2),
                "note": "Closed at end of backtest"
            })

        result.final_balance = round(balance, 2)
        logger.info(f"Backtest complete. Return: {result.total_return_pct}% | Trades: {len(result.trades)} | Win Rate: {result.win_rate}%")
        return result

    def generate_html_report(self, result: BacktestResult, symbol: str) -> str:
        """Generates a self-contained HTML report with an embedded equity curve chart."""
        trade_rows = "".join([
            f"<tr class='{'win' if t.get('pnl',0)>0 else 'loss'}'>"
            f"<td>{t['side']}</td><td>{t['entry']}</td><td>{t['exit']}</td>"
            f"<td>${t['pnl']:+.2f}</td><td>${t['balance_after']:.2f}</td></tr>"
            for t in result.trades
        ])
        equity_data = ",".join(str(e) for e in result.equity_curve)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Syndicate.ai Backtest Report — {symbol}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #0a0a0f; color: #e2e8f0; margin: 0; padding: 24px; }}
  h1 {{ color: #10b981; text-align: center; letter-spacing: 2px; }}
  .metrics {{ display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; margin: 24px 0; }}
  .card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 20px 32px; text-align: center; }}
  .card .val {{ font-size: 2rem; font-weight: 900; color: #10b981; }}
  .card .lbl {{ font-size: 0.7rem; text-transform: uppercase; color: rgba(255,255,255,0.4); letter-spacing: 1px; margin-top: 4px; }}
  canvas {{ max-height: 300px; margin: 24px 0; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
  th {{ background: rgba(16,185,129,0.2); color: #10b981; padding: 10px; text-align: left; font-size: 0.8rem; text-transform: uppercase; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; }}
  .win td {{ color: #34d399; }} .loss td {{ color: #f87171; }}
</style>
</head>
<body>
<h1>⚡ Syndicate.ai Backtest — {symbol}</h1>
<div class="metrics">
  <div class="card"><div class="val">{result.total_return_pct:+.1f}%</div><div class="lbl">Total Return</div></div>
  <div class="card"><div class="val">{result.win_rate}%</div><div class="lbl">Win Rate</div></div>
  <div class="card"><div class="val">{result.max_drawdown}%</div><div class="lbl">Max Drawdown</div></div>
  <div class="card"><div class="val">{result.sharpe_ratio}</div><div class="lbl">Sharpe Ratio</div></div>
  <div class="card"><div class="val">{len(result.trades)}</div><div class="lbl">Total Trades</div></div>
  <div class="card"><div class="val">${result.final_balance:,.0f}</div><div class="lbl">Final Balance</div></div>
</div>
<canvas id="equityChart"></canvas>
<table><thead><tr><th>Side</th><th>Entry</th><th>Exit</th><th>P&L</th><th>Balance</th></tr></thead>
<tbody>{trade_rows}</tbody></table>
<script>
const ctx = document.getElementById('equityChart').getContext('2d');
new Chart(ctx, {{
  type: 'line',
  data: {{
    labels: Array.from({{length: {len(result.equity_curve)}}}, (_,i) => i),
    datasets: [{{
      label: 'Equity Curve ($)',
      data: [{equity_data}],
      borderColor: '#10b981',
      backgroundColor: 'rgba(16,185,129,0.1)',
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointRadius: 0,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ labels: {{ color: '#e2e8f0' }} }} }},
    scales: {{
      x: {{ ticks: {{ color: 'rgba(255,255,255,0.3)' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
      y: {{ ticks: {{ color: 'rgba(255,255,255,0.3)' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}
    }}
  }}
}});
</script>
</body></html>"""
        return html


backtester = Backtester()

if __name__ == "__main__":
    async def main():
        result = await backtester.run("BTC/USDT", "1h", 300)
        html = backtester.generate_html_report(result, "BTC/USDT")
        with open("backtest_report.html", "w") as f:
            f.write(html)
        print(f"Report saved. Return: {result.total_return_pct}%, Win Rate: {result.win_rate}%, Sharpe: {result.sharpe_ratio}")
    asyncio.run(main())
