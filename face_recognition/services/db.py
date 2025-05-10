import mysql.connector
import base64
import os
from mysql.connector import Error

# Fungsi untuk membuat koneksi ke database
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",       # Ganti dengan alamat host jika perlu
            user="root",            # Ganti dengan username MySQL Anda
            password="",            # Ganti dengan password MySQL Anda
            database="db_facerecognition"  # Nama database
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Fungsi untuk menutup koneksi dan cursor
def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        
        

# LOGIN / REGISTER
def login(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query untuk mengecek username dan password
        cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return user[0]  # Mengembalikan user_id
        else:
            return None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)
        
def register(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query untuk memeriksa apakah username sudah ada
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists"

        # Query untuk menyimpan data pengguna baru
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        connection.commit()
        return "Success"  # Mengembalikan sukses jika registrasi berhasil
    except Error as e:
        print(f"Error: {e}")
        return "Error during registration"
    finally:
        close_connection(connection, cursor)



# Fungsi untuk mengonversi Base64 ke BLOB
def convert_base64_to_blob(base64_data):
    return base64.b64decode(base64_data)

# Fungsi untuk menyimpan gambar ke database
def save_face_data(user_id, image_data, nama, alamat, tanggal_lahir):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query untuk menyimpan gambar wajah ke tabel face_data
        cursor.execute(
            "INSERT INTO face_data (user_id, image_data, nama, alamat, tanggal_lahir) VALUES (%s, %s, %s, %s, %s)",
            (user_id, image_data, nama, alamat, tanggal_lahir)
        )
        connection.commit()
        
        return True  # Menandakan bahwa data berhasil disimpan
    except Error as e:
        print(f"Error saving data to database: {e}")
        connection.rollback()  # Rollback jika terjadi kesalahan
        return False  # Menandakan bahwa penyimpanan data gagal
    finally:
        close_connection(connection, cursor)

# Fungsi untuk mendapatkan gambar berdasarkan user_id
def get_face_data(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT image_data, nama, alamat, tanggal_lahir 
            FROM face_data 
            WHERE user_id = %s
        """, (user_id,))
        face_data = cursor.fetchall()

        images = []
        for row in face_data:
            image_blob = row[0]
            if image_blob is None:
                continue  # Skip jika data kosong

            try:
                blob_data = list(image_blob)  # Konversi bytes -> list[int]
            except Exception as e:
                print(f"[Error konversi image_blob] {e}")
                blob_data = []

            # Tangani data teks kosong atau None
            nama = str(row[1] or "nama").strip().replace(" ", "_")
            alamat = str(row[2] or "alamat").strip().replace(" ", "_")
            tanggal = str(row[3] or "tanggal").strip().replace(" ", "_")

            filename = f"{nama}_{alamat}_{tanggal}.jpg"

            images.append({
                "filename": filename,
                "blob_data": blob_data
            })

        print(f"[get_face_data] {len(images)} gambar ditemukan untuk user_id {user_id}")
        return images

    except Error as e:
        print(f"[Database Error] {e}")
        return []

    finally:
        close_connection(connection, cursor)



# Fungsi untuk mengekspor semua gambar milik user ke folder 'images'

def export_user_face_data(user_id):
    try:
        print(f"[DEBUG] Memulai ekspor untuk user_id: {user_id}")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT image_data, nama, alamat, tanggal_lahir FROM face_data WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()

        output_folder = "images"
        os.makedirs(output_folder, exist_ok=True)

        logs = []

        for index, (blob, nama, alamat, tanggal_lahir) in enumerate(results):
            if not blob:
                logs.append(f"[{index}] Data kosong - dilewati.")
                continue

            filename = f"{nama}_{alamat}_{tanggal_lahir}.jpg".replace(" ", "_")
            filepath = os.path.join(output_folder, filename)

            if os.path.exists(filepath):
                logs.append(f"{filename} sudah ada, dilewati.")
                continue

            try:
                with open(filepath, "wb") as f:
                    f.write(blob)
                logs.append(f"{filename} berhasil diekspor.")
            except Exception as file_error:
                logs.append(f"{filename} gagal disimpan: {file_error}")

        return "\n".join(logs)

    except Exception as e:
        return f"[ERROR] Ekspor gagal: {e}"

    finally:
        close_connection(connection, cursor)

        
    
UPLOAD_FOLDER = "images" 

def delete_image(image_name):
    try:
        # --- Hapus dari database ---
        connection = get_connection()
        cursor = connection.cursor()

        # Pisahkan nama berdasarkan format "nama_alamat_tanggal.jpg"
        name_parts = image_name.replace(".jpg", "").split("_")
        if len(name_parts) < 3:
            return "Nama file tidak valid!"

        nama = name_parts[0]
        alamat = name_parts[1]
        tanggal_lahir = name_parts[2]

        cursor.execute("""
            DELETE FROM face_data 
            WHERE nama = %s AND alamat = %s AND tanggal_lahir = %s
        """, (nama, alamat, tanggal_lahir))
        connection.commit()

        deleted_from_db = cursor.rowcount > 0

        # --- Hapus file dari folder ---
        file_path = os.path.join(UPLOAD_FOLDER, image_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_from_folder = True
        else:
            deleted_from_folder = False

        # --- Respons ---
        if deleted_from_db and deleted_from_folder:
            return f"Gambar '{image_name}' berhasil dihapus dari database dan folder."
        elif deleted_from_db:
            return f"Gambar '{image_name}' hanya dihapus dari database (file tidak ditemukan)."
        elif deleted_from_folder:
            return f"Gambar '{image_name}' hanya dihapus dari folder (data DB tidak ditemukan)."
        else:
            return f"Tidak ditemukan gambar bernama '{image_name}'."

    except Exception as e:
        print(f"Error deleting image: {e}")
        return "Terjadi kesalahan saat menghapus gambar!"
    finally:
        close_connection(connection, cursor)