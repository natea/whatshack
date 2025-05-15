-- Function to hard delete all user data from the database
-- This function deletes all records related to a user from all tables
-- and finally deletes the user from the users table

CREATE OR REPLACE FUNCTION hard_delete_user_data(user_whatsapp_id TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    success BOOLEAN := FALSE;
BEGIN
    -- Delete all message logs for the user
    DELETE FROM message_logs WHERE user_whatsapp_id = $1;
    
    -- Delete any security logs for the user
    DELETE FROM security_logs WHERE user_whatsapp_id = $1;
    
    -- Delete the user from the users table
    DELETE FROM users WHERE whatsapp_id = $1;
    
    -- If we reach this point without errors, the deletion was successful
    success := TRUE;
    
    -- Return success status
    RETURN success;
EXCEPTION
    WHEN OTHERS THEN
        -- Log the error (in a real system, you might want to log to a table)
        RAISE NOTICE 'Error deleting user data: %', SQLERRM;
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION hard_delete_user_data(TEXT) TO authenticated;

-- Comment on function
COMMENT ON FUNCTION hard_delete_user_data(TEXT) IS 'Deletes all data related to a user from all tables in the database';