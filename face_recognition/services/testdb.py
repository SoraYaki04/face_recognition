from db import connect_db

try:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT db_facerecognition();")
    result = cursor.fetchone()
    print("Koneksi berhasil ke database:", result[0])
    conn.close()
except Exception as e:
    print("Koneksi gagal:", e)