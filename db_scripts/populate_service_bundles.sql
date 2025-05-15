-- SQL script to populate the service_bundles table with initial data

-- First, ensure the table exists (this should be created in db_schema_v1.sql)
-- CREATE TABLE IF NOT EXISTS service_bundles (
--     bundle_id TEXT PRIMARY KEY,
--     bundle_name_en TEXT,
--     bundle_name_xh TEXT,
--     bundle_name_af TEXT,
--     description_en TEXT,
--     description_xh TEXT,
--     description_af TEXT
-- );

-- Insert Street-Vendor CRM bundle
INSERT INTO service_bundles (
    bundle_id, 
    bundle_name_en, 
    bundle_name_xh, 
    bundle_name_af, 
    description_en, 
    description_xh, 
    description_af
) VALUES (
    'street_vendor_crm',
    'Street-Vendor CRM',
    'Isixhobo soThengiso',
    'Straatverkoper CRM',
    'Tools for street vendors.',
    'Izixhobo zabathengisi basesitratweni.',
    'Gereedskap vir straatverkopers.'
);

-- Insert Small Business Suite bundle
INSERT INTO service_bundles (
    bundle_id, 
    bundle_name_en, 
    bundle_name_xh, 
    bundle_name_af, 
    description_en, 
    description_xh, 
    description_af
) VALUES (
    'small_business',
    'Small Business Suite',
    'Iseti yoShishino oluNcinci',
    'Klein Besigheid Suite',
    'Complete tools for small businesses.',
    'Izixhobo ezipheleleyo zamashishini amancinci.',
    'Volledige gereedskap vir klein besighede.'
);

-- Insert Delivery Runner bundle
INSERT INTO service_bundles (
    bundle_id, 
    bundle_name_en, 
    bundle_name_xh, 
    bundle_name_af, 
    description_en, 
    description_xh, 
    description_af
) VALUES (
    'delivery_runner',
    'Delivery Runner',
    'Umgquzuli woKuhambisa',
    'Aflewering Hardloper',
    'Tools for local delivery runners.',
    'Izixhobo zabagquzuli bokuhambisa bendawo.',
    'Gereedskap vir plaaslike afleweringshardlopers.'
);