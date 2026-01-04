import { Shield, Lock, Gavel, Globe, AlertTriangle, BookOpen } from 'lucide-react';

export default function FeatureCards() {
  const features = [
    {
      icon: Shield,
      title: 'Cyber Crime',
      description: 'Hacking & Digital Crimes',
    },
    {
      icon: Lock,
      title: 'Data Protection',
      description: 'Privacy & GDPR Laws',
    },
    {
      icon: Gavel,
      title: 'IP Rights',
      description: 'Intellectual Property',
    },
    {
      icon: Globe,
      title: 'Digital Commerce',
      description: 'E-commerce & Contracts',
    },
    {
      icon: AlertTriangle,
      title: 'Social Media',
      description: 'Online Regulations',
    },
    {
      icon: BookOpen,
      title: 'AI & Emerging Tech',
      description: 'Future of Digital Law',
    },
  ];

  return (
    <div className="bg-black py-24">
      <div className="max-w-7xl mx-auto px-6">
        <h2 className="text-4xl font-bold text-white text-center mb-16">
          Master Key Areas of Cyber Law
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="group relative bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 rounded-xl p-6 hover:border-cyan-400/50 transition-all hover:shadow-xl hover:shadow-cyan-400/20"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/0 to-orange-500/0 group-hover:from-cyan-400/10 group-hover:to-orange-500/10 rounded-xl transition-all"></div>

              <div className="relative z-10 space-y-3">
                <div className="w-12 h-12 bg-gradient-to-br from-cyan-400/20 to-orange-500/20 rounded-lg flex items-center justify-center border border-cyan-400/30 group-hover:border-cyan-400/60 transition-colors">
                  <feature.icon className="text-cyan-400 group-hover:text-orange-500 transition-colors" size={24} />
                </div>
                <h3 className="font-bold text-white text-lg">{feature.title}</h3>
                <p className="text-slate-400 text-sm">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
