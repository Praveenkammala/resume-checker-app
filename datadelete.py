import sqlite3

def clear_evaluations_db():
    try:
        conn = sqlite3.connect('results.db')
        cursor = conn.cursor()

        # SQL command to delete all records from the table
        cursor.execute("DELETE FROM evaluations")
        
        # Commit the changes to the database file
        conn.commit()
        print("The results.db database has been successfully cleared.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    clear_evaluations_db()