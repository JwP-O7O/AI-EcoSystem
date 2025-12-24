import { Link, useLocation } from 'react-router-dom';
import { MessageSquare, TrendingUp, Package, Settings, LucideIcon } from 'lucide-react';

interface TabItemProps {
  to: string;
  icon: LucideIcon;
  label: string;
  active: boolean;
}

const TabItem = ({ to, icon: Icon, label, active }: TabItemProps) => {
  return (
    <Link
      to={to}
      className={`flex-1 flex flex-col items-center justify-center py-2 transition-colors duration-200 ${
        active
          ? 'text-primary-500'
          : 'text-slate-400 hover:text-slate-300'
      }`}
    >
      <Icon size={24} strokeWidth={active ? 2.5 : 2} />
      <span className={`text-xs mt-1 font-medium ${active ? 'font-semibold' : ''}`}>
        {label}
      </span>
    </Link>
  );
};

export default function TabBar() {
  const location = useLocation();

  const tabs = [
    { to: '/', icon: MessageSquare, label: 'Agent' },
    { to: '/solana', icon: TrendingUp, label: 'Trading' },
    { to: '/marketplace', icon: Package, label: 'Market' },
    { to: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <nav className="h-16 bg-slate-900 border-t border-slate-800 flex items-center px-2 shadow-lg">
      {tabs.map((tab) => (
        <TabItem
          key={tab.to}
          {...tab}
          active={location.pathname === tab.to}
        />
      ))}
    </nav>
  );
}
