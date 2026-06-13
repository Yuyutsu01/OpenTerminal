'use client';

import React, { useState, useEffect } from 'react';
import { 
  BarChart2, Terminal, BookOpen, Search, Cpu, 
  Sparkles, Sliders, Bell, AlertTriangle, Layers, Keyboard 
} from 'lucide-react';

// Import dashboards
import InvestorDashboard from '@/components/Dashboards/InvestorDashboard';
import EconomistDashboard from '@/components/Dashboards/EconomistDashboard';
import StudentDashboard from '@/components/Dashboards/StudentDashboard';
import ResearchDashboard from '@/components/Dashboards/ResearchDashboard';
import GovernmentDashboard from '@/components/Dashboards/GovernmentDashboard';

// Import simulator, copilot and command bar
import SimulatorPanel from '@/components/ScenarioSimulator/SimulatorPanel';
import MacroGraph from '@/components/AICopilot/MacroGraph';
import CopilotPanel from '@/components/AICopilot/CopilotPanel';
import CommandBar from '@/components/CommandBar';

interface AlertMessage {
  title: string;
  severity: string;
  message: string;
  time: string;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState('investor');
  const [isCommandBarOpen, setIsCommandBarOpen] = useState(false);
  const [copilotSearchQuery, setCopilotSearchQuery] = useState('');
  
  // Real-time ticking ticks
  const [liveTicks, setLiveTicks] = useState<any>({});
  
  // Real-time notifications / alerts list
  const [alerts, setAlerts] = useState<AlertMessage[]>([
    {
      title: 'System Initialized',
      severity: 'Low',
      message: 'Terminal connected. Macro relationship nodes loaded successfully.',
      time: new Date().toLocaleTimeString()
    }
  ]);
  const [activeToast, setActiveToast] = useState<AlertMessage | null>(null);

  // Establish WebSockets Connection to backend
  useEffect(() => {
    let ws: WebSocket;
    
    const connectWS = () => {
      ws = new WebSocket('ws://localhost:8000/api/ws');

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          
          if (msg.type === 'tick') {
            setLiveTicks(msg.data);
          } else if (msg.type === 'alerts') {
            const newAlerts = msg.data.map((a: any) => ({
              ...a,
              time: new Date().toLocaleTimeString()
            }));
            
            setAlerts(prev => [...newAlerts, ...prev].slice(0, 15)); // Cap at 15
            
            // Pop active toast alert
            if (newAlerts.length > 0) {
              setActiveToast(newAlerts[0]);
              // Dismiss toast after 4 seconds
              setTimeout(() => setActiveToast(null), 4000);
            }
          }
        } catch (e) {
          console.error("Error parsing WS packet: ", e);
        }
      };

      ws.onerror = (err) => {
        console.error("WebSocket error:", err);
      };

      ws.onclose = () => {
        // Auto-reconnect after 3 seconds
        setTimeout(connectWS, 3000);
      };
    };

    connectWS();
    return () => {
      if (ws) ws.close();
    };
  }, []);

  // Listen to keyboard shortcut '/' or 'Ctrl+K' to open Command Bar
  useEffect(() => {
    const handleGlobalKeys = (e: KeyboardEvent) => {
      if (e.key === '/' && document.activeElement?.tagName !== 'INPUT') {
        e.preventDefault();
        setIsCommandBarOpen(true);
      } else if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandBarOpen(true);
      }
    };

    window.addEventListener('keydown', handleGlobalKeys);
    return () => window.removeEventListener('keydown', handleGlobalKeys);
  }, []);

  const executeCommand = (cmd: string) => {
    // Reset copilot search query to allow repeated triggering
    setCopilotSearchQuery('');

    if (cmd.startsWith('/dashboard')) {
      const db = cmd.split(' ')[1];
      if (['investor', 'economist', 'student', 'research', 'government'].includes(db)) {
        setActiveTab(db);
      }
    } else if (cmd.startsWith('/simulate')) {
      // Toggle to Economist Dashboard where simulator resides, 
      // or triggers AI analyst copilot with specific prompt
      setActiveTab('economist');
      const queryText = cmd.substring(10);
      setCopilotSearchQuery(`What happens if ${queryText}?`);
    } else if (cmd.startsWith('/teach')) {
      setActiveTab('student');
    } else if (cmd.startsWith('/ask')) {
      const q = cmd.substring(5);
      setCopilotSearchQuery(q);
    }
  };

  return (
    <main className="h-screen bg-[#030712] flex flex-col font-mono relative overflow-hidden select-none">
      
      {/* Top Header bar */}
      <header className="h-11 border-b border-gray-850 bg-[#090d16]/90 flex items-center justify-between px-4 z-10 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <Terminal className="w-5 h-5 text-blue-500 animate-pulse" />
          <span className="text-xs font-bold text-gray-150 tracking-wider">
            OPENTERMINAL <span className="text-gray-500 font-normal">v1.2 // INDIAN ECON INTELLIGENCE ENGINE</span>
          </span>
        </div>

        {/* Global Action Search Button */}
        <button 
          onClick={() => setIsCommandBarOpen(true)}
          className="flex items-center gap-2 px-3 py-1 bg-gray-950/65 border border-gray-800 rounded text-[10px] text-gray-500 hover:text-gray-350 transition-colors font-mono cursor-pointer"
        >
          <Keyboard className="w-3.5 h-3.5" />
          <span>Press <kbd className="text-gray-400 font-bold">/</kbd> or <kbd className="text-gray-400 font-bold">Ctrl+K</kbd> to search</span>
        </button>

        <div className="flex items-center gap-3">
          {/* Ticking clock indicator */}
          <span className="text-[10px] text-gray-500 flex items-center">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-ping"></span>
            LIVE FEEDS CHANNEL
          </span>
        </div>
      </header>

      {/* Main Terminal Grid Shell */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Dashboard Switcher Tabbar */}
        <aside className="w-12 border-r border-gray-850 bg-[#070b13] flex flex-col items-center py-4 justify-between">
          <div className="flex flex-col gap-5 items-center">
            {/* Investor Tab */}
            <button
              onClick={() => setActiveTab('investor')}
              title="Investor Dashboard"
              className={`p-2 rounded transition-colors ${
                activeTab === 'investor' ? 'bg-blue-600/15 text-blue-400 border border-blue-600/50' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <BarChart2 className="w-4 h-4" />
            </button>

            {/* Economist Tab */}
            <button
              onClick={() => setActiveTab('economist')}
              title="Economist Dashboard"
              className={`p-2 rounded transition-colors ${
                activeTab === 'economist' ? 'bg-blue-600/15 text-blue-400 border border-blue-600/50' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <Terminal className="w-4 h-4" />
            </button>

            {/* Student Tab */}
            <button
              onClick={() => setActiveTab('student')}
              title="Interactive Learning Mode"
              className={`p-2 rounded transition-colors ${
                activeTab === 'student' ? 'bg-blue-600/15 text-blue-400 border border-blue-600/50' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <BookOpen className="w-4 h-4" />
            </button>

            {/* Researcher Tab */}
            <button
              onClick={() => setActiveTab('research')}
              title="AI Research Analyst Reports"
              className={`p-2 rounded transition-colors ${
                activeTab === 'research' ? 'bg-blue-600/15 text-blue-400 border border-blue-600/50' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <Search className="w-4 h-4" />
            </button>

            {/* Government/Policymaker Tab */}
            <button
              onClick={() => setActiveTab('government')}
              title="Government Alternative Data Dashboard"
              className={`p-2 rounded transition-colors ${
                activeTab === 'government' ? 'bg-blue-600/15 text-blue-400 border border-blue-600/50' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <Cpu className="w-4 h-4" />
            </button>
          </div>

          <div className="flex flex-col gap-4 items-center">
            {/* Command shortcut */}
            <button 
              onClick={() => setIsCommandBarOpen(true)}
              className="p-2 text-gray-650 hover:text-gray-400"
            >
              <Keyboard className="w-4 h-4" />
            </button>
          </div>
        </aside>

        {/* Central Dynamic Workspace Panel */}
        <div className="flex-1 flex flex-col p-3 overflow-y-auto gap-3">
          
          {/* Top workspace row: Active Tab Rendering */}
          <div className="flex-1 overflow-hidden min-h-[300px]">
            {activeTab === 'investor' && <InvestorDashboard liveTicks={liveTicks} />}
            {activeTab === 'economist' && <EconomistDashboard />}
            {activeTab === 'student' && <StudentDashboard />}
            {activeTab === 'research' && <ResearchDashboard />}
            {activeTab === 'government' && <GovernmentDashboard />}
          </div>

          {/* Bottom workspace row: Macro knowledge graph AND Scenario simulator */}
          <div className="h-[420px] min-h-[420px] grid grid-cols-1 md:grid-cols-2 gap-3">
            <MacroGraph />
            <SimulatorPanel />
          </div>

        </div>

        {/* Right Drawer: AI Research Analyst Chat Co-pilot */}
        <aside className="w-80 min-w-[320px] max-w-sm hidden xl:block">
          <CopilotPanel 
            onSearchQuery={copilotSearchQuery} 
            onNavigateToDashboard={(db) => executeCommand(`/dashboard ${db}`)}
          />
        </aside>

      </div>

      {/* Floating System Alerts / Blinking Toasts Notification layer */}
      {activeToast && (
        <div className="fixed bottom-4 right-4 z-40 max-w-xs border border-yellow-500/50 bg-[#090d16] shadow-2xl rounded p-3 flex items-start gap-2.5 animate-bounce font-mono text-xs">
          <AlertTriangle className="w-4.5 h-4.5 text-yellow-500 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-yellow-400 block mb-0.5">{activeToast.title}</span>
            <p className="text-gray-400 text-[10px] leading-tight">{activeToast.message}</p>
          </div>
        </div>
      )}

      {/* Keyboard Command Dialog overlay */}
      <CommandBar
        isOpen={isCommandBarOpen}
        onClose={() => setIsCommandBarOpen(false)}
        onExecuteCommand={executeCommand}
      />

    </main>
  );
}
