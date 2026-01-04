import { useState, useEffect, useRef } from 'react';
import { supabase, Message, Conversation } from '../lib/supabase';
import ChatSidebar from './ChatSidebar';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { Loader2 } from 'lucide-react';
import cyberSaathiAPI from './api.js';

interface ChatContainerProps {
  onBack: () => void;
}

export default function ChatContainer({ onBack }: ChatContainerProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (currentConversationId) {
      loadMessages(currentConversationId);
    }
  }, [currentConversationId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const { data, error } = await supabase
        .from('conversations')
        .select('*')
        .order('updated_at', { ascending: false });

      if (error) throw error;
      setConversations(data || []);
    } catch (error) {
      console.error('Error loading conversations:', error);
    } finally {
      setInitializing(false);
    }
  };

  const loadMessages = async (conversationId: string) => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .eq('conversation_id', conversationId)
        .order('created_at', { ascending: true });

      if (error) throw error;
      setMessages(data || []);
    } catch (error) {
      console.error('Error loading messages:', error);
      setMessages([]);
    }
  };

  const createNewConversation = async (firstMessage: string): Promise<string | null> => {
    try {
      const title = firstMessage.slice(0, 50) + (firstMessage.length > 50 ? '...' : '');

      const { data, error } = await supabase
        .from('conversations')
        .insert({ title })
        .select()
        .single();

      if (error) throw error;

      setConversations([data, ...conversations]);
      return data.id;
    } catch (error) {
      console.error('Error creating conversation:', error);
      return null;
    }
  };

  const saveMessage = async (conversationId: string, role: 'user' | 'assistant', content: string) => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .insert({
          conversation_id: conversationId,
          role,
          content,
        })
        .select()
        .single();

      if (error) throw error;

      await supabase
        .from('conversations')
        .update({ updated_at: new Date().toISOString() })
        .eq('id', conversationId);

      return data;
    } catch (error) {
      console.error('Error saving message:', error);
      return null;
    }
  };



  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    setLoading(true);

    try {
      let conversationId = currentConversationId;

      if (!conversationId) {
        conversationId = await createNewConversation(content);
        if (!conversationId) {
          throw new Error('Failed to create conversation');
        }
        setCurrentConversationId(conversationId);
      }

      // Save user message
      const userMessage = await saveMessage(conversationId, 'user', content);
      if (userMessage) {
        setMessages((prev) => [...prev, userMessage]);
      }

      // Call the actual chat API
      const apiResponse = await cyberSaathiAPI.chat(content);
      
      // Extract the answer from the API response
      const assistantResponse = apiResponse.answer || 'Sorry, I could not generate a response.';
      
      // Save assistant message
      const assistantMessage = await saveMessage(conversationId, 'assistant', assistantResponse);

      if (assistantMessage) {
        setMessages((prev) => [...prev, assistantMessage]);
      }

      await loadConversations();
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Show error message to user
      const errorMessage = `I apologize, but I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please make sure the backend API is running at http://127.0.0.1:8000`;
      
      if (currentConversationId) {
        const errorMsg = await saveMessage(currentConversationId, 'assistant', errorMessage);
        if (errorMsg) {
          setMessages((prev) => [...prev, errorMsg]);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setCurrentConversationId(null);
    setMessages([]);
  };

  const handleSelectConversation = (id: string) => {
    setCurrentConversationId(id);
  };

  if (initializing) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <Loader2 className="animate-spin text-cyan-400 mx-auto mb-4" size={48} />
          <p className="text-slate-400">Loading Cyber Law Assistant...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-black">
      <ChatSidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        onBack={onBack}
      />

      <div className="flex-1 flex flex-col bg-gradient-to-b from-slate-950 to-black">
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center space-y-6 max-w-2xl px-6">
                <h2 className="text-3xl font-bold text-white">Start a Conversation</h2>
                <p className="text-slate-400">Ask me anything about cyber law, data protection, digital rights, and technology regulations.</p>
              </div>
            </div>
          ) : (
            <div>
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {loading && (
                <div className="flex gap-4 p-6 mx-auto max-w-4xl">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-gradient-to-br from-cyan-400 to-orange-500">
                    <Loader2 className="animate-spin text-black" size={18} />
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold text-sm text-cyan-400 mb-2">
                      Cyber Law Assistant
                    </div>
                    <div className="text-slate-400">Analyzing your question...</div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
      </div>
    </div>
  );
}
