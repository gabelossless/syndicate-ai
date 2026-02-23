import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Ticker from './components/Ticker';
import StatsCard from './components/StatsCard';
import Leaderboard from './components/Leaderboard';
import CreatorDashboard from './components/CreatorDashboard';
import { Activity, DollarSign, Users, Zap, Headphones } from 'lucide-react';
import axios from 'axios';

function App() {
  const [view, setView] = useState('trader'); // 'trader' | 'creator'
  const [stats, setStats] = useState({
    total_volume: 1250000,
    active_syndicates: 12,
    top_roi: 45.2,
    users_delegated: 843
  });

  useEffect(() => {
    axios.get('http://localhost:8000/api/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error("Failed to fetch stats", err));
  }, []);

  return (
    <div className="min-h-screen bg-dots-pattern pb-20">
      <Header />
      <Ticker />

      {/* Navigation Switcher */}
      <div className="container mx-auto px-6 mt-6 flex gap-4">
        <button
          onClick={() => setView('trader')}
          className={`neo-btn ${view === 'trader' ? 'bg-neo-black text-neo-white' : 'bg-white text-neo-black'}`}
        >
          TRADER VIEW
        </button>
        <button
          onClick={() => setView('creator')}
          className={`neo-btn flex items-center gap-2 ${view === 'creator' ? 'bg-neo-pink text-neo-black' : 'bg-white text-neo-black'}`}
        >
          <Headphones size={20} /> CREATOR STUDIO
        </button>
      </div>

      <main className="container mx-auto p-6 space-y-8">
        {view === 'creator' ? (
          <CreatorDashboard />
        ) : (
          <>
            {/* KPI Section */}
            <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatsCard
                label="Total Volume (24h)"
                value={`$${(stats.total_volume / 1000000).toFixed(2)}M`}
                trend={12.5}
                icon={DollarSign}
              />
              <StatsCard
                label="Active Syndicates"
                value={stats.active_syndicates}
                icon={Zap}
              />
              <StatsCard
                label="Top ROI (30d)"
                value={`${stats.top_roi}%`}
                trend={2.4}
                icon={Activity}
              />
              <StatsCard
                label="Users Delegated"
                value={stats.users_delegated}
                trend={5.8}
                icon={Users}
              />
            </section>

            {/* Main Content Split */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-8">
                <Leaderboard />

                {/* Recent Signals (Placeholder for Chart) */}
                <div className="neo-card">
                  <h2 className="text-xl mb-4 flex items-center gap-2">
                    <Activity /> Live AI Signals
                  </h2>
                  <div className="space-y-4">
                    {[
                      { time: '10:42 AM', type: 'BUY', pair: 'BTC/USDT', conf: 92 },
                      { time: '10:38 AM', type: 'SELL', pair: 'SOL/USDT', conf: 78 },
                      { time: '10:15 AM', type: 'BUY', pair: 'ETH/USDT', conf: 85 },
                    ].map((sig, i) => (
                      <div key={i} className="flex justify-between items-center border-b-2 border-dashed border-gray-300 pb-2">
                        <span className="font-mono text-sm opacity-60">{sig.time}</span>
                        <span className={`font-bold ${sig.type === 'BUY' ? 'text-green-600' : 'text-red-600'}`}>
                          {sig.type}
                        </span>
                        <span className="font-mono">{sig.pair}</span>
                        <span className="bg-neo-black text-neo-white text-xs px-2 py-1 rounded-sm">
                          {sig.conf}% CONFIDENCE
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sidebar / Connect */}
              <div className="space-y-6">
                <div className="neo-card bg-neo-yellow">
                  <h3 className="text-xl font-black mb-2">🚀 START EARNING</h3>
                  <p className="text-sm border-b-2 border-black pb-4 mb-4">
                    Delegate your trades to "The Whale Hunter" today.
                  </p>
                  <div className="space-y-3">
                    <input type="text" placeholder="API Key" className="neo-input bg-white" />
                    <input type="password" placeholder="Secret" className="neo-input bg-white" />
                    <button className="neo-btn w-full bg-neo-black text-neo-green hover:text-neo-pink">
                      DELEGATE NOW
                    </button>
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
