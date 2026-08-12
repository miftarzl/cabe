# -*- coding: utf-8 -*-
"""
app.py — Flask API Prototipe Layanan Klasifikasi Kondisi Tanaman Cabai
Skripsi: CNN Transfer Learning MobileNetV2

Endpoint:
    GET  /            -> Tampilan web (upload citra & hasil)
    POST /predict      -> Menerima citra (multipart/form-data, field 'file'),
                          mengembalikan JSON hasil klasifikasi + rekomendasi

Menjalankan (lokal / VS Code):
    1) python -m venv venv && source venv/bin/activate   (Windows: venv\\Scripts\\activate)
    2) pip install -r requirements.txt
    3) Pastikan model/mobilenetv2_cabai_final.h5 dan model/class_indices.json ada
    4) python app.py
    5) Buka http://127.0.0.1:5000
"""

import os
import io
import json
import time
import uuid

import numpy as np
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

from disease_info import get_disease_info

# ------------------------------------------------------------------
# KONFIGURASI
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "mobilenetv2_cabai_final.h5")
CLASS_INDEX_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
IMG_SIZE = (224, 224)   # sesuai input MobileNetV2 pada tahap training
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB

# Ambang batas keyakinan minimum agar prediksi dianggap valid sebagai daun cabai.
# Model TIDAK punya kelas "bukan daun cabai", jadi gambar apa pun yang diunggah
# tetap akan dipaksa masuk ke salah satu dari 5 kelas yang ada. Cara paling
# praktis untuk menolak gambar yang bukan daun cabai (tanpa retraining model)
# adalah menolak hasil prediksi yang keyakinannya terlalu rendah, karena untuk
# gambar yang tidak dikenali model, probabilitasnya cenderung tersebar rata ke
# semua kelas (tidak ada satu kelas yang menonjol).
MIN_CONFIDENCE_THRESHOLD = 0.60  # 60% — ubah sesuai kebutuhan/skripsimu

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ------------------------------------------------------------------
# MUAT MODEL & CLASS MAPPING (sekali saat server start)
# ------------------------------------------------------------------
model = None
idx_to_class = {}

# Urutan default fallback jika class_indices.json belum tersedia
DEFAULT_CLASSES = ["Cercospora", "Healthy", "Mites_and_Thrips", "Nutritional", "Powdery_Mildew"]


def load_ml_assets():
    global model, idx_to_class
    if os.path.exists(MODEL_PATH):
        print(f"[INFO] Memuat model dari: {MODEL_PATH}")
        model = load_model(MODEL_PATH)
    else:
        print(f"[WARNING] Model tidak ditemukan di {MODEL_PATH}.")
        print("          Letakkan file 'mobilenetv2_cabai_final.h5' hasil training Colab di folder 'model/'.")
        model = None

    if os.path.exists(CLASS_INDEX_PATH):
        with open(CLASS_INDEX_PATH, "r") as f:
            raw = json.load(f)
        idx_to_class = {int(k): v for k, v in raw.items()}
    else:
        print("[WARNING] class_indices.json tidak ditemukan, menggunakan urutan kelas default.")
        idx_to_class = {i: c for i, c in enumerate(DEFAULT_CLASSES)}


load_ml_assets()


# ------------------------------------------------------------------
# UTIL
# ------------------------------------------------------------------
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    """Resizing 224x224 + normalisasi [0,1], identik dengan preprocessing saat training."""
    img = pil_img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)  # (1, 224, 224, 3)
    return arr


# Ambang batas rasio piksel "mirip daun" (hijau/kuning/coklat) minimum agar
# gambar dianggap layak diproses. Bekerja SEBELUM gambar masuk ke model CNN,
# jadi bisa langsung menolak foto yang jelas-jelas bukan tumbuhan (foto orang,
# dokumen, layar HP, dsb) tanpa membebani model dengan gambar di luar
# domainnya. Ini heuristik, BUKAN deteksi objek — cukup efektif untuk
# menyaring kasus yang jelas salah, tapi tidak sempurna (mis. foto tanaman
# lain yang hijau tetap bisa lolos tahap ini; itu wajar, karena tahap ini
# hanya penyaring awal, bukan pengganti model).
LEAF_COLOR_RATIO_THRESHOLD = 0.12  # minimal 12% piksel bernuansa daun


def leaf_color_ratio(pil_img: Image.Image) -> float:
    """Hitung proporsi piksel bernuansa hijau/kuning/coklat (khas daun, sehat
    maupun sakit) dalam gambar, menggunakan ruang warna HSV. Sepenuhnya
    offline (PIL + numpy saja, tanpa model/tanpa unduh apa pun)."""
    hsv = np.array(pil_img.convert("RGB").resize((128, 128)).convert("HSV"), dtype=np.int16)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # Skala H pada mode 'HSV' PIL adalah 0-255 (mewakili 0-360 derajat).
    # 11-108 di skala ini ≈ 15°-152° pada skala hue biasa: kuning-oranye,
    # hijau, sampai olive/coklat — rentang warna daun sehat maupun sakit,
    # SEKALIGUS menghindari biru/cyan/magenta (langit, baju, dinding, dsb).
    hue_mask = (h >= 11) & (h <= 108)
    # Saturasi dinaikkan (>=70 dari skala 0-255) untuk membuang warna pucat/
    # low-saturation seperti kulit manusia, dinding krem, kertas kecoklatan —
    # daun (sehat maupun bercak sakit) umumnya cukup jenuh warnanya.
    sat_mask = s >= 70
    val_mask = (v >= 25) & (v <= 250)  # bukan gelap total / putih pekat (overexposed)
    leaf_mask = hue_mask & sat_mask & val_mask
    return float(np.mean(leaf_mask))


def mock_predict(arr: np.ndarray) -> np.ndarray:
    """Digunakan HANYA jika model .h5 belum diletakkan, agar UI tetap dapat didemokan."""
    rng = np.random.default_rng(seed=int(arr.sum() * 1000) % (2**32 - 1))
    logits = rng.random(len(idx_to_class))
    probs = np.exp(logits) / np.sum(np.exp(logits))
    return probs.reshape(1, -1)


# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------------------------------------------
# PWA ROUTES
# ------------------------------------------------------------------
@app.route("/manifest.json")
def manifest():
    """Serve Web App Manifest dari root path (diperlukan oleh PWA)."""
    return send_from_directory(os.path.join(BASE_DIR, "static"), "manifest.json",
                               mimetype="application/manifest+json")


@app.route("/sw.js")
def service_worker():
    """Serve Service Worker dari root path agar scope-nya mencakup seluruh app."""
    response = send_from_directory(os.path.join(BASE_DIR, "static"), "sw.js",
                                   mimetype="application/javascript")
    # Header wajib agar browser menerima SW dari path ini
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/.well-known/assetlinks.json")
def asset_links():
    """Digital Asset Links — diperlukan untuk TWA (Trusted Web Activity).
    SHA-256 fingerprint diisi setelah APK di-generate via PWABuilder."""
    return send_from_directory(os.path.join(BASE_DIR, "static"), "assetlinks.json",
                               mimetype="application/json")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "classes": list(idx_to_class.values())
    })


@app.route("/predict", methods=["POST"])
def predict():
    start_time = time.time()

    if "file" not in request.files:
        return jsonify({"success": False, "error": "Tidak ada berkas citra yang diunggah (field 'file')."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Nama berkas kosong."}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Format berkas tidak didukung. Gunakan PNG/JPG/JPEG/WEBP."}), 400

    try:
        image_bytes = file.read()
        pil_img = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return jsonify({"success": False, "error": "Berkas bukan citra yang valid atau rusak."}), 400

    # Tahap 1: saring cepat berbasis warna — tolak jika gambar jelas-jelas
    # tidak mengandung nuansa warna khas daun (hijau/kuning/coklat).
    ratio = leaf_color_ratio(pil_img)
    if ratio < LEAF_COLOR_RATIO_THRESHOLD:
        return jsonify({
            "success": False,
            "error": (
                "Gambar ini sepertinya bukan foto daun cabai (warna dominan tidak "
                "sesuai daun). Pastikan foto memperlihatkan daun cabai secara close-up, "
                "dengan pencahayaan yang cukup, lalu unggah ulang."
            ),
        }), 400

    # Simpan preview untuk ditampilkan di web (nama unik agar tidak tertimpa)
    unique_name = f"{uuid.uuid4().hex}.jpg"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    pil_img.convert("RGB").save(save_path, format="JPEG", quality=90)

    # Preprocessing identik dengan tahap training
    input_arr = preprocess_image(pil_img)

    # Inferensi
    if model is not None:
        preds = model.predict(input_arr, verbose=0)
    else:
        preds = mock_predict(input_arr)  # fallback demo mode

    probs = preds[0]
    pred_idx = int(np.argmax(probs))
    pred_class = idx_to_class.get(pred_idx, f"class_{pred_idx}")
    confidence = float(probs[pred_idx])

    # Tolak jika keyakinan terlalu rendah — kemungkinan besar gambar bukan
    # daun cabai (mis. foto benda lain), atau kualitas/pencahayaan buruk.
    # Hanya diterapkan saat model asli aktif (bukan mode demo/mock).
    if model is not None and confidence < MIN_CONFIDENCE_THRESHOLD:
        return jsonify({
            "success": False,
            "error": (
                f"Gambar tidak dikenali sebagai daun cabai (keyakinan model hanya "
                f"{round(confidence * 100, 1)}%). Pastikan foto menunjukkan satu daun "
                f"cabai dengan jelas, pencahayaan cukup, dan latar tidak terlalu ramai, "
                f"lalu unggah ulang."
            ),
        }), 400

    # Susun distribusi probabilitas seluruh kelas (untuk ditampilkan sbg bar chart)
    all_probs = [
        {"class": idx_to_class.get(i, f"class_{i}"), "probability": float(p)}
        for i, p in enumerate(probs)
    ]
    all_probs.sort(key=lambda x: x["probability"], reverse=True)

    info = get_disease_info(pred_class)
    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    response = {
        "success": True,
        "demo_mode": model is None,
        "prediction": {
            "class": pred_class,
            "label": info.get("label", pred_class),
            "confidence": round(confidence * 100, 2),
            "kategori": info.get("kategori"),
            "severity": info.get("severity"),
        },
        "probabilities": all_probs,
        "recommendation": {
            "deskripsi": info.get("deskripsi"),
            "perlu_pestisida": info.get("perlu_pestisida"),
            "rekomendasi_residu": info.get("rekomendasi_residu", []),
            "dampak_berlebihan": info.get("dampak_berlebihan", []),
            "dampak_kekurangan": info.get("dampak_kekurangan", []),
            "tindakan": info.get("tindakan", []),
            "analisis_kesehatan_manusia": info.get("analisis_kesehatan_manusia", ""),
        },
        "image_url": url_for("static", filename=f"uploads/{unique_name}"),
        "inference_time_ms": elapsed_ms
    }
    return jsonify(response)


if __name__ == "__main__":
    # host="0.0.0.0" agar dapat diakses saat di-hosting / dari perangkat lain di jaringan lokal
    app.run(host="0.0.0.0", port=5000, debug=True)