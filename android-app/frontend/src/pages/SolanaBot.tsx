import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, DollarSign, Activity, Play, Square, RefreshCw, AlertCircle } from 'lucide-react';
import { getSolanaStatus, startSolanaTrading, stopSolanaTrading, SolanaStatus } from '../services/gatewayApi';

export default function SolanaBot() {
  const [status, setStatus] = useState<SolanaStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  const fetchStatus = async () => {
    try {
      const data = await getSolanaStatus();
      setStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch status');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    setActionLoading(true);
    try {
      await startSolanaTrading();
      await fetchStatus();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start trading');
    } finally {
      setActionLoading(false);
    }
  };

  const handleStop = async () => {
    setActionLoading(true);
    try {
      await stopSolanaTrading();
      await fetchStatus();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to stop trading');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <RefreshCw className="animate-spin text-primary-500" size={48} />
      </div>
    );
  }

  const isTrading = status?.isTrading || false;
  const backtestMode = status?.config?.backtestMode !== false;

  return (
    <div className="flex flex-col h-full bg-slate-950 overflow-y-auto">
      {/* Header */}
      <div className="bg-slate-900 border-b border-slate-800 p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <TrendingUp className="text-primary-500" size={28} />
            <div>
              <h1 className="text-xl font-bold">Solana Trading Bot</h1>
              <p className="text-sm text-slate-400">
                {backtestMode ? '🧪 Backtest Mode' : '🟢 Live Mode'}
              </p>
            </div>
          </div>
          <button
            onClick={fetchStatus}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
            disabled={actionLoading}
          >
            <RefreshCw size={20} className={actionLoading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-900/30 border-l-4 border-red-500 p-4 m-4 flex items-start gap-3">
          <AlertCircle className="text-red-500 flex-shrink-0 mt-0.5" size={20} />
          <div>
            <p className="font-semibold text-red-200">Error</p>
            <p className="text-sm text-red-300">{error}</p>
          </div>
        </div>
      )}

      <div className="p-4 space-y-4">
        {/* Control Panel */}
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity size={20} className="text-primary-500" />
            Control Panel
          </h2>
          <div className="flex gap-3">
            <button
              onClick={handleStart}
              disabled={isTrading || actionLoading}
              className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
            >
              <Play size={18} />
              Start Trading
            </button>
            <button
              onClick={handleStop}
              disabled={!isTrading || actionLoading}
              className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
            >
              <Square size={18} />
              Stop Trading
            </button>
          </div>
          <div className="mt-3 text-center">
            <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${
              isTrading ? 'bg-green-900/50 text-green-300' : 'bg-slate-800 text-slate-400'
            }`}>
              <span className={`w-2 h-2 rounded-full ${isTrading ? 'bg-green-500 animate-pulse' : 'bg-slate-600'}`} />
              {isTrading ? 'Trading Active' : 'Trading Stopped'}
            </span>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 gap-4">
          <StatCard
            icon={<DollarSign className="text-blue-400" />}
            label="Daily P&L"
            value={status?.dailyPnL !== undefined ? `$${status.dailyPnL.toFixed(2)}` : 'N/A'}
            positive={status?.dailyPnL !== undefined && status.dailyPnL > 0}
          />
          <StatCard
            icon={<TrendingUp className="text-green-400" />}
            label="Total P&L"
            value={status?.totalPnL !== undefined ? `$${status.totalPnL.toFixed(2)}` : 'N/A'}
            positive={status?.totalPnL !== undefined && status.totalPnL > 0}
          />
          <StatCard
            icon={<Activity className="text-purple-400" />}
            label="Win Rate"
            value={status?.stats?.winRate !== undefined ? `${(status.stats.winRate * 100).toFixed(1)}%` : 'N/A'}
          />
          <StatCard
            icon={<TrendingDown className="text-red-400" />}
            label="Max Drawdown"
            value={status?.stats?.maxDrawdown !== undefined ? `${(status.stats.maxDrawdown * 100).toFixed(1)}%` : 'N/A'}
          />
        </div>

        {/* Wallet Balance */}
        {status?.wallet && (
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <h2 className="text-lg font-semibold mb-3">Wallet Balance</h2>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">SOL</span>
                <span className="font-mono font-semibold">{status.wallet.solBalance.toFixed(4)}</span>
              </div>
              {Object.entries(status.wallet.tokenBalances || {}).map(([token, balance]) => (
                <div key={token} className="flex justify-between items-center">
                  <span className="text-slate-400 text-sm">{token}</span>
                  <span className="font-mono text-sm">{typeof balance === 'number' ? balance.toFixed(4) : balance}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recent Trades */}
        {status?.tradeHistory && status.tradeHistory.length > 0 && (
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <h2 className="text-lg font-semibold mb-3">Recent Trades</h2>
            <div className="space-y-2">
              {status.tradeHistory.slice(0, 5).map((trade, i) => (
                <div key={i} className="flex justify-between items-center py-2 border-b border-slate-800 last:border-0">
                  <span className="text-sm text-slate-400">Trade #{i + 1}</span>
                  <span className={`text-sm font-semibold ${
                    trade.pnl > 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {trade.pnl > 0 ? '+' : ''}{trade.pnl?.toFixed(2) || 'N/A'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  positive?: boolean;
}

function StatCard({ icon, label, value, positive }: StatCardProps) {
  return (
    <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
      <div className="flex items-center gap-2 mb-2">
        {icon}
        <span className="text-sm text-slate-400">{label}</span>
      </div>
      <div className={`text-2xl font-bold ${
        positive !== undefined
          ? positive
            ? 'text-green-400'
            : 'text-red-400'
          : 'text-white'
      }`}>
        {value}
      </div>
    </div>
  );
}
