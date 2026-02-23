import React from 'react';
import { motion } from 'framer-motion';

const StatsCard = ({ label, value, trend, icon: Icon }) => {
    return (
        <motion.div
            whileHover={{ translate: "4px 4px", boxShadow: "0px 0px 0px 0px #000" }}
            className="neo-card flex flex-col justify-between h-40"
        >
            <div className="flex justify-between items-start">
                <h3 className="text-sm font-bold opacity-70">{label}</h3>
                {Icon && <Icon className="text-neo-black opacity-50" size={24} />}
            </div>

            <div>
                <div className="text-4xl font-black font-sans tracking-tighter">{value}</div>
                {trend && (
                    <div className={`text-sm font-bold ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {trend > 0 ? '▲' : '▼'} {Math.abs(trend)}%
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default StatsCard;
