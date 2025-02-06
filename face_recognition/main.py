import cv2
from simple_facerec import SimpleFacerec
import eel
import os
import base64

# from services import db

eel.init('gui')

@eel.expose
def face_recognition():

    cap = cv2.VideoCapture(1)

    # encode face from folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
    
    while True:
        ret, frame = cap.read()
        
        # Detect faces
        face_locations, face_name = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_name):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            
            cv2.putText(frame, name,(x1, y1 -10 ), cv2.FONT_HERSHEY_DUPLEX, 1, (200, 0 , 0), 2 )
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 0), 2)
        
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()



# upload images

# Folder tempat gambar disimpan
UPLOAD_FOLDER = "images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fungsi untuk menerima data dari frontend dan menyimpan file
@eel.expose
def upload_image(image_name, image_data):
    try:
        # Decode base64 image
        header, encoded = image_data.split(",", 1)
        file_extension = header.split("/")[-1].split(";")[0]
        decoded_image = base64.b64decode(encoded)

        # Membuat nama file
        file_name = f"{image_name}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Simpan gambar ke folder uploads
        with open(file_path, "wb") as file:
            file.write(decoded_image)

        print(f"Image saved: {file_path}")
        return f"Image uploaded successfully as {file_name}!"
    except Exception as e:
        print(f"Error uploading image: {e}")
        return "Error uploading image!"


# ambil data images
@eel.expose
def get_uploaded_images():
    try:
        images = os.listdir(UPLOAD_FOLDER)
        print("Daftar gambar yang dikirim ke frontend:", images)
        return images
    except Exception as e:
        print(f"Error getting images: {e}")
        return []


# delete images
@eel.expose    
def delete_image(image_name):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, image_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Image deleted: {file_path}")
            return f"Image {image_name} deleted successfully!"
        else:
            return "Image not found!"
    except Exception as e:
        print(f"Error deleting image: {e}")
        return "Error deleting image!"

eel.init('gui', allowed_extensions=['.js', '.html', '.css'])

def App():
    print("Application Running")
    eel.start('index.html', size=(700, 550), position=(0, 0))

def main():
    App()

if __name__ == "__main__" :
    main()

