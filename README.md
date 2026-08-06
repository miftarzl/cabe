# 🌶️ Klinik Daun Cabai — Prototipe Layanan Klasifikasi Kondisi Tanaman Cabai

Prototipe layanan berbasis **Flask API** untuk mengklasifikasikan 5 kondisi daun cabai
(*Powdery Mildew, Cercospora, Mites and Thrips, Nutritional, Healthy*) menggunakan model
**CNN Transfer Learning MobileNetV2**, dilengkapi rekomendasi residu pestisida, dampak
jika berlebihan/kekurangan, dan tindakan yang harus dilakukan — sesuai fase **Deployment
CRISP-DM** pada skripsi.

## Struktur Proyek

```
flask_app/
├── app.py                 # Backend Flask (endpoint / dan /predict)
├── disease_info.py        # Basis pengetahuan: rekomendasi & dampak per kelas
├── requirements.txt
├── model/
│   ├── mobilenetv2_cabai_final.h5   # <- letakkan hasil training dari Colab di sini
│   ├── class_indices.json           # <- letakkan hasil training dari Colab di sini
│   └── README.txt
├── templates/
│   └── index.html         # Tampilan web (upload + hasil)
└── static/
    ├── style.css
    ├── script.js
    └── uploads/            # penyimpanan sementara citra yang diunggah pengguna
```

## Alur Kerja End-to-End

1. **Training model** dijalankan di **Google Colab** menggunakan notebook
   `Training_MobileNetV2_Cabai_Colab.ipynb` (folder `colab/`), mengikuti tahapan
   Data Preparation → Modeling (Feature Extraction + Fine-Tuning) → Evaluation.
2. Notebook meng-export dua berkas: `mobilenetv2_cabai_final.h5` dan `class_indices.json`.
3. Kedua berkas dipindahkan ke folder `flask_app/model/` pada proyek **VS Code** ini.
4. Aplikasi Flask dijalankan secara lokal, lalu dapat di-deploy ke layanan hosting
   (Render, Railway, PythonAnywhere, VPS, dsb).

## Menjalankan di VS Code (Lokal)

```bash
cd flask_app

# 1. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependensi
pip install -r requirements.txt

# 3. Pastikan model sudah ada di model/mobilenetv2_cabai_final.h5
#    (jika belum ada, aplikasi tetap bisa dijalankan dalam MODE DEMO)

# 4. Jalankan server
python app.py
```

Buka browser ke **http://127.0.0.1:5000**

> Tanpa model `.h5`, aplikasi otomatis berjalan dalam **MODE DEMO** (probabilitas acak)
> agar tampilan web tetap dapat diuji coba sebelum model tersedia — akan muncul
> banner peringatan kuning pada hasil diagnosis.

## Endpoint API

| Method | Endpoint   | Deskripsi                                                    |
|--------|-----------|----------------------------------------------------------------|
| GET    | `/`        | Halaman web utama (upload citra & tampilan hasil)              |
| GET    | `/health`  | Status server & daftar kelas yang dikenali model                |
| POST   | `/predict` | Menerima citra (`multipart/form-data`, field `file`), mengembalikan JSON hasil klasifikasi + rekomendasi |

Contoh respons `/predict`:
```json
{
  "success": true,
  "demo_mode": false,
  "prediction": {
    "class": "Cercospora",
    "label": "Cercospora (Bercak Daun)",
    "confidence": 92.15,
    "kategori": "Penyakit Jamur",
    "severity": "tinggi"
  },
  "probabilities": [ { "class": "Cercospora", "probability": 0.9215 }, ... ],
  "recommendation": {
    "deskripsi": "...",
    "perlu_pestisida": true,
    "rekomendasi_residu": [ "..." ],
    "dampak_berlebihan": [ "..." ],
    "dampak_kekurangan": [ "..." ],
    "tindakan": [ "..." ]
  },
  "image_url": "/static/uploads/xxxx.jpg",
  "inference_time_ms": 245.3
}
```

## Deploy ke Hosting (opsional)

Gunakan **gunicorn** (sudah termasuk pada `requirements.txt`) sebagai WSGI server produksi:

```bash
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

Untuk platform seperti Render/Railway, cukup arahkan **Start Command** ke perintah di atas
dan pastikan berkas model `.h5` (± beberapa puluh MB) ikut ter-upload/di-mount, atau
diunduh saat build dari Google Drive/Storage eksternal karena ukurannya biasanya melebihi
batas repositori git standar.

## Catatan Penting

- Rekomendasi residu pestisida bersifat **edukatif/deskriptif** sesuai lingkup penelitian
  (analisis dampak dilakukan secara deskriptif berdasarkan literatur), **bukan pengganti**
  anjuran resmi Pengendalian Hama Terpadu (PHT) atau label produk pestisida berizin.
- Preprocessing pada `app.py` (`resize 224x224` + normalisasi `/255`) **harus identik**
  dengan preprocessing saat training di notebook Colab agar hasil prediksi valid.
- Urutan kelas pada `class_indices.json` **wajib sama** dengan urutan saat `train_generator`
  dibuat di notebook — jangan diubah manual.
