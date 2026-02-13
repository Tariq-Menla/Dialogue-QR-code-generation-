import sqlite3

def reset_tokens():
    # Path to your specific database
    db_path = './instance/qr.db'
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Update ALL rows to be unused (0)
    cursor.execute("UPDATE qr_codes SET is_used = 0")
    
    # Save the changes
    connection.commit()
    
    # Check how many were reset
    cursor.execute("SELECT COUNT(*) FROM qr_codes WHERE is_used = 0")
    count = cursor.fetchone()[0]
    
    connection.close()
    print(f"Success! {count} tokens have been reset to 0 (Unused).")

if __name__ == "__main__":
    reset_tokens()