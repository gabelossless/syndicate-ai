import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const CreatorStats = ({ data }) => {
    // Mock daily data for the chart (since MVP backend only sends totals)
    // In a real app, we'd fetch specific time-series data from /api/stats/history
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
        <div className="neo-card h-80">
            <h2 className="text-xl mb-4 font-black">PERFORMANCE (7D)</h2>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis dataKey="day" style={{ fontFamily: 'Space Mono', fontSize: '12px' }} />
                    <YAxis yAxisId="left" orientation="left" stroke="#000" />
                    <YAxis yAxisId="right" orientation="right" stroke="#00d084" />
                    <Tooltip
                        contentStyle={{ border: '2px solid black', boxShadow: '4px 4px 0px 0px black' }}
                        cursor={{ fill: '#f0f0f0' }}
                    />
                    <Bar yAxisId="left" dataKey="plays" fill="#000" name="Plays" />
                    <Bar yAxisId="right" dataKey="revenue" fill="#00ff9d" name="Revenue ($)" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default CreatorStats;
