import React, { useState, useEffect } from 'react';
import StatsCard from './StatsCard';
import CreatorStats from './CreatorStats';
import AudioUpload from './AudioUpload';
import { Music, DollarSign, PlayCircle, Trash2 } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const CreatorDashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchDashboard = async () => {
        try {
            const res = await axios.get(`${API_URL}/api/creator/dashboard`);
            setData(res.data);
        } catch (err) {
            console.error("Failed to fetch dashboard", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboard();
    }, []);

    const handleDelete = async (id) => {
        if (!window.confirm("Delete this track?")) return;
        try {
            await axios.delete(`${API_URL}/api/media/${id}`);
            fetchDashboard(); // Refresh
        } catch (err) {
            alert("Failed to delete");
        }
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center p-20 space-y-4">
            <div className="w-12 h-12 border-4 border-brand-primary/20 border-t-brand-primary rounded-full animate-spin" />
            <div className="font-mono text-xs uppercase tracking-widest text-white/40">Syncing Studio Data...</div>
        </div>
    );

    return (
        <div className="space-y-12">
            {/* Top Stats */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <StatsCard
                    label="Total Revenue"
                    value={`$${data?.summary.total_revenue.toFixed(2)}`}
                    icon={DollarSign}
                    color="emerald"
                />
                <StatsCard
                    label="Total Plays"
                    value={data?.summary.total_plays}
                    icon={PlayCircle}
                    color="pink"
                />
                <StatsCard
                    label="Tracks Uploaded"
                    value={data?.summary.total_tracks}
                    icon={Music}
                    color="blue"
                />
            </section>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                {/* Main Content: Chart & Track List */}
                <div className="lg:col-span-2 space-y-10">
                    <CreatorStats />

                    <div className="glass-card p-8">
                        <h2 className="text-2xl font-black mb-8 flex items-center gap-3">
                            <Music className="text-brand-primary" />
                            <span className="glow-text tracking-tighter uppercase">Media Library</span>
                        </h2>
                        <div className="space-y-6">
                            {data?.tracks.map((track) => (
                                <div key={track.id} className="flex justify-between items-center bg-white/[0.02] p-6 rounded-2xl border border-white/5 hover:border-white/10 transition-all group">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 bg-brand-primary/10 rounded-xl flex items-center justify-center text-brand-primary group-hover:bg-brand-primary group-hover:text-black transition-all">
                                            <Music size={24} />
                                        </div>
                                        <div>
                                            <h3 className="font-bold text-lg text-white/90">{track.title}</h3>
                                            <div className="text-[10px] font-mono uppercase tracking-widest text-white/30">
                                                ID: {track.id} • <span className="text-brand-primary/60">{track.media_type}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-8">
                                        <div className="text-right">
                                            <span className="block font-black text-white/90">{track.plays} PLAYS</span>
                                            <span className="block text-xs font-mono text-emerald-400 font-bold">${track.revenue.toFixed(2)} YIELD</span>
                                        </div>
                                        <button
                                            onClick={() => handleDelete(track.id)}
                                            className="p-3 bg-white/5 hover:bg-pink-500/20 text-white/40 hover:text-pink-400 rounded-xl transition-all border border-transparent hover:border-pink-500/30"
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                            {data?.tracks.length === 0 && (
                                <div className="text-center py-20 bg-white/[0.02] rounded-3xl border border-dashed border-white/10">
                                    <Music className="mx-auto text-white/10 mb-4" size={48} />
                                    <div className="text-xs uppercase tracking-[0.2em] text-white/20 font-black">Architecture Empty</div>
                                    <p className="text-[10px] text-white/10 mt-1">Upload your first asset to begin tracking</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Sidebar: Upload */}
                <div className="space-y-8">
                    <AudioUpload onUploadSuccess={fetchDashboard} />

                    <div className="glass-card p-6 border-brand-primary/10">
                        <h4 className="text-[10px] font-black uppercase tracking-widest text-white/30 mb-4 text-center">Creator Compliance</h4>
                        <ul className="space-y-3 text-[10px] font-bold text-white/50">
                            <li className="flex items-center gap-2">
                                <div className="w-1 h-1 bg-brand-primary rounded-full" />
                                Audio: Max 100MB (WAV/MP3)
                            </li>
                            <li className="flex items-center gap-2">
                                <div className="w-1 h-1 bg-brand-primary rounded-full" />
                                Reels: Max 15 Seconds
                            </li>
                            <li className="flex items-center gap-2">
                                <div className="w-1 h-1 bg-brand-primary rounded-full" />
                                Video: 4K Support Active
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CreatorDashboard;
