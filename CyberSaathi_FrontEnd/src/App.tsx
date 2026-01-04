import { useState } from 'react';
import Navigation from './components/Navigation';
import HeroSection from './components/HeroSection';
import FeatureCards from './components/FeatureCards';
import ChatContainer from './components/ChatContainer';

function App() {
  const [showChat, setShowChat] = useState(false);

  const handleGetStarted = () => {
    setShowChat(true);
  };

  const handleBackToHome = () => {
    setShowChat(false);
  };

  if (showChat) {
    return <ChatContainer onBack={handleBackToHome} />;
  }

  return (
    <>
      <Navigation onGetStarted={handleGetStarted} />
      <HeroSection onGetStarted={handleGetStarted} />
      <FeatureCards />

      <footer className="bg-black border-t border-slate-800 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center text-slate-500 text-sm space-y-4">
          <div>
            Educational AI Assistant for Cyber Law | Not a substitute for legal advice
          </div>
          <div>
            © 2024 Cyber Saathi AI. All rights reserved.
          </div>
        </div>
      </footer>
    </>
  );
}

export default App;
