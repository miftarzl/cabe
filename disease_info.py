# -*- coding: utf-8 -*-
"""
disease_info.py
Basis pengetahuan hasil klasifikasi kondisi tanaman cabai (Capsicum annuum L.)
Berisi: deskripsi kondisi, rekomendasi residu pestisida, dampak jika berlebihan/kekurangan,
serta tindakan yang harus dilakukan petani.

Disusun berdasarkan tinjauan literatur pada skripsi:
"Klasifikasi Kondisi Tanaman Cabai berbasis CNN Transfer Learning MobileNetV2"
(Bab II & III — Powdery Mildew, Cercospora, Mites and Thrips, Nutritional, Healthy)

CATATAN PENTING:
Rekomendasi di bawah ini bersifat EDUKATIF/DESKRIPTIF sebagai prototipe penelitian,
BUKAN pengganti anjuran resmi Pengendalian Hama Terpadu (PHT) dari penyuluh
pertanian atau label produk pestisida terdaftar Kementerian Pertanian RI.
Dosis aktual WAJIB mengikuti label kemasan produk yang terdaftar/berizin.
"""

DISEASE_INFO = {
    "Powdery_Mildew": {
        "label": "Powdery Mildew (Embun Tepung)",
        "kategori": "Penyakit Jamur",
        "severity": "tinggi",
        "deskripsi": (
            "Infeksi jamur biotrofik obligat Leveillula taurica yang menyerang jaringan "
            "mesofil daun melalui stomata, ditandai lapisan tepung putih keabu-abuan di "
            "permukaan bawah daun disertai klorosis di permukaan atas."
        ),
        "perlu_pestisida": True,
        "rekomendasi_residu": [
            "Fungisida berbahan aktif Sulfur 80% WP dosis 2–3 g/liter air (kontak, risiko residu rendah).",
            "Alternatif fungisida sistemik: Difenokonazol 250 EC atau Trifloksistrobin, sesuai dosis label.",
            "Lakukan rotasi bahan aktif setiap 2–3 kali aplikasi untuk mencegah resistensi jamur.",
            "Interval penyemprotan 7 hari, dihentikan minimal 7–14 hari sebelum panen (Pre-Harvest Interval)."
        ],
        "dampak_berlebihan": [
            "Residu fungisida terakumulasi pada buah cabai yang dipanen dan berpotensi masuk ke rantai makanan.",
            "Paparan berkepanjangan berisiko menimbulkan gangguan sistem saraf, tekanan darah tinggi, dan anemia pada manusia.",
            "Resistensi patogen meningkat sehingga fungisida menjadi kurang efektif pada musim berikutnya.",
            "Membunuh mikroorganisme dan musuh alami yang menguntungkan di sekitar tanaman."
        ],
        "dampak_kekurangan": [
            "Jika tidak ditangani, infeksi dapat menyebabkan kehilangan hasil panen hingga 50%.",
            "Fotosintesis menurun akibat lapisan tepung menutupi permukaan daun.",
            "Daun gugur sebelum waktunya dan spora menyebar cepat ke tanaman sekitar."
        ],
        "tindakan": [
            "Pangkas dan musnahkan (bakar/kubur) daun yang terinfeksi berat agar spora tidak menyebar.",
            "Semprotkan fungisida pada pagi atau sore hari saat suhu tidak terlalu tinggi.",
            "Perbaiki jarak tanam dan sirkulasi udara untuk menurunkan kelembaban mikro di sekitar daun.",
            "Lakukan pemantauan ulang setiap 7 hari untuk menilai efektivitas pengendalian."
        ],
        "analisis_kesehatan_manusia": (
            "Leveillula taurica adalah jamur obligat yang tidak menghasilkan mikotoksin dan "
            "tidak menginfeksi manusia, sehingga buah cabai yang terserang embun tepung pada "
            "dasarnya tidak berbahaya bila dikonsumsi. Risiko kesehatan justru muncul secara "
            "tidak langsung dari sisi pengendalian: penyemprotan fungisida berbahan aktif sulfur "
            "atau golongan triazol (Difenokonazol) yang tidak mengikuti Pre-Harvest Interval dapat "
            "meninggalkan residu pada permukaan buah. Paparan residu sulfur berlebih dapat memicu "
            "iritasi saluran napas dan kulit pada petani penyemprot, sementara paparan golongan "
            "triazol dalam jangka panjang dan berulang dikaitkan pada literatur toksikologi dengan "
            "potensi gangguan fungsi hati dan sistem endokrin. Oleh karena itu, kepatuhan terhadap "
            "dosis anjuran, penggunaan alat pelindung diri (APD) saat aplikasi, serta pencucian "
            "buah sebelum konsumsi tetap menjadi langkah mitigasi utama."
        )
    },

    "Cercospora": {
        "label": "Cercospora (Bercak Daun)",
        "kategori": "Penyakit Jamur",
        "severity": "tinggi",
        "deskripsi": (
            "Bercak daun yang disebabkan oleh jamur Cercospora capsici, ditandai bercak "
            "kecil bulat berwarna coklat dengan area klorosis di sekelilingnya yang dapat "
            "berkembang menjadi nekrosis."
        ),
        "perlu_pestisida": True,
        "rekomendasi_residu": [
            "Fungisida kontak berbahan aktif Mankozeb 80% WP dosis 2 g/liter air.",
            "Alternatif fungisida sistemik: Klorotalonil atau Azoksistrobin sesuai dosis label.",
            "Kombinasikan aplikasi kontak dan sistemik secara bergantian (rotasi) untuk mencegah resistensi.",
            "Interval semprot 7–10 hari, hentikan sesuai Pre-Harvest Interval pada label produk."
        ],
        "dampak_berlebihan": [
            "Akumulasi residu fungisida pada buah dapat menurunkan kualitas dan nilai jual/ekspor komoditas cabai.",
            "Paparan residu organoklorin/karbamat berkepanjangan berisiko memicu penyakit kronis pada konsumen.",
            "Biaya produksi petani meningkat tanpa manfaat pengendalian tambahan yang signifikan."
        ],
        "dampak_kekurangan": [
            "Tingkat serangan di dataran tinggi dapat mencapai 50,89% apabila tidak ditangani.",
            "Bercak berkembang menjadi nekrosis luas yang menyebabkan daun rontok.",
            "Kerontokan daun masif menurunkan kapasitas fotosintesis dan hasil panen."
        ],
        "tindakan": [
            "Lakukan sanitasi lahan dengan membersihkan sisa tanaman dan gulma inang jamur.",
            "Buang dan musnahkan daun yang menunjukkan gejala bercak sejak dini.",
            "Terapkan rotasi tanaman non-Solanaceae pada musim berikutnya.",
            "Hindari penyiraman/kelembaban berlebih pada daun, terutama pada sore-malam hari."
        ],
        "analisis_kesehatan_manusia": (
            "Cercospora capsici menyerang jaringan daun dan umumnya tidak menjalar ke buah matang "
            "yang dipanen, sehingga bercak daun itu sendiri bukan ancaman langsung bagi konsumen. "
            "Namun demikian, tanaman yang stres akibat infeksi berat cenderung disemprot fungisida "
            "kontak (Mankozeb) atau sistemik (Klorotalonil, Azoksistrobin) secara lebih intensif. "
            "Mankozeb mengandung senyawa etilen-tiourea (ETU) sebagai produk degradasinya, yang pada "
            "paparan kronis berulang telah diasosiasikan dengan gangguan fungsi tiroid pada studi "
            "hewan coba, sedangkan Klorotalonil tergolong bahan dengan potensi karsinogenik pada "
            "paparan dosis tinggi jangka panjang menurut beberapa badan regulasi lingkungan. Bagi "
            "petani, kontak kulit dan inhalasi saat penyemprotan adalah jalur paparan tertinggi, "
            "sedangkan bagi konsumen risiko utamanya adalah residu pada permukaan buah jika masa "
            "tunggu (Pre-Harvest Interval) tidak dipatuhi. Mencuci buah dengan air mengalir dan "
            "mengupas bila memungkinkan dapat menurunkan residu permukaan secara signifikan."
        )
    },

    "Mites_and_Thrips": {
        "label": "Mites and Thrips (Tungau dan Trips)",
        "kategori": "Hama",
        "severity": "sedang-tinggi",
        "deskripsi": (
            "Serangan hama penghisap cairan sel daun oleh tungau (Tetranychus urticae) "
            "dan trips (Thrips parvispinus), menyebabkan daun melengkung, menggulung, "
            "dan berubah warna coklat tembaga."
        ),
        "perlu_pestisida": True,
        "rekomendasi_residu": [
            "Akarisida/insektisida selektif berbahan aktif Abamektin 18 EC dosis 0,5–1 ml/liter air.",
            "Alternatif: Spiromesifen atau Fipronil sesuai dosis label untuk mengendalikan thrips.",
            "Rotasi bahan aktif tiap 2–3 aplikasi untuk mencegah resistensi hama.",
            "Prioritaskan agens pengendali biologis (predator Amblyseius sp.) untuk menekan penggunaan kimia."
        ],
        "dampak_berlebihan": [
            "Residu insektisida golongan organofosfat/karbamat terakumulasi pada buah cabai.",
            "Paparan berkepanjangan pada petani/konsumen berisiko menimbulkan gangguan sistem saraf dan keracunan kronis.",
            "Populasi musuh alami (predator tungau/trips) ikut terbunuh sehingga hama justru re-infestasi lebih cepat.",
            "Resistensi hama terhadap bahan aktif meningkat akibat aplikasi berulang tanpa rotasi."
        ],
        "dampak_kekurangan": [
            "Populasi hama meningkat cepat dan dapat menurunkan hasil panen sebesar 12–74%.",
            "Daun yang rusak menghambat fotosintesis dan pertumbuhan buah.",
            "Serangan lanjut dapat menyebabkan kematian tanaman pada kasus berat."
        ],
        "tindakan": [
            "Pasang perangkap likat berwarna kuning/biru untuk memantau populasi trips secara berkala.",
            "Semprot hanya ketika populasi melewati ambang ekonomi, bukan terjadwal rutin.",
            "Kombinasikan dengan pengendalian biologis (predator alami) dan mulsa reflektif.",
            "Buang bagian tanaman yang terserang parah untuk mengurangi sumber infestasi baru."
        ],
        "analisis_kesehatan_manusia": (
            "Tungau dan trips tidak menularkan penyakit ke manusia dan tidak mencemari buah secara "
            "biologis, sehingga risiko kesehatan pada kondisi ini hampir sepenuhnya berasal dari "
            "bahan kimia pengendaliannya. Abamektin bersifat neurotoksik pada serangga dengan "
            "mekanisme yang juga dapat memengaruhi sistem saraf mamalia pada paparan dosis tinggi, "
            "sehingga inhalasi uap semprotan tanpa masker berisiko menimbulkan pusing, mual, atau "
            "gangguan koordinasi otot pada petani aplikator. Fipronil, sebagai alternatif, tergolong "
            "moderately hazardous oleh WHO dan residunya yang persisten pada tanah maupun permukaan "
            "buah dapat terakumulasi bila aplikasi dilakukan terlalu sering. Karena hama ini "
            "berkembang biak cepat dan mendorong penyemprotan berulang, pendekatan Pengendalian Hama "
            "Terpadu (ambang ekonomi, predator alami) sangat penting untuk menekan frekuensi paparan "
            "bahan kimia baik bagi petani maupun konsumen akhir."
        )
    },

    "Nutritional": {
        "label": "Nutritional (Defisiensi Nutrisi)",
        "kategori": "Kondisi Fisiologis (Bukan Penyakit/Hama)",
        "severity": "sedang",
        "deskripsi": (
            "Kondisi fisiologis akibat kekurangan unsur hara makro (Nitrogen, Fosfor, "
            "atau Kalium), bukan disebabkan oleh infeksi jamur, bakteri, virus, maupun hama."
        ),
        "perlu_pestisida": False,
        "rekomendasi_residu": [
            "TIDAK memerlukan aplikasi pestisida/fungisida/insektisida — akar masalahnya bukan hama/penyakit.",
            "Berikan pemupukan sesuai unsur yang defisien: Nitrogen (Urea/ZA) untuk klorosis daun tua, "
            "Fosfor (SP-36) untuk daun keunguan, atau Kalium (KCl) untuk nekrosis tepi daun.",
            "Gunakan pupuk daun (foliar fertilizer) untuk penyerapan lebih cepat pada kasus defisiensi akut.",
            "Lakukan uji tanah (soil test) untuk memastikan unsur hara yang benar-benar kurang sebelum pemupukan."
        ],
        "dampak_berlebihan": [
            "Jika keliru diberi pestisida (bukan pupuk): pemborosan biaya tanpa manfaat, karena akar masalah bukan hama/patogen.",
            "Residu kimia pestisida yang tidak perlu tetap tertinggal pada buah meski tidak menyelesaikan defisiensi.",
            "Tanaman semakin stres akibat kombinasi defisiensi nutrisi dan potensi fitotoksisitas dari bahan kimia yang tidak relevan.",
            "Inilah pola kesalahan penanganan utama yang ingin dicegah oleh sistem klasifikasi ini — salah membedakan penyakit dengan defisiensi nutrisi mendorong penyemprotan pestisida yang tidak tepat sasaran."
        ],
        "dampak_kekurangan": [
            "Jika defisiensi nutrisi tidak segera dikoreksi dengan pemupukan, hasil panen dapat menurun 5–30%.",
            "Klorosis dapat menyebar dari daun tua ke daun muda dan menghambat pembentukan buah.",
            "Sering keliru diidentifikasi sebagai infeksi jamur/virus sehingga penanganan menjadi tidak tepat sasaran."
        ],
        "tindakan": [
            "JANGAN menyemprotkan pestisida — arahkan penanganan ke pemupukan sesuai unsur yang kurang.",
            "Amati pola gejala: klorosis daun tua menyebar → indikasi kekurangan Nitrogen; daun keunguan → Fosfor; nekrosis tepi daun → Kalium.",
            "Lakukan pemupukan susulan/pupuk daun dan evaluasi perbaikan gejala setelah 1–2 minggu.",
            "Perbaiki juga pH tanah dan drainase, karena keduanya mempengaruhi ketersediaan unsur hara bagi akar."
        ],
        "analisis_kesehatan_manusia": (
            "Defisiensi hara bukan kondisi patogenik sehingga secara langsung tidak menimbulkan "
            "risiko biologis pada buah yang dikonsumsi. Justru dampak kesehatan terbesar pada "
            "kondisi ini bersifat tidak langsung dan berasal dari kesalahan diagnosis: apabila "
            "gejala klorosis akibat kekurangan Nitrogen keliru dianggap sebagai infeksi jamur atau "
            "virus, petani berisiko menyemprotkan fungisida/insektisida yang sebenarnya tidak "
            "diperlukan. Aplikasi bahan kimia yang tidak tepat sasaran ini menambah beban paparan "
            "residu pada buah dan lingkungan tanpa manfaat agronomis, sekaligus meningkatkan risiko "
            "keracunan akut maupun kronis bagi petani aplikator secara sia-sia. Sebaliknya, "
            "pemupukan yang tepat dan terukur (mengikuti hasil uji tanah) justru mendukung kualitas "
            "gizi buah cabai, karena kandungan vitamin C dan kapsaisin pada buah turut dipengaruhi "
            "oleh kecukupan hara tanaman."
        )
    },

    "Healthy": {
        "label": "Healthy (Sehat)",
        "kategori": "Kondisi Normal",
        "severity": "tidak ada",
        "deskripsi": (
            "Tanaman cabai dalam kondisi baik: daun berwarna hijau cerah, permukaan halus "
            "tanpa noda atau perubahan tekstur, serta pertumbuhan yang wajar."
        ),
        "perlu_pestisida": False,
        "rekomendasi_residu": [
            "TIDAK diperlukan aplikasi pestisida maupun pupuk tambahan pada kondisi ini.",
            "Lanjutkan program pemupukan rutin/berimbang sesuai fase pertumbuhan tanaman.",
            "Pertahankan praktik budidaya standar (penyiraman, penyiangan gulma, sanitasi lahan)."
        ],
        "dampak_berlebihan": [
            "Jika tetap disemprot pestisida tanpa indikasi hama/penyakit: pemborosan biaya produksi yang tidak perlu.",
            "Residu kimia yang tidak perlu tetap tertinggal pada buah meski tanaman dalam kondisi sehat.",
            "Berpotensi meracuni musuh alami/predator dan penyerbuk (lebah) yang justru membantu produktivitas tanaman."
        ],
        "dampak_kekurangan": [
            "Tidak relevan — tanaman dalam kondisi sehat tidak memiliki gejala yang perlu dikoreksi.",
            "Tetap perlu pemantauan berkala agar kondisi sehat ini dapat dipertahankan hingga panen."
        ],
        "tindakan": [
            "Lanjutkan monitoring kondisi tanaman secara berkala (mingguan) menggunakan sistem ini.",
            "Jaga sanitasi lahan dan rotasi tanaman untuk mencegah munculnya penyakit/hama baru.",
            "Tidak perlu tindakan pengendalian kimia tambahan pada kondisi ini."
        ],
        "analisis_kesehatan_manusia": (
            "Tanaman dalam kondisi sehat tanpa tekanan hama, penyakit, maupun defisiensi hara "
            "umumnya menghasilkan buah dengan profil gizi optimal — termasuk kandungan vitamin C, "
            "karotenoid, dan kapsaisin yang menjadi sumber manfaat kesehatan cabai (antioksidan dan "
            "efek termogenik). Karena tidak ada indikasi hama/penyakit, tidak ada kebutuhan aplikasi "
            "pestisida sama sekali pada kondisi ini, sehingga risiko residu kimia pada buah berada "
            "pada titik terendah. Potensi risiko kesehatan hanya muncul apabila petani tetap "
            "melakukan penyemprotan preventif tanpa dasar diagnosis yang jelas ('safety spraying'), "
            "yang justru menambah paparan bahan kimia tanpa manfaat agronomis maupun kesehatan. "
            "Praktik budidaya bersih dan pemantauan rutin seperti yang difasilitasi sistem ini "
            "adalah cara paling efektif menjaga buah cabai tetap aman dan bergizi bagi konsumen."
        )
    }
}


# Alias nama kelas mentah (persis seperti pada model/class_indices.json,
# yang di-export otomatis dari folder training di Google Colab — biasanya huruf
# kecil semua) menuju key baku pada DISEASE_INFO di atas. Ditambahkan juga
# beberapa variasi ejaan/kapitalisasi agar pencocokan tetap berhasil walau
# format penamaan kelas sedikit berbeda antar hasil training.
_CLASS_ALIASES = {
    "powdery_mildew": "Powdery_Mildew",
    "cercospora": "Cercospora",
    "mites_and_trips": "Mites_and_Thrips",
    "mites_and_thrips": "Mites_and_Thrips",
    "nutritional": "Nutritional",
    "healthy": "Healthy",
}


def _normalize_class_name(class_name: str) -> str:
    return class_name.strip().lower().replace(" ", "_").replace("-", "_")


def get_disease_info(class_name: str) -> dict:
    """Mengambil informasi lengkap berdasarkan nama kelas hasil prediksi model.

    Pencocokan bersifat case-insensitive dan menangani beberapa alias ejaan,
    karena nama kelas pada class_indices.json (huruf kecil, hasil export
    Colab) tidak selalu identik dengan key pada DISEASE_INFO di atas.
    """
    normalized = _normalize_class_name(class_name)
    key = _CLASS_ALIASES.get(normalized, class_name.strip().replace(" ", "_"))
    return DISEASE_INFO.get(key, {
        "label": class_name,
        "kategori": "Tidak diketahui",
        "severity": "-",
        "deskripsi": "Informasi untuk kelas ini belum tersedia dalam basis pengetahuan.",
        "perlu_pestisida": False,
        "rekomendasi_residu": [],
        "dampak_berlebihan": [],
        "dampak_kekurangan": [],
        "tindakan": [],
        "analisis_kesehatan_manusia": ""
    })
