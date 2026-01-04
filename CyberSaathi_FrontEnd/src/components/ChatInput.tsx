import { useState } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t border-slate-800 bg-gradient-to-t from-black to-slate-950 p-6">
      <div className="max-w-4xl mx-auto flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about cyber law, data protection, digital rights..."
          disabled={disabled}
          className="flex-1 px-4 py-3 bg-slate-900 border border-slate-700 text-white placeholder-slate-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-transparent disabled:bg-slate-950 disabled:cursor-not-allowed transition-all"
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="px-6 py-3 bg-gradient-to-r from-cyan-400 to-orange-500 text-black font-semibold rounded-lg hover:shadow-lg hover:shadow-cyan-400/50 disabled:bg-slate-700 disabled:cursor-not-allowed transition-all flex items-center gap-2"
        >
          <Send size={18} />
          Send
        </button>
      </div>
    </form>
  );
}
