import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const CreatorStats = ({ data }) => {
    const chartData = [
        { day: 'Mon', plays: 120, revenue: 15 },
        { day: 'Tue', plays: 150, revenue: 22 },
        { day: 'Wed', plays: 98, revenue: 10 },
        { day: 'Thu', plays: 200, revenue: 45 },
        { day: 'Fri', plays: 250, revenue: 55 },
        { day: 'Sat', plays: 300, revenue: 80 },
        { day: 'Sun', plays: 180, revenue: 35 },
    ];

    return (
        <div className="glass-card p-6 h-80">
            <h2 className="text-[10px] font-black uppercase tracking-widest text-white/30 mb-6">Yield Performance (7D)</h2>
            <ResponsiveContainer width="100%" height="80%">
                <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                    <XAxis
                        dataKey="day"
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 10, fontWeight: 800 }}
                    />
                    <YAxis
                        yAxisId="left"
                        hide
                    />
                    <YAxis
                        yAxisId="right"
                        orientation="right"
                        hide
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#050505', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', fontSize: '10px' }}
                        itemStyle={{ color: '#10b981', fontWeight: 900 }}
                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                    />
                    <Bar
                        yAxisId="left"
                        dataKey="plays"
                        fill="rgba(16, 185, 129, 0.4)"
                        radius={[4, 4, 0, 0]}
                        name="Plays"
                    />
                    <Bar
                        yAxisId="right"
                        dataKey="revenue"
                        fill="#d946ef"
                        radius={[4, 4, 0, 0]}
                        name="Revenue ($)"
                    />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default CreatorStats;
