import React from 'react';
import { motion } from 'framer-motion';

const Ticker = () => {
    const items = [
        "BTC: $65,420 🚀", "ETH: $3,500 💎", "SOL: $145 🔥", "AI-AGENT-1: +450% 🤖", "WHALE-ALERT: 500 BTC MOVED 🚨"
    ];

    return (
        <div className="bg-neo-black text-neo-white py-2 overflow-hidden border-b-4 border-neo-black whitespace-nowrap">
            <motion.div
                className="flex gap-8 font-mono font-bold text-lg"
                animate={{ x: [0, -1000] }}
                transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
            >
                {[...items, ...items, ...items].map((item, i) => (
                    <span key={i} className="mx-4">{item}</span>
                ))}
            </motion.div>
        </div>
    );
};

export default Ticker;
