-- Function to count users with a specific WhatsApp ID
-- This function is used for verification in the AI-verifiable deliverable

CREATE OR REPLACE FUNCTION get_user_count(user_id TEXT)
RETURNS INTEGER AS $$
DECLARE
    user_count INTEGER;
BEGIN
    -- Count users with the specified WhatsApp ID
    SELECT COUNT(*) INTO user_count FROM users WHERE whatsapp_id = $1;
    
    -- Return the count
    RETURN user_count;
EXCEPTION
    WHEN OTHERS THEN
        -- Log the error (in a real system, you might want to log to a table)
        RAISE NOTICE 'Error counting users: %', SQLERRM;
        RETURN 0;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION get_user_count(TEXT) TO authenticated;

-- Comment on function
COMMENT ON FUNCTION get_user_count(TEXT) IS 'Counts users with a specific WhatsApp ID for verification purposes';