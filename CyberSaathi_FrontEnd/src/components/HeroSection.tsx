import { ArrowRight } from 'lucide-react';

interface HeroSectionProps {
  onGetStarted: () => void;
}

export default function HeroSection({ onGetStarted }: HeroSectionProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-950 to-black relative overflow-hidden pt-20">
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-400/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-orange-500/20 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-32 text-center space-y-8">
        <div className="space-y-4">
          <div className="inline-block">
            <span className="text-sm font-semibold text-cyan-400 uppercase tracking-widest bg-slate-800/50 px-4 py-2 rounded-full border border-cyan-400/30">
              AI-Powered Legal Education
            </span>
          </div>
          <h1 className="text-6xl lg:text-7xl font-bold text-white leading-tight">
            Cyber Law <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-orange-500 text-transparent bg-clip-text">Intelligence</span>
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Master digital rights, regulations, and cyber ethics with our intelligent AI assistant. Get instant answers about complex legal frameworks in the digital age.
          </p>
        </div>

        <button
          onClick={onGetStarted}
          className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-cyan-400 to-orange-500 text-black font-bold rounded-lg hover:shadow-2xl hover:shadow-cyan-400/50 transition-all hover:scale-105"
        >
          Start Chatting Now
          <ArrowRight size={20} />
        </button>

        <div className="pt-12 grid grid-cols-3 gap-6 text-slate-400 text-sm">
          <div className="space-y-1">
            <div className="text-2xl font-bold text-cyan-400">10+</div>
            <div>Legal Topics Covered</div>
          </div>
          <div className="space-y-1">
            <div className="text-2xl font-bold text-cyan-400">24/7</div>
            <div>Always Available</div>
          </div>
          <div className="space-y-1">
            <div className="text-2xl font-bold text-cyan-400">100%</div>
            <div>Educational Focus</div>
          </div>
        </div>
      </div>
    </div>
  );
}
