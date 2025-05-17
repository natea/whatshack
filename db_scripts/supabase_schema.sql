-- Township Connect WhatsApp Assistant Database Schema
-- Execute this SQL in the Supabase Studio SQL Editor

-- Township Connect WhatsApp Assistant Database Schema v1
-- This schema defines the core tables for the Township Connect application
-- Tables: users, service_bundles, message_logs

-- Users table - stores user information and preferences
CREATE TABLE IF NOT EXISTS users (
    whatsapp_id TEXT PRIMARY KEY,
    preferred_language TEXT DEFAULT 'en',
    current_bundle TEXT,
    popia_consent_given BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    baileys_creds_encrypted TEXT,
    CONSTRAINT whatsapp_id_unique UNIQUE (whatsapp_id)
);

-- Service bundles table - stores available service bundles
CREATE TABLE IF NOT EXISTS service_bundles (
    bundle_id TEXT PRIMARY KEY,
    bundle_name_en TEXT NOT NULL,
    bundle_name_xh TEXT NOT NULL,
    bundle_name_af TEXT NOT NULL,
    description_en TEXT,
    description_xh TEXT,
    description_af TEXT,
    price_tier TEXT DEFAULT 'free',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Message logs table - stores all message interactions
CREATE TABLE IF NOT EXISTS message_logs (
    log_id SERIAL PRIMARY KEY,
    user_whatsapp_id TEXT REFERENCES users(whatsapp_id),
    direction TEXT, -- 'inbound' or 'outbound'
    message_content TEXT,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    data_size_kb FLOAT
);

-- Security logs table - stores security-related events
CREATE TABLE IF NOT EXISTS security_logs (
    event_id SERIAL PRIMARY KEY,
    user_whatsapp_id TEXT,
    event_type TEXT,
    details JSONB,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_message_logs_user_id ON message_logs(user_whatsapp_id);
CREATE INDEX IF NOT EXISTS idx_message_logs_timestamp ON message_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_users_language ON users(preferred_language);
CREATE INDEX IF NOT EXISTS idx_users_bundle ON users(current_bundle);
CREATE INDEX IF NOT EXISTS idx_security_logs_user_id ON security_logs(user_whatsapp_id);
CREATE INDEX IF NOT EXISTS idx_security_logs_event_type ON security_logs(event_type);

-- Enable Row-Level Security (RLS) on the users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create a policy that restricts access to users based on their whatsapp_id
-- This is a placeholder that will be replaced with actual auth.uid() checks when Supabase Auth is implemented
CREATE POLICY users_isolation_policy ON users
    USING (whatsapp_id = current_setting('app.current_user_id', TRUE)::TEXT);

-- Create a policy for the message_logs table to restrict access to a user's own messages
ALTER TABLE message_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY message_logs_isolation_policy ON message_logs
    USING (user_whatsapp_id = current_setting('app.current_user_id', TRUE)::TEXT);

-- Create a policy for the security_logs table to restrict access to a user's own security logs
ALTER TABLE security_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY security_logs_isolation_policy ON security_logs
    USING (user_whatsapp_id = current_setting('app.current_user_id', TRUE)::TEXT);

-- Create a function to delete all user data (for POPIA compliance)
CREATE OR REPLACE FUNCTION hard_delete_user_data(user_whatsapp_id TEXT)
RETURNS VOID AS $$
BEGIN
    -- Delete message logs
    DELETE FROM message_logs WHERE user_whatsapp_id = $1;
    
    -- Delete security logs
    DELETE FROM security_logs WHERE user_whatsapp_id = $1;
    
    -- Delete user
    DELETE FROM users WHERE whatsapp_id = $1;
END;
$$ LANGUAGE plpgsql;

-- Comment on tables and columns for documentation
COMMENT ON TABLE users IS 'Stores user information, preferences, and consent status';
COMMENT ON TABLE service_bundles IS 'Stores available service bundles with multilingual names and descriptions';
COMMENT ON TABLE message_logs IS 'Logs all message interactions with data size tracking for monitoring';
COMMENT ON TABLE security_logs IS 'Logs security-related events such as data deletion requests';