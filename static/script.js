// ============================================================
// script.js — Klinik Daun Cabai
// Menangani upload citra (galeri) & kamera langsung, pemanggilan
// /predict, dan render hasil
// ============================================================

// ---- Elemen: sumber citra (tabs) ----
const tabUpload = document.getElementById('tab-upload');
const tabCamera = document.getElementById('tab-camera');
const paneUpload = document.getElementById('pane-upload');
const paneCamera = document.getElementById('pane-camera');

// ---- Elemen: unggah dari galeri ----
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const dropzoneEmpty = document.getElementById('dropzone-empty');
const previewImg = document.getElementById('preview-img');

// ---- Elemen: kamera ----
const cameraWrap = document.getElementById('camera-wrap');
const cameraVideo = document.getElementById('camera-video');
const cameraPreview = document.getElementById('camera-preview');
const cameraHint = document.getElementById('camera-hint');
const cameraCanvas = document.getElementById('camera-canvas');
const cameraStartBtn = document.getElementById('camera-start-btn');
const cameraCaptureBtn = document.getElementById('camera-capture-btn');
const cameraSwitchBtn = document.getElementById('camera-switch-btn');
const cameraRetakeBtn = document.getElementById('camera-retake-btn');

// ---- Elemen: form & status ----
const uploadForm = document.getElementById('upload-form');
const submitBtn = document.getElementById('submit-btn');
const btnLabel = submitBtn.querySelector('.btn-label');
const btnSpinner = submitBtn.querySelector('.btn-spinner');
const errorBox = document.getElementById('error-box');

// ---- Elemen: hasil ----
const resultEmpty = document.getElementById('result-empty');
const resultContent = document.getElementById('result-content');
const severityPill = document.getElementById('severity-pill');
const predLabel = document.getElementById('pred-label');
const predKategori = document.getElementById('pred-kategori');
const confidenceValue = document.getElementById('confidence-value');
const confidenceFill = document.getElementById('confidence-fill');
const probsList = document.getElementById('probs-list');
const inferenceMeta = document.getElementById('inference-meta');
const recoDeskripsi = document.getElementById('reco-deskripsi');
const healthAnalysisCard = document.getElementById('health-analysis-card');
const healthAnalysisText = document.getElementById('health-analysis-text');
const listResidu = document.getElementById('list-residu');
const listOver = document.getElementById('list-over');
const listUnder = document.getElementById('list-under');
const listAction = document.getElementById('list-action');
const resetBtn = document.getElementById('reset-btn');

let selectedFile = null;
let activeSource = 'upload'; // 'upload' | 'camera'
let cameraStream = null;
let currentFacingMode = 'environment'; // kamera belakang sbg default (HP)

// ============================================================
// Tab switching: Unggah dari Galeri <-> Gunakan Kamera
// ============================================================
function switchSource(target) {
  activeSource = target;

  tabUpload.classList.toggle('is-active', target === 'upload');
  tabCamera.classList.toggle('is-active', target === 'camera');
  paneUpload.classList.toggle('is-active', target === 'upload');
  paneCamera.classList.toggle('is-active', target === 'camera');

  if (target !== 'camera') {
    stopCamera();
  }
}

tabUpload.addEventListener('click', () => switchSource('upload'));
tabCamera.addEventListener('click', () => switchSource('camera'));

// ============================================================
// Sumber 1: Unggah dari galeri
// ============================================================
dropzone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
  if (e.target.files && e.target.files[0]) handleFile(e.target.files[0]);
});

['dragenter', 'dragover'].forEach(evt => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
  });
});
['dragleave', 'drop'].forEach(evt => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
  });
});
dropzone.addEventListener('drop', (e) => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

function handleFile(file) {
  if (!file.type.startsWith('image/')) {
    showError('Berkas harus berupa citra (PNG/JPG/JPEG/WEBP).');
    return;
  }
  hideError();
  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewImg.hidden = false;
    dropzoneEmpty.hidden = true;
  };
  reader.readAsDataURL(file);

  submitBtn.disabled = false;
}

// ============================================================
// Sumber 2: Kamera langsung (live scan)
// ============================================================
function isSecureContextForCamera() {
  // getUserMedia hanya diizinkan browser pada koneksi aman (HTTPS) atau localhost.
  const host = window.location.hostname;
  return window.isSecureContext || host === 'localhost' || host === '127.0.0.1' || host === '[::1]';
}

async function startCamera(facingMode = currentFacingMode) {
  hideError();
  setCameraBusy(true);
  stopCamera(); // pastikan stream lama ditutup dulu

  if (window.location.protocol === 'file:') {
    showError('Halaman ini dibuka langsung dari berkas (file://), sehingga kamera tidak bisa diakses. Jalankan server terlebih dahulu dengan "python app.py", lalu buka http://127.0.0.1:5000 di browser.');
    setCameraBusy(false);
    return;
  }

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showError('Browser ini tidak mendukung akses kamera. Gunakan Chrome/Safari/Edge versi terbaru, atau pilih "Unggah dari Galeri".');
    setCameraBusy(false);
    return;
  }

  if (!isSecureContextForCamera()) {
    showError('Akses kamera memerlukan koneksi aman. Jika membuka lewat alamat IP jaringan (mis. 192.168.x.x atau 0.0.0.0), gunakan http://127.0.0.1:5000 di komputer ini, atau akses lewat HTTPS.');
    setCameraBusy(false);
    return;
  }

  // Coba dengan facingMode spesifik dahulu (ideal untuk HP); jika perangkat
  // seperti laptop/webcam tidak punya kamera depan/belakang, otomatis fallback
  // ke kamera default apa pun yang tersedia.
  const constraintAttempts = [
    { video: { facingMode: { ideal: facingMode }, width: { ideal: 1280 }, height: { ideal: 1280 } }, audio: false },
    { video: { width: { ideal: 1280 }, height: { ideal: 1280 } }, audio: false },
    { video: true, audio: false }
  ];

  let lastErr = null;
  for (const constraints of constraintAttempts) {
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
      lastErr = null;
      break;
    } catch (err) {
      lastErr = err;
    }
  }

  if (!cameraStream) {
    showError(cameraErrorMessage(lastErr));
    setCameraBusy(false);
    return;
  }

  cameraVideo.srcObject = cameraStream;
  cameraVideo.hidden = false;
  cameraHint.hidden = true;
  cameraPreview.hidden = true;

  cameraStartBtn.hidden = true;
  cameraCaptureBtn.hidden = false;
  cameraRetakeBtn.hidden = true;

  // Beberapa browser tidak langsung menjalankan <video autoplay> setelah
  // srcObject diubah secara dinamis, terutama jika elemen sempat tersembunyi.
  // Panggil play() secara eksplisit dan tunggu metadata siap agar video pasti tampil.
  try {
    await new Promise((resolve) => {
      if (cameraVideo.readyState >= 1) return resolve();
      cameraVideo.onloadedmetadata = () => resolve();
    });
    await cameraVideo.play();
  } catch (playErr) {
    console.warn('Video kamera gagal diputar otomatis:', playErr);
    showError('Kamera aktif, tetapi pratinjau video gagal ditampilkan. Coba klik pada area kamera, atau muat ulang halaman.');
  }

  setCameraBusy(false);

  // Tombol "Ganti Kamera" selalu ditampilkan begitu kamera aktif. Mencoba
  // mendeteksi jumlah kamera lewat enumerateDevices() sebelumnya kurang andal
  // (banyak browser/HP tidak melaporkan jumlah kamera dengan akurat, apalagi
  // sebelum label perangkat tersedia). Jika perangkat memang cuma punya 1
  // kamera, klik tombol ini aman saja — browser otomatis memakai kamera yang
  // sama karena facingMode di atas hanya preferensi ("ideal"), bukan wajib.
  cameraSwitchBtn.hidden = false;
}

function setCameraBusy(isBusy) {
  cameraStartBtn.disabled = isBusy;
  cameraStartBtn.textContent = isBusy ? 'Membuka kamera…' : 'Aktifkan Kamera';
}

function cameraErrorMessage(err) {
  const name = err && err.name;
  if (name === 'NotAllowedError' || name === 'PermissionDeniedError') {
    return 'Izin kamera ditolak. Aktifkan izin kamera untuk situs ini pada pengaturan browser/perangkat, lalu coba lagi.';
  }
  if (name === 'NotFoundError' || name === 'DevicesNotFoundError') {
    return 'Tidak ditemukan kamera pada perangkat ini. Gunakan opsi "Unggah dari Galeri" sebagai gantinya.';
  }
  if (name === 'NotReadableError' || name === 'TrackStartError') {
    return 'Kamera sedang digunakan oleh aplikasi lain. Tutup aplikasi tersebut lalu coba lagi.';
  }
  if (name === 'OverconstrainedError') {
    return 'Konfigurasi kamera tidak didukung perangkat ini. Silakan coba "Ganti Kamera" atau gunakan "Unggah dari Galeri".';
  }
  return 'Tidak dapat mengakses kamera. Pastikan izin kamera diberikan pada browser, lalu coba lagi.';
}

function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  cameraVideo.srcObject = null;
}

cameraStartBtn.addEventListener('click', () => startCamera());

cameraSwitchBtn.addEventListener('click', () => {
  currentFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
  startCamera(currentFacingMode);
});

cameraCaptureBtn.addEventListener('click', () => {
  const videoW = cameraVideo.videoWidth;
  const videoH = cameraVideo.videoHeight;
  if (!videoW || !videoH) return;

  cameraCanvas.width = videoW;
  cameraCanvas.height = videoH;
  const ctx = cameraCanvas.getContext('2d');
  ctx.drawImage(cameraVideo, 0, 0, videoW, videoH);

  cameraCanvas.toBlob((blob) => {
    if (!blob) {
      showError('Gagal mengambil citra dari kamera, silakan coba lagi.');
      return;
    }
    const file = new File([blob], `kamera-${Date.now()}.jpg`, { type: 'image/jpeg' });
    selectedFile = file;

    cameraPreview.src = URL.createObjectURL(blob);
    cameraPreview.hidden = false;
    cameraVideo.hidden = true;

    cameraCaptureBtn.hidden = true;
    cameraSwitchBtn.hidden = true;
    cameraRetakeBtn.hidden = false;

    stopCamera();
    submitBtn.disabled = false;
  }, 'image/jpeg', 0.92);
});

cameraRetakeBtn.addEventListener('click', () => {
  cameraPreview.hidden = true;
  cameraRetakeBtn.hidden = true;
  submitBtn.disabled = true;
  selectedFile = null;
  startCamera(currentFacingMode);
});

// ============================================================
// Submit ke /predict
// ============================================================
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!selectedFile) return;

  setLoading(true);
  hideError();

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const res = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Terjadi kesalahan pada server.');
    }
    renderResult(data);
  } catch (err) {
    showError(err.message || 'Gagal menghubungi server. Pastikan Flask API sedang berjalan.');
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  btnSpinner.hidden = !isLoading;
  btnLabel.textContent = isLoading ? 'Menganalisis…' : 'Jalankan Diagnosis';
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.hidden = false;
}
function hideError() {
  errorBox.hidden = true;
}

// ---------- Render hasil ----------
function severityClass(sev) {
  return 'sev-' + (sev || '').toString().toLowerCase().replace(/\s+/g, '-');
}

function fillList(ulEl, items) {
  ulEl.innerHTML = '';
  if (!items || items.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'Tidak ada catatan khusus.';
    ulEl.appendChild(li);
    return;
  }
  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    ulEl.appendChild(li);
  });
}

function renderResult(data) {
  resultEmpty.hidden = true;
  resultContent.hidden = false;

  const pred = data.prediction;
  const reco = data.recommendation;

  severityPill.textContent = 'Severity: ' + (pred.severity || '-');
  severityPill.className = 'severity-pill ' + severityClass(pred.severity);

  predLabel.textContent = pred.label;
  predKategori.textContent = pred.kategori || '';

  confidenceValue.textContent = pred.confidence.toFixed(2) + '%';
  requestAnimationFrame(() => {
    confidenceFill.style.width = pred.confidence + '%';
  });

  // Distribusi probabilitas
  probsList.innerHTML = '';
  data.probabilities.forEach((p, idx) => {
    const row = document.createElement('div');
    row.className = 'prob-row';

    const name = document.createElement('span');
    name.className = 'prob-name';
    name.textContent = p.class.replace(/_/g, ' ');

    const track = document.createElement('div');
    track.className = 'prob-track';
    const fill = document.createElement('div');
    fill.className = 'prob-fill' + (idx === 0 ? ' is-top' : '');
    fill.style.width = (p.probability * 100).toFixed(1) + '%';
    track.appendChild(fill);

    const val = document.createElement('span');
    val.className = 'prob-val';
    val.textContent = (p.probability * 100).toFixed(1) + '%';

    row.appendChild(name);
    row.appendChild(track);
    row.appendChild(val);
    probsList.appendChild(row);
  });

  inferenceMeta.textContent = `Waktu inferensi: ${data.inference_time_ms} ms`;

  recoDeskripsi.textContent = reco.deskripsi || '';

  if (reco.analisis_kesehatan_manusia) {
    healthAnalysisText.textContent = reco.analisis_kesehatan_manusia;
    healthAnalysisCard.hidden = false;
  } else {
    healthAnalysisCard.hidden = true;
  }

  fillList(listResidu, reco.rekomendasi_residu);
  fillList(listOver, reco.dampak_berlebihan);
  fillList(listUnder, reco.dampak_kekurangan);
  fillList(listAction, reco.tindakan);

  resultContent.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ---------- Reset ----------
resetBtn.addEventListener('click', () => {
  selectedFile = null;

  // reset galeri
  fileInput.value = '';
  previewImg.src = '';
  previewImg.hidden = true;
  dropzoneEmpty.hidden = false;

  // reset kamera
  stopCamera();
  cameraPreview.hidden = true;
  cameraVideo.hidden = true;
  cameraHint.hidden = false;
  cameraStartBtn.hidden = false;
  cameraCaptureBtn.hidden = true;
  cameraSwitchBtn.hidden = true;
  cameraRetakeBtn.hidden = true;

  submitBtn.disabled = true;

  resultContent.hidden = true;
  resultEmpty.hidden = false;
  hideError();
});

// Hentikan kamera jika pengguna berpindah tab/menutup halaman (hemat baterai/privasi)
document.addEventListener('visibilitychange', () => {
  if (document.hidden && activeSource === 'camera') {
    stopCamera();
    if (!cameraPreview.hidden) return; // sudah ada hasil jepretan, biarkan
    cameraStartBtn.hidden = false;
    cameraCaptureBtn.hidden = true;
    cameraSwitchBtn.hidden = true;
    cameraVideo.hidden = true;
    cameraHint.hidden = false;
  }
});
window.addEventListener('beforeunload', stopCamera);