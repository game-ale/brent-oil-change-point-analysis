import { Activity, AlertTriangle, Calendar, TrendingDown, TrendingUp } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Area, AreaChart, CartesianGrid, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const App = () => {
    const [data, setData] = useState({ prices: [], events: [], results: {} });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [pricesRes, eventsRes, resultsRes] = await Promise.all([
                    fetch('http://localhost:5000/api/prices'),
                    fetch('http://localhost:5000/api/events'),
                    fetch('http://localhost:5000/api/results')
                ]);

                if (!pricesRes.ok || !eventsRes.ok) throw new Error("Failed to fetch data");

                const prices = await pricesRes.json();
                const events = await eventsRes.json();
                const results = await resultsRes.json();

                // Sampling data for performance if it's too large for the chart
                const sampledPrices = prices.filter((_, i) => i % 5 === 0);

                setData({ prices: sampledPrices, events, results });
            } catch (err) {
                console.error("Error fetching data:", err);
                setError("Make sure the backend is running at localhost:5000");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return (
        <div className="flex items-center justify-center min-h-screen text-white">
            <div className="animate-pulse flex flex-col items-center">
                <Activity className="w-12 h-12 text-sky-400 mb-4" />
                <p className="font-medium text-lg">Loading Analysis Data...</p>
            </div>
        </div>
    );

    if (error) return (
        <div className="flex items-center justify-center min-h-screen text-white p-4">
            <div className="glass-card p-8 text-center max-w-md">
                <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                <h2 className="text-xl font-bold mb-2">Backend Connection Error</h2>
                <p className="text-slate-400 mb-4">{error}</p>
                <div className="bg-slate-800 p-3 rounded text-sm font-mono text-left">
                    python dashboard/backend/app.py
                </div>
            </div>
        </div>
    );

    const changeDateFormatted = new Date(data.results.change_date).toLocaleDateString();
    const impactColor = data.results.price_change_pct < 0 ? 'text-rose-500' : 'text-emerald-500';

    return (
        <div className="p-4 md:p-8 max-w-7xl mx-auto min-h-screen text-slate-200">
            {/* Header */}
            <header className="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-4xl md:text-5xl font-bold mb-2 outfit text-gradient">Oil Insight Pro</h1>
                    <p className="text-slate-400 font-medium tracking-wide">BRENT CRUDE STRUCTURAL BREAK ANALYSIS</p>
                </div>
                <div className="flex items-center gap-2 bg-slate-800/50 px-4 py-2 rounded-full border border-slate-700 text-sm">
                    <Calendar className="w-4 h-4 text-sky-400" />
                    <span>1987 - 2020 Analysis Period</span>
                </div>
            </header>

            {/* Main Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="glass-card p-6 stat-card">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Detected Break</h3>
                        <Activity className="w-4 h-4 text-sky-400" />
                    </div>
                    <p className="text-3xl font-bold">{data.results.event_date || changeDateFormatted}</p>
                    <p className="text-sm text-slate-400 mt-1">Bayesian posterior mode</p>
                </div>

                <div className="glass-card p-6 stat-card">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Closest Event</h3>
                        <AlertTriangle className="w-4 h-4 text-amber-500" />
                    </div>
                    <p className="text-3xl font-bold truncate">{data.results.event_name || 'N/A'}</p>
                    <p className="text-sm text-slate-400 mt-1">{data.results.days_diff} days from break</p>
                </div>

                <div className="glass-card p-6 stat-card">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Price Impact</h3>
                        {data.results.price_change_pct < 0 ? <TrendingDown className="w-4 h-4 text-rose-500" /> : <TrendingUp className="w-4 h-4 text-emerald-500" />}
                    </div>
                    <p className={`text-3xl font-bold ${impactColor}`}>
                        {data.results.price_change_pct > 0 ? '+' : ''}{data.results.price_change_pct?.toFixed(2)}%
                    </p>
                    <p className="text-sm text-slate-400 mt-1">Mean shift magnitude</p>
                </div>
            </div>

            {/* Chart Section */}
            <div className="grid grid-cols-1 gap-8">
                <div className="glass-card p-6 md:p-8">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-bold">Historical Price Timeline</h2>
                        <div className="flex gap-4 text-xs font-semibold">
                            <div className="flex items-center gap-1"><div className="w-3 h-3 bg-sky-500 rounded-sm"></div> Price (USD)</div>
                            <div className="flex items-center gap-1"><div className="w-3 h-0.5 bg-rose-500"></div> Structural Break</div>
                        </div>
                    </div>

                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data.prices}>
                                <defs>
                                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                                <XAxis
                                    dataKey="Date"
                                    stroke="#64748b"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                    minTickGap={50}
                                />
                                <YAxis
                                    stroke="#64748b"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                    tickFormatter={(value) => `$${value}`}
                                />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                                    itemStyle={{ color: '#bae6fd' }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="Price"
                                    stroke="#0ea5e9"
                                    strokeWidth={2}
                                    fillOpacity={1}
                                    fill="url(#colorPrice)"
                                />

                                {/* Detected Break Line */}
                                {data.results.event_date && (
                                    <ReferenceLine
                                        x={data.prices.find(p => p.Date.includes(data.results.event_date))?.Date || data.results.event_date}
                                        stroke="#f43f5e"
                                        strokeWidth={2}
                                        strokeDasharray="5 5"
                                        label={{ position: 'top', value: 'Shift Detect', fill: '#f43f5e', fontSize: 10, fontWeight: 'bold' }}
                                    />
                                )}
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Narrative Section */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="glass-card p-8">
                        <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-sky-400">
                            <Activity className="w-5 h-5" />
                            Impact Narrative
                        </h2>
                        <p className="text-slate-300 leading-relaxed mb-4">
                            The Bayesian model identified a significant structural break on <span className="text-white font-semibold">{data.results.event_date}</span>.
                            This period correlates strongly with the <span className="text-white font-semibold">{data.results.event_name}</span>.
                        </p>
                        <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                            <p className="text-sm italic text-slate-400">"{data.results.description}"</p>
                        </div>
                    </div>

                    <div className="glass-card p-8">
                        <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-sky-400">
                            <Activity className="w-5 h-5" />
                            Statistical Inference
                        </h2>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                                <span className="text-slate-400">Mean Price Pre-Break</span>
                                <span className="font-mono text-white">${data.results.mu1?.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                                <span className="text-slate-400">Mean Price Post-Break</span>
                                <span className="font-mono text-white">${data.results.mu2?.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                                <span className="text-slate-400">Confidence Method</span>
                                <span className="text-sky-300 text-xs font-bold uppercase">MCMC Bayesian Switch</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <footer className="mt-12 mb-8 text-center text-slate-500 text-sm">
                <p>&copy; 2026 Birhan Energies Data Science Team. All rights reserved.</p>
                <p className="mt-1 text-slate-600">Model: Bayesian Discrete Switch Point with Normal Likelihood</p>
            </footer>
        </div>
    );
};

export default App;
