import face_recognition
import cv2
import os
import glob
import numpy as np
import datetime
import eel


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_data = []
        self.user_data = {}
        self.message = None

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """

        # Ambil semua file gambar di folder
        image_files = glob.glob(os.path.join(images_path, "*.*"))
        print("{} gambar ditemukan.".format(len(image_files)))

        self.message = "{} gambar ditemukan.".format(len(image_files))
        eel.showAlert(self.message)
        eel.sleep(1)

        # Store image encoding and names
        for img_path in image_files:

            # Ambil nama file tanpa ekstensi
            filename = os.path.basename(img_path)
            name_ext = os.path.splitext(filename)[0]  # Contoh: "John_Jakarta_2000-05-02"

            # Pastikan format nama file benar
            if name_ext.count("_") != 2:
                print(f"Skipping invalid filename format: {filename}")
                continue

            name, address, tanggal = name_ext.split("_")

            # Ubah tanggal menjadi umur
            try:
                tanggal_lahir = datetime.datetime.strptime(tanggal, "%Y-%m-%d")
                today = datetime.date.today()
                umur = today.year - tanggal_lahir.year - ((today.month, today.day) < (tanggal_lahir.month, tanggal_lahir.day))
            except ValueError:
                print(f"Format tanggal salah: {tanggal}")
                continue

            # Load gambar
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Encode wajah
            encodings = face_recognition.face_encodings(rgb_img)
            if len(encodings) > 0:
                img_encoding = encodings[0]
                self.known_face_encodings.append(img_encoding)
                self.known_face_data.append({"Nama": name, "Alamat": address, "Umur": umur})
            else:
                print(f"Tidak ditemukan wajah di {img_path}")

        print("Gambar dimuat")
        self.message = "Gambar dimuat"
        eel.showAlert(self.message)

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_data = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            address = "Unknown"
            age = "Unknown"

            if len(self.known_face_encodings) == 0:
                face_data.append("Unknown, Unknown, Unknown")
                continue

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            if len(face_distances) == 0:
                face_data.append("Unknown, Unknown, Unknown")
                continue

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                matched_data = self.known_face_data[best_match_index]
                name, address, age = matched_data["Nama"], matched_data["Alamat"], matched_data["Umur"]

            face_data.append(f"Nama : {name}, Alamat : {address}, Umur : {age}")

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_data
