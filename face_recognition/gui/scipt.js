// FACE RECOGNITION

async function faceRecognition() {
    alert("Program Running - Just Wait..");
    eel.face_recognition()();
}

eel.expose(showAlert);
function showAlert(msg) {
    alert(msg);  
}


// INTERFACE

function showPage(page) {
    document.querySelectorAll('.page').forEach((p) => {
        p.style.display = 'none';
    });
    document.getElementById(page).style.display = 'block';
}

function showPopup() {
    const popup = document.getElementById('popup');

    if (popup.style.display === 'block') {
        document.getElementById('popup').style.display = 'none';
    } else {
        document.getElementById('popup').style.display = 'block';
    }
}


// IMAGES

// Fungsi untuk mengunggah gambar
async function uploadImage() {
    const imageInput = document.getElementById("imageInput");
    const imageName = document.getElementById("imageName").value.trim();

// Validasi input
if (!imageName) {
    alert("Please enter an image name.")
}

if (!imageInput.files.length) {
    alert("Please select an image file.")
}


const file = imageInput.files[0];
const reader = new FileReader();

reader.onload = async function () {
    const base64Image = reader.result;

    // Kirim data ke backend menggunakan Eel
    const response = await eel.upload_image(imageName, base64Image)();
    alert(response);
};

reader.readAsDataURL(file);
}


// fungsi show images
async function showImages() {
    let images = await eel.get_uploaded_images()();
    console.log("Daftar gambar:", images);

    let imageListDiv = document.getElementById("imageList");
    imageListDiv.innerHTML = ""; // Kosongkan dulu sebelum menampilkan gambar baru
    
    if (images.length === 0) {
        imageListDiv.innerHTML = "<p>Tidak ada gambar yang diunggah.</p>";
        return;
    }

    images.forEach(image => {
        let img = document.createElement("img");
        img.src = "images/" + image; 
        img.width = 100;
        img.height = 100; 
        img.style.margin = "10px";
        img.onclick = function() { imageClicked(image); };

        console.log("Menampilkan gambar:", img.src);
        imageListDiv.appendChild(img);
    });
}

async function imageClicked(imageName) {
    if (confirm("Apakah Anda yakin ingin menghapus " + imageName + "?")) {
        let response = await eel.delete_image(imageName)();
        alert(response);
        showImages(); // Refresh daftar gambar setelah dihapus
    }
}
