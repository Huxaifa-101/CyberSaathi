/*
  # Cyber Law Chatbot Database Schema

  ## Overview
  Creates the database structure for storing chat conversations between users and the Cyber Law AI Assistant.

  ## New Tables
  
  ### `conversations`
  Stores individual chat sessions
  - `id` (uuid, primary key) - Unique identifier for each conversation
  - `created_at` (timestamptz) - When the conversation was started
  - `updated_at` (timestamptz) - Last message timestamp
  - `title` (text) - Auto-generated conversation title based on first message
  
  ### `messages`
  Stores individual messages within conversations
  - `id` (uuid, primary key) - Unique message identifier
  - `conversation_id` (uuid, foreign key) - Links to parent conversation
  - `role` (text) - Either 'user' or 'assistant'
  - `content` (text) - The message text
  - `created_at` (timestamptz) - When the message was sent

  ## Security
  - Enable RLS on both tables
  - Public read/write access for demo purposes (in production, this would be user-specific)
  
  ## Indexes
  - Index on conversation_id for fast message retrieval
  - Index on created_at for chronological sorting
*/

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  title text DEFAULT 'New Conversation'
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id uuid REFERENCES conversations(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at DESC);

-- Enable Row Level Security
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (demo mode)
CREATE POLICY "Allow public read access to conversations"
  ON conversations FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Allow public insert to conversations"
  ON conversations FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Allow public update to conversations"
  ON conversations FOR UPDATE
  TO anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public read access to messages"
  ON messages FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Allow public insert to messages"
  ON messages FOR INSERT
  TO anon
  WITH CHECK (true);