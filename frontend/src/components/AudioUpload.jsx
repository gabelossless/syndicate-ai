import React, { useState } from 'react';
import { Upload, Check } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const MediaUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [title, setTitle] = useState('');
    const [price, setPrice] = useState('0.00');
    const [mediaType, setMediaType] = useState('audio');
    const [loading, setLoading] = useState(false);

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('title', title);
            formData.append('price', price);
            formData.append('media_type', mediaType);

            await axios.post(`${API_URL}/api/media/upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            setTitle('');
            setPrice('0.00');
            setFile(null);
            setMediaType('audio');
            if (onUploadSuccess) onUploadSuccess();
            alert("SUCCESS: Published to Cloud Architecture!");
        } catch (error) {
            console.error("Upload failed", error);
            const msg = error.response?.data?.detail || "Upload failed!";
            alert(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card p-8">
            <h2 className="text-xl font-black mb-8 flex items-center gap-3">
                <Upload className="text-brand-secondary" />
                <span className="glow-text tracking-tighter uppercase">Forge New Asset</span>
            </h2>
            <form onSubmit={handleUpload} className="space-y-6">
                <div className="space-y-1">
                    <label className="text-[10px] uppercase font-black text-white/30 px-2 tracking-tighter">Asset Title</label>
                    <input
                        type="text"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        className="cyber-input"
                        placeholder="e.g. Neo-Tokyo Resonance"
                        required
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1">
                        <label className="text-[10px] uppercase font-black text-white/30 px-2 tracking-tighter">Yield Price ($)</label>
                        <input
                            type="number"
                            step="0.01"
                            value={price}
                            onChange={e => setPrice(e.target.value)}
                            className="cyber-input"
                            required
                        />
                    </div>
                    <div className="space-y-1">
                        <label className="text-[10px] uppercase font-black text-white/30 px-2 tracking-tighter">Engine Type</label>
                        <select
                            value={mediaType}
                            onChange={e => setMediaType(e.target.value)}
                            className="cyber-input bg-[#050505] appearance-none"
                        >
                            <option value="audio">Audio Node</option>
                            <option value="reel">Rapid Reel</option>
                            <option value="video">Full Vision</option>
                        </select>
                    </div>
                </div>

                <div className="border-2 border-dashed border-white/5 p-10 rounded-2xl text-center hover:bg-white/[0.02] hover:border-brand-secondary/40 cursor-pointer relative transition-all group">
                    <input
                        type="file"
                        accept="audio/*,video/mp4,video/webm"
                        onChange={e => setFile(e.target.files[0])}
                        className="absolute inset-0 opacity-0 cursor-pointer"
                    />
                    {file ? (
                        <div className="text-brand-secondary font-black flex flex-col items-center gap-2">
                            <Check className="p-2 bg-brand-secondary/20 rounded-full" size={40} />
                            <span className="text-xs truncate max-w-[200px]">{file.name}</span>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            <div className="text-white/20 font-black text-[10px] uppercase tracking-[0.2em] group-hover:text-white/40">Transmit Data</div>
                            <div className="text-[8px] text-white/10 uppercase font-bold tracking-widest">DRAG ASSET HERE</div>
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-4 rounded-xl font-black text-sm uppercase tracking-widest transition-all ${loading
                            ? 'bg-white/5 text-white/20'
                            : 'bg-brand-secondary text-black hover:shadow-[0_0_25px_rgba(217,70,239,0.4)] hover:scale-[1.02] active:scale-[0.98]'
                        }`}
                >
                    {loading ? 'Transmitting...' : 'Initiate Publish'}
                </button>
            </form>
        </div>
    );
};

export default MediaUpload;
