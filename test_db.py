import psycopg2

DATABASE_URL = "postgresql://postgres:calm_sphere@localhost:5432/chatbot_db"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile;")  # Check if the table exists
    rows = cursor.fetchall()
    print("✅ Database connection successful! Found records:")
    for row in rows:
        print(row)
except Exception as e:
    print("❌ Database connection failed:", e)
finally:
    if conn:
        cursor.close()
        conn.close()
