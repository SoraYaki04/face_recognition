import cv2
from simple_facerec import SimpleFacerec
import eel
import os
import gc
from services import db  # Mengimpor fungsi dari file db.py

eel.init('gui')

@eel.expose
def face_recognition():

    cap = cv2.VideoCapture(1)

    # encode face from folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
    
    while True:
        ret, frame = cap.read()
        
        # deteksi wajah
        face_locations, face_data = sfr.detect_known_faces(frame)

        for face_loc, text in zip(face_locations, face_data):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            
            cv2.putText(frame, text,(x1 -150 , y1 -10 ), cv2.FONT_HERSHEY_DUPLEX, 0.7, (200, 0 , 0), 2 )
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 0), 2)
        
        cv2.imshow("Face Recognition", frame)

        # Tambahkan garbage collection setiap 50 frame
        if cv2.waitKey(10) % 50 == 0:
            gc.collect()  # Membersihkan memory
        
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()



# LOGIN / REGISTER /LOGOUT
current_user_id = None

@eel.expose
def login(username, password):
    global current_user_id
    user_id = db.login(username, password)
    if user_id:
        current_user_id = user_id
        return user_id  # Kembalikan user_id, bukan True
    return None  # Return None jika login gaga

@eel.expose
def register(username, password):
    return db.register(username, password)

@eel.expose
def logout():
    global current_user_id
    current_user_id = None
    clear_images_folder() 
    return True

@eel.expose
def is_logged_in():
    return current_user_id is not None

# UPLOAD IMAGE
UPLOAD_FOLDER = "images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@eel.expose
def upload_image(user_id, nama, alamat, tanggal_lahir, byte_array):
    try:
        image_blob = bytes(byte_array)
        success = db.save_face_data(user_id, image_blob, nama, alamat, tanggal_lahir)
        return "Upload berhasil!" if success else "Gagal upload"
    except Exception as e:
        return f"Terjadi error: {e}"    
    
@eel.expose
def get_uploaded_images(user_id):
    print(f"[DEBUG] showImages untuk user_id: {user_id}")
    return db.get_face_data(user_id);

@eel.expose    
def delete_image(image_name):
    print(f"[DEBUG] Delete untuk image: {image_name}")
    return db.delete_image(image_name);
    
@eel.expose
def export_user_face_data(user_id):
    print(f"[DEBUG] Export untuk user_id: {user_id}")
    return db.export_user_face_data(user_id)    

# @eel.expose
# def export_user_face_data(user_id, folder_path='images'):
#     try:
#         # Pastikan folder tujuan ada
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)

#         # Koneksi ke database
#         conn = get_connection()
#         cursor = conn.cursor()

#         # Query untuk mengambil data gambar berdasarkan user_id
#         cursor.execute("""
#             SELECT nama, alamat, tanggal_lahir, image_data 
#             FROM face_data 
#             WHERE user_id = %s
#         """, (user_id,))
#         data = cursor.fetchall()

#         # Jika tidak ada data untuk user_id tersebut
#         if not data:
#             return f"Tidak ada data untuk user_id: {user_id}"

#         exported = 0
#         skipped = 0

#         # Proses setiap baris data
#         for row in data:
#             nama, alamat, tanggal_lahir, image_blob = row
#             # Buat nama file berdasarkan data
#             filename = f"{nama}_{alamat}_{tanggal_lahir}"
#             # Bersihkan nama file agar aman untuk sistem file
#             filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
            
#             if not filename.lower().endswith('.jpg'):
#                 filename += '.jpg'
                
#             filepath = os.path.join(folder_path, filename)

#             # Cek apakah file sudah ada
#             if os.path.exists(filepath):
#                 skipped += 1
#                 continue

#             # image_blob adalah data BLOB (biner), jadi langsung simpan ke file
#             with open(filepath, 'wb') as f:
#                 f.write(image_blob)  # Menulis data BLOB ke file
#                 exported += 1

#         # Kembalikan hasil ekspor
#         return f"Export selesai. Berhasil: {exported}, Dilewati (sudah ada): {skipped}"

#     except Exception as e:
#         # Tangani jika ada kesalahan
#         return f"Terjadi kesalahan saat ekspor: {e}"
    
#     finally:
#         # Pastikan koneksi ditutup setelah eksekusi
#         close_connection(conn, cursor)

        
        
def clear_images_folder():
    folder = "images"
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


eel.init('gui', allowed_extensions=['.js', '.html', '.css'])

def App():
    print("Application Running")
    eel.start('index.html', size=(700, 550), position=(0, 0))

def main():
    clear_images_folder() 
    App()

if __name__ == "__main__" :
    main()
