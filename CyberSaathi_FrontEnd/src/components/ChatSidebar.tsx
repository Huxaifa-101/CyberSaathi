import { MessageSquare, Plus, ArrowLeft } from 'lucide-react';
import { Conversation } from '../lib/supabase';

interface ChatSidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
  onBack: () => void;
}

export default function ChatSidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onBack,
}: ChatSidebarProps) {
  return (
    <div className="w-64 bg-gradient-to-b from-slate-900 to-black text-white flex flex-col h-screen border-r border-slate-800">
      <div className="p-4 border-b border-slate-800/50">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors mb-4 text-sm"
        >
          <ArrowLeft size={16} />
          Back
        </button>
        <button
          onClick={onNewConversation}
          className="w-full flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500/20 to-orange-500/20 hover:from-cyan-500/30 hover:to-orange-500/30 border border-cyan-400/50 rounded-lg transition-all"
        >
          <Plus size={18} />
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        <div className="text-xs font-semibold text-slate-500 px-3 py-2 uppercase tracking-wider">
          Recent Chats
        </div>
        {conversations.length === 0 ? (
          <div className="px-3 py-4 text-sm text-slate-500 text-center">
            No chats yet
          </div>
        ) : (
          <div className="space-y-2">
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => onSelectConversation(conv.id)}
                className={`w-full text-left px-3 py-2 rounded-lg transition-all flex items-center gap-2 text-sm ${
                  currentConversationId === conv.id
                    ? 'bg-gradient-to-r from-cyan-500/30 to-orange-500/30 border border-cyan-400/50 text-white'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <MessageSquare size={14} />
                <span className="truncate">{conv.title}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-slate-800/50 text-xs text-slate-500 space-y-3">
        <div className="font-semibold text-slate-400 uppercase tracking-wider">Topics</div>
        <div className="space-y-1 text-slate-500">
          <div>• Cyber Crime</div>
          <div>• Data Protection</div>
          <div>• IP Rights</div>
          <div>• Social Media Law</div>
          <div>• AI & Tech Regulation</div>
          <div>• Digital Ethics</div>
        </div>
      </div>
    </div>
  );
}
