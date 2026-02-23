import React, { useEffect, useState } from 'react';
import { Trophy, TrendingUp, Activity } from 'lucide-react';
import axios from 'axios';

const Leaderboard = () => {
    const [syndicates, setSyndicates] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/leaderboard')
            .then(res => setSyndicates(res.data))
            .catch(err => console.error("Failed to fetch leaderboard", err));
    }, []);

    return (
        <div className="neo-card p-0 overflow-hidden">
            <div className="bg-neo-black text-neo-white p-4 border-b-4 border-neo-black flex justify-between items-center">
                <h2 className="text-2xl flex items-center gap-2">
                    <Trophy className="text-neo-yellow" /> Syndicate Leaderboard
                </h2>
                <div className="text-xs font-mono bg-neo-pink text-neo-black px-2 py-1 transform -rotate-2">
                    LIVE RANKING
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b-4 border-neo-black bg-gray-100 font-mono text-sm uppercase">
                            <th className="p-4 border-r-2 border-neo-black">Rank</th>
                            <th className="p-4 border-r-2 border-neo-black">Syndicate Name</th>
                            <th className="p-4 border-r-2 border-neo-black">ROI (30d)</th>
                            <th className="p-4 border-r-2 border-neo-black">Win Rate</th>
                            <th className="p-4">Volume</th>
                        </tr>
                    </thead>
                    <tbody>
                        {syndicates.map((syn) => (
                            <tr key={syn.rank} className="border-b-2 border-neo-black hover:bg-neo-green/20 transition-colors font-bold">
                                <td className="p-4 border-r-2 border-neo-black text-center text-xl">
                                    {syn.rank === 1 ? '👑' : `#${syn.rank}`}
                                </td>
                                <td className="p-4 border-r-2 border-neo-black">{syn.name}</td>
                                <td className={`p-4 border-r-2 border-neo-black ${syn.roi > 0 ? 'text-green-600' : 'text-red-600'}`}>
                                    {syn.roi > 0 ? '+' : ''}{syn.roi}%
                                </td>
                                <td className="p-4 border-r-2 border-neo-black">
                                    <div className="flex items-center gap-2">
                                        <div className="w-full bg-gray-300 h-2 border border-black rounded-full overflow-hidden">
                                            <div className="bg-neo-black h-full" style={{ width: `${syn.win_rate}%` }}></div>
                                        </div>
                                        {syn.win_rate}%
                                    </div>
                                </td>
                                <td className="p-4 font-mono">{syn.volume}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Leaderboard;
