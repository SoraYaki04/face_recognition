// FACE RECOGNITION
async function exportImagesfirst() {
    await eel.export_user_face_data(loggedInUserId)();  // loggedInUserId dari login
    
}
async function exportImages() {
    const response = await eel.export_user_face_data(loggedInUserId)();  // loggedInUserId dari login
    alert(response)
}




async function faceRecognition() {
    alert("Program Running - Just Wait..");
    eel.face_recognition()();
}

eel.expose(showAlert);
function showAlert(msg) {
    alert(msg);  
}


// INTERFACE

let loggedInUserId = null;
let loggedInUsername = null;


window.addEventListener("DOMContentLoaded", async () => {
    loggedInUserId = localStorage.getItem("user_id");
    loggedInUsername = localStorage.getItem("username");

    if (loggedInUserId) {
        showPage('page2');
        updateProfile();
        await exportImagesfirst(); 
        showImages(loggedInUserId);
    }
});


// LOGIN
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Tolong isi kedua input");
        return;
    }

    // Panggil fungsi login di backend Python
    const userId = await eel.login(username, password)();

    if (userId) {
        loggedInUserId = userId;  
        loggedInUsername = username;

        localStorage.setItem("user_id", userId);
        localStorage.setItem("username", username);

        updateProfile();
        showPage('page2')
        showImages(loggedInUserId);
        await exportImagesfirst();
        alert("Login Berhasil!");
    } else {
        // Jika login gagal, tampilkan pesan error
        alert("Login Error")
    }
}

// REGISTER
async function register() {
    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;

    if (!username || !password) {
        alert("Tolong isi kedua input");
        return;
    }

    // Panggil fungsi registrasi di backend Python
    const response = await eel.register(username, password)();

    if (response === "Success") {
        alert("Registrasi Berhasi;");
        showPage('page1')
    } else {
        alert("Register Error")
    }
}

function updateProfile() {
    document.getElementById("profileUsername").innerText = loggedInUsername;
}

// LOGOUT
async function logout() {
    loggedInUserId = null;
    loggedInUsername = null;

    localStorage.removeItem("user_id");
    localStorage.removeItem("username");

    await eel.logout()();
    alert("Berhasil logout!");
    showPage("page0"); // Kembali ke halaman login
}


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
    const nama = document.getElementById("imageNama").value;
    const alamat = document.getElementById("imageAlamat").value;
    const tanggalLahir = document.getElementById("imageTanggal").value;
    const fileInput = document.getElementById("imageInput");

    if (!fileInput.files[0] || !nama || !alamat || !tanggalLahir) {
        alert("Isi seluruh input.");
        return;
    }
    
    const file = fileInput.files[0];
    const fileName = file.name;
    const fileExtension = fileName.split('.').pop().toLowerCase(); // Mendapatkan ekstensi file

    if (fileExtension !== 'jpg' && fileExtension !== 'jpeg') {
        alert("Hanya file dengan format JPG yang diperbolehkan.");
        return;
    }


    const arrayBuffer = await file.arrayBuffer();  // Ini menghasilkan data biner mentah
    const byteArray = Array.from(new Uint8Array(arrayBuffer));  // Konversi ke array angka

    // Kirim ke backend
    const response = await eel.upload_image(loggedInUserId, nama, alamat, tanggalLahir, byteArray)();
    alert(response);

    exportImagesfirst();
    showImages(loggedInUserId);
}


// fungsi show images
async function showImages(user_id) {
    let images = await eel.get_uploaded_images(user_id)();
    let imageListDiv = document.getElementById("imageList");
    imageListDiv.innerHTML = "";

    if (images.length === 0) {
        imageListDiv.innerHTML = "<p>Tidak ada gambar yang diunggah.</p>";
        return;
    }

    images.forEach(image => {
        let container = document.createElement("div");
        container.style.display = "inline-block";
        container.style.textAlign = "center";
        container.style.margin = "10px";
    
        // Konversi list[int] ke Uint8Array lalu ke Blob
        const byteArray = new Uint8Array(image.blob_data);
        const imageBlob = new Blob([byteArray], { type: "image/jpeg" });
        const objectURL = URL.createObjectURL(imageBlob);
    
        let img = document.createElement("img");
        img.src = objectURL;
        img.width = 100;
        img.height = 100;
    
        let caption = document.createElement("p");
        caption.innerText = image.filename;
    
        img.addEventListener("click", function () {
            imageClicked(image.filename);
        });
    
        container.appendChild(img);
        container.appendChild(caption);
        imageListDiv.appendChild(container);
    });
    
}


// Fungsi untuk mencari gambar berdasarkan nama
function searchImages() {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    showImagesWithSearch(loggedInUserId, searchTerm);
}

// Fungsi untuk menampilkan gambar berdasarkan hasil pencarian
async function showImagesWithSearch(user_id, searchTerm) {
    let images = await eel.get_uploaded_images(user_id)();
    let imageListDiv = document.getElementById("imageList");
    imageListDiv.innerHTML = "";

    if (images.length === 0) {
        imageListDiv.innerHTML = "<p>Tidak ada gambar yang diunggah.</p>";
        return;
    }

    // Filter gambar berdasarkan nama
    let filteredImages = images.filter(image => image.filename.toLowerCase().includes(searchTerm));

    // Tampilkan gambar yang difilter
    filteredImages.forEach(image => {
        let container = document.createElement("div");
        container.style.display = "inline-block";
        container.style.textAlign = "center";
        container.style.margin = "10px";
    
        // Konversi list[int] ke Uint8Array lalu ke Blob
        const byteArray = new Uint8Array(image.blob_data);
        const imageBlob = new Blob([byteArray], { type: "image/jpeg" });
        const objectURL = URL.createObjectURL(imageBlob);
    
        let img = document.createElement("img");
        img.src = objectURL;
        img.width = 100;
        img.height = 100;
    
        let caption = document.createElement("p");
        caption.innerText = image.filename;
    
        img.addEventListener("click", function () {
            imageClicked(image.filename);
        });
    
        container.appendChild(img);
        container.appendChild(caption);
        imageListDiv.appendChild(container);
    });
}

async function imageClicked(imageName) {
    if (confirm("Apakah Anda yakin ingin menghapus " + imageName + "?")) {
        let response = await eel.delete_image(imageName)();
        alert(response);
        showImages(loggedInUserId); // Refresh setelah delete
    }
}


