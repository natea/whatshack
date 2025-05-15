-- Schema for service_bundles table

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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Schema for service_bundle_features table
CREATE TABLE IF NOT EXISTS service_bundle_features (
    feature_id TEXT,
    bundle_id TEXT REFERENCES service_bundles(bundle_id),
    name_en TEXT NOT NULL,
    name_xh TEXT,
    name_af TEXT,
    description_en TEXT,
    description_xh TEXT,
    description_af TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (feature_id, bundle_id)
);

-- Schema for user_bundle_selections table
CREATE TABLE IF NOT EXISTS user_bundle_selections (
    selection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    bundle_id TEXT REFERENCES service_bundles(bundle_id),
    selection_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, bundle_id, active)
);

-- Add index for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_bundle_selections_user_id ON user_bundle_selections(user_id);
CREATE INDEX IF NOT EXISTS idx_user_bundle_selections_bundle_id ON user_bundle_selections(bundle_id);
CREATE INDEX IF NOT EXISTS idx_service_bundle_features_bundle_id ON service_bundle_features(bundle_id);

-- Add column to users table for current bundle
ALTER TABLE IF EXISTS users 
ADD COLUMN IF NOT EXISTS current_bundle TEXT REFERENCES service_bundles(bundle_id);