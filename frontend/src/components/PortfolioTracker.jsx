import { useState, useEffect } from 'react';
import { TrendingUp, Coins, BarChart3, RefreshCw } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function StatBox({ label, value, color = 'emerald' }) {
    const colors = {
        emerald: 'text-emerald-400',
        blue: 'text-blue-400',
        purple: 'text-purple-400',
        yellow: 'text-yellow-400',
    };
    return (
        <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold tracking-widest opacity-40">{label}</span>
            <span className={`text-xl font-black ${colors[color] || colors.emerald} tabular-nums`}>{value}</span>
        </div>
    );
}

export default function PortfolioTracker() {
    const [portfolio, setPortfolio] = useState(null);
    const [loading, setLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState(null);

    const fetchPortfolio = async () => {
        try {
            const res = await fetch(`${API_URL}/api/portfolio`);
            if (!res.ok) throw new Error('Failed');
            const data = await res.json();
            setPortfolio(data);
            setLastUpdated(new Date().toLocaleTimeString());
        } catch (err) {
            console.error('Portfolio fetch failed:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPortfolio();
        const interval = setInterval(fetchPortfolio, 30000); // Refresh every 30s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="glass-card p-6 space-y-5">
            {/* Header */}
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-black flex items-center gap-2">
                    <BarChart3 className="text-brand-primary" size={20} />
                    <span className="glow-text">Live Portfolio</span>
                </h3>
                <button
                    onClick={fetchPortfolio}
                    className="text-white/30 hover:text-brand-primary transition-colors"
                    title="Refresh"
                >
                    <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
                </button>
            </div>

            {loading ? (
                <div className="space-y-3 animate-pulse">
                    {[1, 2, 3].map(i => (
                        <div key={i} className="h-8 bg-white/5 rounded-lg" />
                    ))}
                </div>
            ) : portfolio ? (
                <>
                    {/* Total Value */}
                    <div className="bg-gradient-to-r from-brand-primary/10 to-transparent rounded-xl p-4 border border-brand-primary/20">
                        <p className="text-[10px] uppercase tracking-widest opacity-40 mb-1">Total Estimated Value</p>
                        <p className="text-3xl font-black text-brand-primary">
                            ${(portfolio.total_usd_estimate ?? 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
                        </p>
                    </div>

                    {/* CEX Balances */}
                    <div className="space-y-2">
                        <p className="text-[10px] uppercase tracking-widest opacity-30 flex items-center gap-1">
                            <Coins size={10} /> CEX (Binance)
                        </p>
                        <div className="grid grid-cols-3 gap-2 bg-white/5 rounded-xl p-3">
                            <StatBox label="USDT" value={`$${(portfolio.cex?.USDT ?? 0).toLocaleString()}`} color="emerald" />
                            <StatBox label="BTC" value={portfolio.cex?.BTC ?? '0'} color="yellow" />
                            <StatBox label="ETH" value={portfolio.cex?.ETH ?? '0'} color="blue" />
                        </div>
                    </div>

                    {/* Solana Balances */}
                    <div className="space-y-2">
                        <p className="text-[10px] uppercase tracking-widest opacity-30 flex items-center gap-1">
                            <TrendingUp size={10} /> Solana On-Chain
                        </p>
                        <div className="grid grid-cols-2 gap-2 bg-white/5 rounded-xl p-3">
                            <StatBox label="SOL" value={portfolio.solana?.SOL ?? '0'} color="purple" />
                            <StatBox label="≈ USD" value={`$${(portfolio.solana?.SOL_USD ?? 0).toLocaleString()}`} color="purple" />
                        </div>
                    </div>

                    {lastUpdated && (
                        <p className="text-[10px] opacity-20 text-right">Updated {lastUpdated}</p>
                    )}
                </>
            ) : (
                <p className="text-sm opacity-40 text-center py-4">Portfolio data unavailable.</p>
            )}
        </div>
    );
}
