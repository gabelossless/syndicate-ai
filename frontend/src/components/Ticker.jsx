import React from 'react';
import { motion } from 'framer-motion';

const Ticker = () => {
    const items = [
        { label: "BTC", price: "$65,420", trend: "+2.4%", color: "text-brand-primary" },
        { label: "ETH", price: "$3,300", trend: "-1.2%", color: "text-pink-400" },
        { label: "SOL", price: "$145", trend: "+5.1%", color: "text-brand-primary" },
        { label: "AI-1", price: "92%", trend: "STABLE", color: "text-blue-400" },
        { label: "GAS", price: "24 Gwei", trend: "LOW", color: "text-yellow-400" }
    ];

    return (
        <div className="bg-brand-bg/40 border-b border-brand-border py-2 overflow-hidden whitespace-nowrap backdrop-blur-sm">
            <motion.div
                className="flex gap-12 font-mono"
                animate={{ x: [0, -1200] }}
                transition={{ repeat: Infinity, duration: 30, ease: "linear" }}
            >
                {[...items, ...items, ...items, ...items].map((item, i) => (
                    <div key={i} className="flex gap-3 items-baseline">
                        <span className="text-[10px] font-black text-white/30 tracking-widest">{item.label}</span>
                        <span className="text-sm font-bold text-white/90">{item.price}</span>
                        <span className={`text-[9px] font-black px-1.5 py-0.5 rounded ${item.color} bg-white/5`}>
                            {item.trend}
                        </span>
                    </div>
                ))}
            </motion.div>
        </div>
    );
};

export default Ticker;
