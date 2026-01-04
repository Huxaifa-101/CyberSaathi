import { Scale } from 'lucide-react';

interface NavigationProps {
  onGetStarted: () => void;
}

export default function Navigation({ onGetStarted }: NavigationProps) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-b from-black to-transparent backdrop-blur-sm border-b border-slate-800/50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-cyan-400 to-orange-500 rounded-lg flex items-center justify-center">
            <Scale size={20} className="text-black" />
          </div>
          <span className="text-xl font-bold text-white">Cyber Law AI</span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">About</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Pricing</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Contact</a>
        </div>

        <button
          onClick={onGetStarted}
          className="px-6 py-2 bg-gradient-to-r from-cyan-400 to-orange-500 text-black font-semibold rounded-lg hover:shadow-lg hover:shadow-cyan-400/50 transition-all"
        >
          Get Started
        </button>
      </div>
    </nav>
  );
}
