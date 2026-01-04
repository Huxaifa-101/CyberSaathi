import { Bot, User } from 'lucide-react';
import { Message } from '../lib/supabase';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === 'assistant';

  return (
    <div className={`flex gap-4 px-6 py-4 ${isAssistant ? 'bg-slate-900/30' : 'bg-transparent'}`}>
      <div className="max-w-4xl mx-auto w-full flex gap-4">
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isAssistant ? 'bg-gradient-to-br from-cyan-400 to-orange-500' : 'bg-slate-700'
        }`}>
          {isAssistant ? <Bot size={18} className="text-black" /> : <User size={18} className="text-white" />}
        </div>
        <div className="flex-1 space-y-2">
          <div className="font-semibold text-sm text-cyan-400">
            {isAssistant ? 'Cyber Law Assistant' : 'You'}
          </div>
          <div className="text-slate-300 leading-relaxed whitespace-pre-wrap">
            {message.content}
          </div>
          {isAssistant && (
            <div className="text-xs text-slate-500 italic mt-3 pt-3 border-t border-slate-700">
              This information is for educational purposes only and does not constitute legal advice.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
