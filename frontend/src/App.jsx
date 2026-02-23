import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Ticker from './components/Ticker';
import StatsCard from './components/StatsCard';
import Leaderboard from './components/Leaderboard';
import CreatorDashboard from './components/CreatorDashboard';
import { Activity, DollarSign, Users, Zap, Headphones } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [view, setView] = useState('trader'); // 'trader' | 'creator'
  const [stats, setStats] = useState({
    total_volume: 0,
    active_syndicates: 0,
    top_roi: 0,
    users_delegated: 0
  });

  useEffect(() => {
    axios.get(`${API_URL}/api/stats`)
      .then(res => setStats(res.data))
      .catch(err => console.error("Failed to fetch stats", err));
  }, []);

  return (
    <div className="min-h-screen pb-20 selection:bg-brand-primary selection:text-black">
      <Header />
      <Ticker />

      {/* Navigation Switcher */}
      <div className="container mx-auto px-6 mt-8 flex gap-4">
        <button
          onClick={() => setView('trader')}
          className={`px-6 py-2 rounded-xl font-bold transition-all ${view === 'trader'
            ? 'bg-brand-primary text-black shadow-[0_0_20px_rgba(16,185,129,0.3)]'
            : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
            }`}
        >
          TRADER VIEW
        </button>
        <button
          onClick={() => setView('creator')}
          className={`px-6 py-2 rounded-xl font-bold flex items-center gap-2 transition-all ${view === 'creator'
            ? 'bg-brand-secondary text-black shadow-[0_0_20px_rgba(217,70,239,0.3)]'
            : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
            }`}
        >
          <Headphones size={18} /> CREATOR STUDIO
        </button>
      </div>

      <main className="container mx-auto p-6 space-y-12">
        {view === 'creator' ? (
          <CreatorDashboard />
        ) : (
          <>
            {/* KPI Section */}
            <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              <StatsCard
                label="Total Volume (24h)"
                value={`$${(stats.total_volume / 1000000).toFixed(2)}M`}
                trend={12.5}
                icon={DollarSign}
                color="emerald"
              />
              <StatsCard
                label="Active Syndicates"
                value={stats.active_syndicates}
                icon={Zap}
                color="blue"
              />
              <StatsCard
                label="Top ROI (30d)"
                value={`${stats.top_roi}%`}
                trend={2.4}
                icon={Activity}
                color="pink"
              />
              <StatsCard
                label="Users Delegated"
                value={stats.users_delegated}
                trend={5.8}
                icon={Users}
                color="yellow"
              />
            </section>

            {/* Main Content Split */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
              <div className="lg:col-span-2 space-y-10">
                <Leaderboard />

                {/* Recent Signals */}
                <div className="glass-card p-8">
                  <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    <Activity className="text-brand-primary" />
                    <span className="glow-text">Live AI Signals</span>
                  </h2>
                  <div className="space-y-4">
                    {[
                      { time: '10:42 AM', type: 'BUY', pair: 'BTC/USDT', conf: 92 },
                      { time: '10:38 AM', type: 'SELL', pair: 'SOL/USDT', conf: 78 },
                      { time: '10:15 AM', type: 'BUY', pair: 'ETH/USDT', conf: 85 },
                    ].map((sig, i) => (
                      <div key={i} className="flex justify-between items-center bg-white/5 p-4 rounded-xl border border-white/5">
                        <span className="font-mono text-xs text-white/40 uppercase tracking-widest">{sig.time}</span>
                        <span className={`font-black text-sm px-3 py-1 rounded-lg ${sig.type === 'BUY' ? 'bg-emerald-500/10 text-emerald-400' : 'text-pink-400 bg-pink-500/10'
                          }`}>
                          {sig.type}
                        </span>
                        <span className="font-bold text-white/90">{sig.pair}</span>
                        <span className="badge-emerald">
                          {sig.conf}% CONFIDENCE
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sidebar / Connect */}
              <div className="space-y-8">
                <div className="glass-card p-8 border-brand-primary/20 bg-gradient-to-b from-brand-primary/10 to-transparent">
                  <h3 className="text-2xl font-black mb-4 flex items-center gap-2">
                    <Zap className="text-brand-primary" fill="currentColor" />
                    START EARNING
                  </h3>
                  <p className="text-sm text-white/60 mb-6 leading-relaxed">
                    Delegate your high-frequency trades to <span className="text-brand-primary font-bold">The Whale Hunter</span> and secure automatic profit sharing.
                  </p>
                  <div className="space-y-4">
                    <div className="space-y-1">
                      <label className="text-[10px] uppercase font-bold text-white/40 px-2 tracking-tighter">API Access Key</label>
                      <input type="text" placeholder="Paste Key..." className="cyber-input" />
                    </div>
                    <div className="space-y-1">
                      <label className="text-[10px] uppercase font-bold text-white/40 px-2 tracking-tighter">Secret Token</label>
                      <input type="password" placeholder="••••••••••••" className="cyber-input" />
                    </div>
                    <button className="btn-primary w-full mt-4">
                      DELEGATE NOW
                    </button>
                  </div>
                </div>

                {/* Secondary Sidebar Widget */}
                <div className="glass-card p-6 bg-brand-secondary/5 border-brand-secondary/20">
                  <p className="text-xs text-brand-secondary font-bold uppercase mb-2">Network Status</p>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-brand-secondary animate-pulse shadow-[0_0_10px_#d946ef]" />
                    <span className="text-sm font-mono opacity-80 uppercase tracking-tighter">Node 2030-Alpha Active</span>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
