import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Server, Info, ExternalLink, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { getHealth, getServicesStatus, HealthStatus } from '../services/gatewayApi';

export default function Settings() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [servicesStatus, setServicesStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchStatus = async () => {
    setLoading(true);
    try {
      const [healthData, servicesData] = await Promise.all([
        getHealth(),
        getServicesStatus(),
      ]);
      setHealth(healthData);
      setServicesStatus(servicesData);
    } catch (err) {
      console.error('Failed to fetch status:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  return (
    <div className="flex flex-col h-full bg-slate-950 overflow-y-auto">
      {/* Header */}
      <div className="bg-slate-900 border-b border-slate-800 p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <SettingsIcon className="text-primary-500" size={28} />
            <div>
              <h1 className="text-xl font-bold">Settings</h1>
              <p className="text-sm text-slate-400">System Configuration</p>
            </div>
          </div>
          <button
            onClick={fetchStatus}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* System Status */}
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Server size={20} className="text-primary-500" />
            System Status
          </h2>

          {loading ? (
            <div className="flex justify-center py-8">
              <RefreshCw className="animate-spin text-primary-500" size={32} />
            </div>
          ) : (
            <div className="space-y-3">
              {/* Gateway Status */}
              <StatusItem
                name="Gateway"
                status={health?.gateway === 'healthy'}
                info="Main API Gateway"
              />

              {/* Services Status */}
              {health?.services && Object.entries(health.services).map(([name, service]: [string, any]) => (
                <StatusItem
                  key={name}
                  name={name === 'agent_zero' ? 'Agent Zero' : name === 'solana_bot' ? 'Solana Bot' : 'Marketplace'}
                  status={service.status === 'healthy'}
                  info={service.url || service.path || 'N/A'}
                />
              ))}
            </div>
          )}
        </div>

        {/* Service Details */}
        {servicesStatus && (
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <h2 className="text-lg font-semibold mb-4">Service Details</h2>
            <div className="space-y-3">
              {Object.entries(servicesStatus).map(([name, details]: [string, any]) => (
                <div key={name} className="border-b border-slate-800 pb-3 last:border-0">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium capitalize">{name.replace('_', ' ')}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      details.healthy ? 'bg-green-900/50 text-green-300' : 'bg-red-900/50 text-red-300'
                    }`}>
                      {details.status}
                    </span>
                  </div>
                  <div className="text-sm text-slate-400 space-y-1">
                    <div>URL: {details.url}</div>
                    <div>Process: {details.process_alive ? 'Running' : 'Stopped'}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* App Info */}
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Info size={20} className="text-primary-500" />
            App Info
          </h2>
          <div className="space-y-2 text-sm">
            <InfoRow label="Version" value="1.0.0" />
            <InfoRow label="Platform" value="Progressive Web App" />
            <InfoRow label="Build" value="Production" />
            <InfoRow label="API Endpoint" value={health ? 'localhost:8080' : 'N/A'} />
          </div>
        </div>

        {/* Links */}
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h2 className="text-lg font-semibold mb-4">Links</h2>
          <div className="space-y-2">
            <LinkItem
              label="Agent Zero Documentation"
              href="https://github.com/frdel/agent-zero"
            />
            <LinkItem
              label="Report Issue"
              href="https://github.com/frdel/agent-zero/issues"
            />
            <LinkItem
              label="Community Discord"
              href="https://discord.gg/B8KZKNsPpj"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-slate-500 py-4">
          <p>AI EcoSystem v1.0.0</p>
          <p className="mt-1">Built with Agent Zero, Solana Bot & Marketplace</p>
        </div>
      </div>
    </div>
  );
}

interface StatusItemProps {
  name: string;
  status: boolean;
  info: string;
}

function StatusItem({ name, status, info }: StatusItemProps) {
  return (
    <div className="flex items-center justify-between py-2">
      <div className="flex items-center gap-3">
        {status ? (
          <CheckCircle size={20} className="text-green-500" />
        ) : (
          <XCircle size={20} className="text-red-500" />
        )}
        <div>
          <div className="font-medium">{name}</div>
          <div className="text-xs text-slate-500">{info}</div>
        </div>
      </div>
      <span className={`text-xs px-2 py-1 rounded ${
        status ? 'bg-green-900/50 text-green-300' : 'bg-red-900/50 text-red-300'
      }`}>
        {status ? 'Online' : 'Offline'}
      </span>
    </div>
  );
}

interface InfoRowProps {
  label: string;
  value: string;
}

function InfoRow({ label, value }: InfoRowProps) {
  return (
    <div className="flex justify-between py-1">
      <span className="text-slate-400">{label}</span>
      <span className="font-medium">{value}</span>
    </div>
  );
}

interface LinkItemProps {
  label: string;
  href: string;
}

function LinkItem({ label, href }: LinkItemProps) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center justify-between py-2 px-3 hover:bg-slate-800 rounded-lg transition-colors group"
    >
      <span>{label}</span>
      <ExternalLink size={16} className="text-slate-500 group-hover:text-primary-500" />
    </a>
  );
}
