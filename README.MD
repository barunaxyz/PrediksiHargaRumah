# 🏠 Prediksi Harga Rumah Jakarta Selatan

## 🚀 Quick Start (Recommended)

Cara termudah untuk menjalankan aplikasi adalah menggunakan **Docker**.

### Prerequisites
- Docker Desktop terinstall dan berjalan.

### Langkah-Langkah
1.  **Clone Repository**
    ```bash
    git clone https://github.com/barunaxyz/PrediksiHargaRumah.git
    cd PrediksiHargaRumah
    ```

2.  **Jalankan Aplikasi**
    *   **Windows (Double Click):**
        Double click file `start_app.bat`.
    
    *   **Terminal:**
        ```bash
        docker-compose up --build
        ```

3.  **Akses Aplikasi**
    - **Frontend (Pengguna):** Buka [http://localhost:8501](http://localhost:8501)
    - **API (Backend):** Buka [http://localhost:5000](http://localhost:5000)

---

## 🛠️ Manual Installation (Tanpa Docker)

Jika Anda ingin menjalankan secara manual satu per satu:

1.  **Setup Environment**
    ```bash
    # Install dependencies
    pip install -r api/requirements.txt
    pip install -r frontend/requirements.txt
    ```

2.  **Jalankan API (Terminal 1)**
    ```bash
    # PENTING: Jalankan dari root directory
    python api/app.py
    ```

3.  **Jalankan Frontend (Terminal 2)**
    ```bash
    # PENTING: Jalankan dari root directory
    streamlit run frontend/app.py
    ```

## 📂 Struktur Project

- `api/`: Backend Flask untuk melayani prediksi dan metrik.
- `frontend/`: Tampilan UI menggunakan Streamlit.
- `models/`: Tempat penyimpanan file model (`.pkl`) dan metrik (`.json`).
- `data/`: Dataset mentah dan hasil cleaning.
- `scripts/`: Script helper untuk training ulang dan maintenance.

## 🤖 Otomatisasi
Repository ini dilengkapi GitHub Actions yang akan **otomatis melakukan training ulang** setiap minggu (Minggu pukul 00:00 UTC) untuk menjaga model tetap update dengan data terbaru.
