-- Pakistani Cyber Law Database Setup
-- Run this script after creating the database

-- Create database (run this separately in psql)
-- CREATE DATABASE pak_cyberlaw_db;

-- Connect to database
-- \c pak_cyberlaw_db;

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table: law_documents
-- Stores chunked documents with embeddings
CREATE TABLE IF NOT EXISTS law_documents (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(500) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: document_registry
-- Tracks uploaded documents
CREATE TABLE IF NOT EXISTS document_registry (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(500) UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    total_chunks INTEGER DEFAULT 0,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB DEFAULT '{}'
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_law_documents_document_name 
    ON law_documents(document_name);

CREATE INDEX IF NOT EXISTS idx_law_documents_embedding 
    ON law_documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_law_documents_metadata 
    ON law_documents USING gin(metadata);

CREATE INDEX IF NOT EXISTS idx_document_registry_name 
    ON document_registry(document_name);

CREATE INDEX IF NOT EXISTS idx_document_registry_hash 
    ON document_registry(file_hash);

-- Create view for document statistics
CREATE OR REPLACE VIEW document_stats AS
SELECT 
    dr.document_name,
    dr.document_type,
    dr.total_chunks,
    dr.upload_date,
    dr.last_updated,
    dr.status,
    COUNT(ld.id) as actual_chunks,
    pg_size_pretty(
        pg_total_relation_size('law_documents')
    ) as total_size
FROM document_registry dr
LEFT JOIN law_documents ld ON dr.document_name = ld.document_name
GROUP BY dr.id, dr.document_name, dr.document_type, 
         dr.total_chunks, dr.upload_date, dr.last_updated, dr.status;

-- Function to update timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for law_documents
CREATE TRIGGER update_law_documents_updated_at 
    BEFORE UPDATE ON law_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for document_registry
CREATE TRIGGER update_document_registry_updated_at 
    BEFORE UPDATE ON document_registry
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;

-- Verify setup
SELECT 'Setup completed successfully!' as status;
SELECT 'Tables created:', tablename FROM pg_tables WHERE schemaname = 'public';
