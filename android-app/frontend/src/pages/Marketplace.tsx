import { useState, useEffect } from 'react';
import { Package, Download, Star, Tag, Search, RefreshCw, AlertCircle } from 'lucide-react';
import { getMarketplaceRegistry, MarketplaceAgent } from '../services/gatewayApi';

export default function Marketplace() {
  const [agents, setAgents] = useState<MarketplaceAgent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchMarketplace = async () => {
    setLoading(true);
    try {
      const data = await getMarketplaceRegistry();
      setAgents(data.agents || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load marketplace');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMarketplace();
  }, []);

  const filteredAgents = agents.filter(agent =>
    agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    agent.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (agent.tags && agent.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase())))
  );

  return (
    <div className="flex flex-col h-full bg-slate-950">
      {/* Header */}
      <div className="bg-slate-900 border-b border-slate-800 p-4 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Package className="text-primary-500" size={28} />
            <div>
              <h1 className="text-xl font-bold">Agent Marketplace</h1>
              <p className="text-sm text-slate-400">
                {agents.length} agents beschikbaar
              </p>
            </div>
          </div>
          <button
            onClick={fetchMarketplace}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
          <input
            type="text"
            placeholder="Zoek agents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-800 text-white rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 placeholder-slate-500"
          />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {error && (
          <div className="bg-red-900/30 border-l-4 border-red-500 p-4 mb-4 flex items-start gap-3 rounded">
            <AlertCircle className="text-red-500 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <p className="font-semibold text-red-200">Error</p>
              <p className="text-sm text-red-300">{error}</p>
            </div>
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="animate-spin text-primary-500" size={48} />
          </div>
        ) : filteredAgents.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-slate-500">
            <Package size={64} className="mb-4 opacity-50" />
            <p className="text-center">
              {searchQuery ? 'Geen agents gevonden' : 'Marketplace is leeg'}
            </p>
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="mt-4 text-primary-500 hover:text-primary-400"
              >
                Clear search
              </button>
            )}
          </div>
        ) : (
          <div className="grid gap-4">
            {filteredAgents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

interface AgentCardProps {
  agent: MarketplaceAgent;
}

function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-slate-700 transition-colors">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-1">{agent.name}</h3>
          <p className="text-sm text-slate-400 line-clamp-2">{agent.description}</p>
        </div>
        {agent.verified && (
          <span className="ml-2 bg-blue-900/50 text-blue-300 text-xs px-2 py-1 rounded-full flex-shrink-0">
            ✓ Verified
          </span>
        )}
      </div>

      {/* Tags */}
      {agent.tags && agent.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {agent.tags.slice(0, 3).map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center gap-1 bg-slate-800 text-slate-300 text-xs px-2 py-1 rounded"
            >
              <Tag size={12} />
              {tag}
            </span>
          ))}
          {agent.tags.length > 3 && (
            <span className="text-xs text-slate-500">
              +{agent.tags.length - 3} more
            </span>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-slate-800">
        <div className="flex items-center gap-4 text-sm text-slate-400">
          {agent.rating !== undefined && (
            <span className="flex items-center gap-1">
              <Star size={14} className="text-yellow-500 fill-yellow-500" />
              {agent.rating.toFixed(1)}
            </span>
          )}
          {agent.downloads !== undefined && (
            <span className="flex items-center gap-1">
              <Download size={14} />
              {agent.downloads}
            </span>
          )}
          {agent.author && (
            <span className="text-xs">
              by <span className="text-primary-400">{agent.author}</span>
            </span>
          )}
        </div>
        <button className="bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors duration-200">
          Install
        </button>
      </div>
    </div>
  );
}
