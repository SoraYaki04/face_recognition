# 🧑‍💻 Face Recognition App

## 1. Project Description

The **Face Recognition App** is a Python-based application designed to recognize faces from a camera feed in real time. When a face is detected, the app overlays the recognized person’s **name**, **address**, and **age** directly onto the camera display. This project is ideal for demonstration purposes, events, or environments where quick identification is required.

## 2. Key Features 🚀

- **Real-Time Face Recognition:** Detects and identifies faces from a live camera feed.
- **Info Overlay:** Displays the recognized person’s name, address, and age on the video stream.
- **Simple UI:** Easy-to-use interface for quick deployment and testing.

## 3. Installation & Setup ⚙️

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SoraYaki04/face_recognition.git
   cd face_recognition
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL Database**
   - Ensure MySQL is installed and running.
   - Create the database:
     ```sql
     CREATE DATABASE db_facerecognition;
     ```
   - Import the schema:
     ```bash
     mysql -u <username> -p db_facerecognition < db_facerecognition.sql
     ```
   - Update database credentials in your config or code as needed.

## 4. Usage 🎥

- **Start the Application**
  ```bash
  python main.py
  ```
- **Workflow:**
  1. The app activates your camera. 📷
  2. When a face is detected and recognized, the person’s name, address, and age appear on the video stream.
  3. If the face is not recognized, no information is shown.


## 5. Example Output 🖼️

- **On successful recognition:**  
  The video feed will show a box around the face with text like:
  ```
  Name: John Doe
  Address: 123 Main St
  Age: 28
  ```

- **On unrecognized face:**  
  No overlay or a message like “Unknown” appears.

  ---

> For more details or troubleshooting, visit the [GitHub repository](https://github.com/SoraYaki04/face_recognition).  
> Made with 💙 by SoraYaki04
