import { BrowserRouter, Routes, Route } from 'react-router-dom';
import TabBar from './components/TabBar';
import AgentChat from './pages/AgentChat';
import SolanaBot from './pages/SolanaBot';
import Marketplace from './pages/Marketplace';
import Settings from './pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col h-screen bg-slate-950 text-white overflow-hidden">
        <main className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<AgentChat />} />
            <Route path="/solana" element={<SolanaBot />} />
            <Route path="/marketplace" element={<Marketplace />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
        <TabBar />
      </div>
    </BrowserRouter>
  );
}

export default App;
