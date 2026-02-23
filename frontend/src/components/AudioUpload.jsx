import React, { useState } from 'react';
import { Upload, Check } from 'lucide-react';
import axios from 'axios';

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
            // 1. Simulate EIP-712 / personal_sign (Costs 0$ gas)
            const message = `Sign this message to prove you own the media: ${title} at ${new Date().toISOString()}`;
            console.log("Requesting signature for:", message);

            // Mock signature (In a real app, this would be window.ethereum.request)
            const mockSignature = "0x4ed2...fake_signature";
            const mockAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";

            // 2. Verify signature on backend
            // In a real dev environment, this would hit the API we just created
            // await axios.post('http://localhost:8000/api/auth/verify', {
            //     address: mockAddress,
            //     signature: mockSignature,
            //     message: message
            // });

            // 3. Upload Media
            const formData = new FormData();
            formData.append('file', file);
            formData.append('title', title);
            formData.append('price', price);
            formData.append('media_type', mediaType);

            await axios.post('http://localhost:8000/api/media/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            setTitle('');
            setPrice('0.00');
            setFile(null);
            setMediaType('audio');
            if (onUploadSuccess) onUploadSuccess();
            alert("SUCCESS: Media verified on-chain & published!");
        } catch (error) {
            console.error("Upload/Auth failed", error);
            const msg = error.response?.data?.detail || "Auth/Upload failed!";
            alert(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="neo-card">
            <h2 className="text-xl mb-4 flex items-center gap-2 font-black uppercase">
                <Upload /> UPLOAD MEDIA
            </h2>
            <form onSubmit={handleUpload} className="space-y-4">
                <div>
                    <label className="block font-mono text-sm mb-1">Title</label>
                    <input
                        type="text"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        className="neo-input"
                        placeholder="e.g. Cyberpunk Vibes"
                        required
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block font-mono text-sm mb-1">Price ($)</label>
                        <input
                            type="number"
                            step="0.01"
                            value={price}
                            onChange={e => setPrice(e.target.value)}
                            className="neo-input"
                            required
                        />
                    </div>
                    <div>
                        <label className="block font-mono text-sm mb-1">Type</label>
                        <select
                            value={mediaType}
                            onChange={e => setMediaType(e.target.value)}
                            className="neo-input uppercase"
                        >
                            <option value="audio">Audio</option>
                            <option value="reel">Reel (15s Max)</option>
                            <option value="video">Video (20m Max)</option>
                        </select>
                    </div>
                </div>

                <div className="border-2 border-dashed border-neo-black p-6 text-center hover:bg-gray-50 cursor-pointer relative">
                    <input
                        type="file"
                        accept="audio/*,video/mp4,video/webm"
                        onChange={e => setFile(e.target.files[0])}
                        className="absolute inset-0 opacity-0 cursor-pointer"
                    />
                    {file ? (
                        <div className="text-green-600 font-bold flex items-center justify-center gap-2">
                            <Check size={20} /> <span className="truncate max-w-[200px]">{file.name}</span>
                        </div>
                    ) : (
                        <span className="text-gray-500 font-mono">DRAG & DROP MEDIA</span>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={`neo-btn w-full bg-neo-pink text-neo-black ${loading ? 'opacity-50' : ''}`}
                >
                    {loading ? 'UPLOADING...' : 'PUBLISH'}
                </button>
            </form>
        </div>
    );
};

export default MediaUpload;
