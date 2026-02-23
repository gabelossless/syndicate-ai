import React, { useState, useEffect } from 'react';
import StatsCard from './StatsCard';
import CreatorStats from './CreatorStats';
import AudioUpload from './AudioUpload';
import { Music, DollarSign, PlayCircle, Trash2 } from 'lucide-react';
import axios from 'axios';

const CreatorDashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchDashboard = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/creator/dashboard');
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
            await axios.delete(`http://localhost:8000/api/media/${id}`);
            fetchDashboard(); // Refresh
        } catch (err) {
            alert("Failed to delete");
        }
    };

    if (loading) return <div className="font-mono p-10 text-center">LOADING STUDIO...</div>;

    return (
        <div className="space-y-8">
            {/* Top Stats */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatsCard
                    label="Total Revenue"
                    value={`$${data?.summary.total_revenue.toFixed(2)}`}
                    icon={DollarSign}
                />
                <StatsCard
                    label="Total Plays"
                    value={data?.summary.total_plays}
                    icon={PlayCircle}
                />
                <StatsCard
                    label="Tracks Uploaded"
                    value={data?.summary.total_tracks}
                    icon={Music}
                />
            </section>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Content: Chart & Track List */}
                <div className="lg:col-span-2 space-y-8">
                    <CreatorStats />

                    <div className="neo-card">
                        <h2 className="text-xl mb-4 font-black flex items-center gap-2">
                            <Music /> YOUR LIBRARY
                        </h2>
                        <div className="space-y-4">
                            {data?.tracks.map((track) => (
                                <div key={track.id} className="flex justify-between items-center border-b-2 border-neo-black pb-4">
                                    <div>
                                        <h3 className="font-bold text-lg">{track.title}</h3>
                                        <div className="text-xs font-mono opacity-60">ID: {track.id} • ${track.price}</div>
                                    </div>
                                    <div className="flex items-center gap-6">
                                        <div className="text-right">
                                            <span className="block font-bold">{track.plays} plays</span>
                                            <span className="block text-sm text-green-600">${track.revenue.toFixed(2)}</span>
                                        </div>
                                        <button
                                            onClick={() => handleDelete(track.id)}
                                            className="p-2 bg-red-100 hover:bg-red-500 hover:text-white border-2 border-black transition-colors"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                            {data?.tracks.length === 0 && (
                                <div className="text-center opacity-50 font-mono py-10">NO TRACKS FOUND</div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Sidebar: Upload */}
                <div>
                    <AudioUpload onUploadSuccess={fetchDashboard} />
                </div>
            </div>
        </div>
    );
};

export default CreatorDashboard;
