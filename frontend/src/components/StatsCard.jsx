import React from 'react';
import { motion } from 'framer-motion';

const StatsCard = ({ label, value, trend, icon: Icon, color }) => {
    const colorTable = {
        emerald: 'text-emerald-400',
        pink: 'text-pink-400',
        blue: 'text-blue-400',
        yellow: 'text-yellow-400'
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -5 }}
            className="stat-card group"
        >
            <div className="flex justify-between items-start mb-4">
                <span className="text-[10px] uppercase font-black tracking-widest text-white/40">
                    {label}
                </span>
                <div className={`p-2 rounded-lg bg-white/5 group-hover:bg-white/10 transition-colors ${colorTable[color] || 'text-brand-primary'}`}>
                    {Icon && <Icon size={18} />}
                </div>
            </div>

            <div className="flex items-end justify-between">
                <div className="text-3xl font-black font-sans tracking-tight text-white/90">
                    {value}
                </div>
                {trend && (
                    <div className={`text-[10px] font-black px-2 py-0.5 rounded-full ${trend > 0 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-pink-500/10 text-pink-400'
                        }`}>
                        {trend > 0 ? '+' : ''}{trend}%
                    </div>
                )}
            </div>

            <div className="mt-4 h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '70%' }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                    className={`h-full ${colorTable[color] || 'bg-brand-primary'} opacity-50`}
                />
            </div>
        </motion.div>
    );
};

export default StatsCard;
