import React, { useEffect, useState } from 'react';
import { Trophy, TrendingUp, Activity } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Leaderboard = () => {
    const [syndicates, setSyndicates] = useState([]);

    useEffect(() => {
        axios.get(`${API_URL}/api/leaderboard`)
            .then(res => setSyndicates(res.data))
            .catch(err => console.error("Failed to fetch leaderboard", err));
    }, []);

    return (
        <div className="glass-card overflow-hidden">
            <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
                <h2 className="text-2xl font-black flex items-center gap-3">
                    <Trophy className="text-brand-primary" fill="currentColor" size={28} />
                    <span className="glow-text tracking-tighter uppercase">Syndicate Leaderboard</span>
                </h2>
                <div className="badge-emerald animate-pulse">
                    Live Engine Data
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left">
                    <thead>
                        <tr className="bg-white/[0.02] text-[10px] uppercase font-black tracking-widest text-white/40">
                            <th className="px-6 py-4">Rank</th>
                            <th className="px-6 py-4">Agent Identifier</th>
                            <th className="px-6 py-4 text-center">ROI (30d)</th>
                            <th className="px-6 py-4">Success Rate</th>
                            <th className="px-6 py-4 text-right">Volume</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {syndicates.map((syn, i) => (
                            <tr key={syn.rank} className="hover:bg-white/[0.03] transition-colors group">
                                <td className="px-6 py-4">
                                    <span className={`flex items-center justify-center w-8 h-8 rounded-lg font-black ${i === 0 ? 'bg-brand-primary text-black' : 'bg-white/5 text-white/60'
                                        }`}>
                                        {syn.rank}
                                    </span>
                                </td>
                                <td className="px-6 py-4 font-bold text-white/90 group-hover:text-brand-primary transition-colors">
                                    {syn.name}
                                </td>
                                <td className={`px-6 py-4 text-center font-mono font-black ${syn.roi > 0 ? 'text-brand-primary' : 'text-pink-400'}`}>
                                    {syn.roi > 0 ? '+' : ''}{syn.roi}%
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3 min-w-[120px]">
                                        <div className="flex-1 bg-white/5 h-1 rounded-full overflow-hidden">
                                            <div
                                                className="bg-brand-primary h-full shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                                                style={{ width: `${syn.win_rate}%` }}
                                            />
                                        </div>
                                        <span className="text-xs font-mono opacity-60">{syn.win_rate}%</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-right font-mono text-xs text-white/40">
                                    ${(syn.volume / 1000).toFixed(0)}K
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Leaderboard;
