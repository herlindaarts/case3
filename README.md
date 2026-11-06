# Proyek Bedah Kasus 3 — Dataset Pengamatan Cuaca

Aplikasi Analisis Data Meteorologi, Eksplorasi Statistik Atmosfer, dan Dashboard Interaktif Pengamatan Cuaca berbasis Python, Pandas, NumPy, Matplotlib, Seaborn, dan Streamlit.

---

## 👤 Identitas Mahasiswa

| Atribut | Informasi Mahasiswa |
| :--- | :--- |
| **Nama Mahasiswa** | **Herlinda Artika Sari** |
| **Nomor Induk Mahasiswa (NIM)** | **241041011** |
| **Mata Kuliah** | Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca |
| **Program Studi** | Analisis Data & Sains Data Terapan |
| **Tahun Akademik** | 2024 / 2025 |

---

## 📁 Struktur Direktori Proyek

```text
case3/
├── app.py                      # Aplikasi dashboard interaktif Streamlit & Plotly
├── analisis.py                 # Skrip analisis meteorologi komprehensif (Matplotlib/Seaborn)
├── generate_data.py            # Skrip generator dataset sintetis cuaca (1.000 baris tepat, reproducible)
├── requirements.txt            # Daftar pustaka dependensi Python
├── README.md                   # Dokumentasi lengkap proyek dan panduan operasional
├── data/
│   └── data_sintesis_1000.csv  # Dataset observasi cuaca sintetis (tepat 1.000 baris data)
├── output/
│   ├── ringkasan_analisis.csv  # Ringkasan metrik iklim mikro per kota pengamatan
│   ├── 01_distribusi_suhu.png  # Histogram & KDE sebaran suhu udara (°C)
│   ├── 02_distribusi_kelembapan.png # Histogram & KDE sebaran kelembapan relatif (%)
│   ├── 03_perbandingan_kota.png # Diagram batang komparasi suhu dan kelembapan antarkota
│   ├── 04_distribusi_kondisi.png # Diagram batang distribusi frekuensi kondisi cuaca
│   ├── 05_boxplot_suhu_kelembapan.png # Box plot suhu dan kelembapan per kota & deteksi outlier
│   ├── 06_scatter_suhu_kelembapan.png # Scatter plot hubungan suhu vs kelembapan & garis regresi
│   └── 07_tren_waktu_cuaca.png # Grafik garis tren suhu & kelembapan bulanan sepanjang 2024
└── laporan/
    └── laporan_analisis.md     # Laporan akademik lengkap analisis pengamatan cuaca
```

---

## ⚙️ Persyaratan Sistem & Instalasi

### 1. Prasyarat Lingkungan
- Python versi 3.9 atau lebih baru.
- Terminal / PowerShell dengan hak akses pembacaan berkas.

### 2. Langkah Instalasi Dependensi
Buka terminal pada direktori `case3/` dan jalankan perintah:

```bash
python -m pip install -r requirements.txt
```

Pustaka yang digunakan:
- `pandas` : Manipulasi data meteorologi tabular dan agregasi spasial-temporal.
- `numpy` : Komputasi statistik numerik dan distribusi probabilitas fisik.
- `matplotlib` & `seaborn` : Visualisasi statis beresolusi tinggi (300 DPI).
- `streamlit` : Framework dashboard web interaktif dan responsif.
- `plotly` : Visualisasi data dinamis dengan tooltip interaktif.

---

## 🚀 Panduan Menjalankan Proyek (Workflow Eksekusi)

Ikuti 4 langkah berurutan di bawah ini untuk menguji dan mendemonstrasikan proyek kepada dosen pengampu:

### Langkah 1: Pembangkitan Dataset Sintetis Cuaca
Menghasilkan berkas `data/data_sintesis_1000.csv` berisi tepat 1.000 pengamatan cuaca dengan *random seed* 42:
```bash
python generate_data.py
```

### Langkah 2: Menjalankan Analisis Statistik Lengkap
Menjalankan audit kualitas data, perhitungan statistik deskriptif, korelasi suhu-kelembapan, serta menyimpan seluruh grafik ke folder `output/`:
```bash
python analisis.py
```

### Langkah 3: Menjalankan Dashboard Streamlit
Membuka aplikasi web interaktif di browser lokal:
```bash
python -m streamlit run app.py
```
*Aplikasi akan otomatis terbuka pada peramban web di alamat `http://localhost:8501`.*

---

## 📊 Ringkasan Hasil Analisis Aktual

Berdasarkan dataset 1.000 log observasi cuaca yang dihitung secara aktual oleh `analisis.py`:

1. **Suhu Udara Rata-rata**: **28,95 °C** (Median: **29,80 °C** | Standar Deviasi: **4,00 °C**).
2. **Kelembapan Relatif Rata-rata**: **77,33%** (Median: **77,00%** | Standar Deviasi: **11,88%**).
3. **Karakteristik Antarkota**:
   - Kota Terpanas: **Surabaya** (Rata-rata **33,1 °C**).
   - Kota Paling Sejuk: **Bandung** (Rata-rata **22,7 °C**).
   - Kota Paling Lembap: **Bogor** (Rata-rata **90,3%**).
   - Kota Paling Kering: **Surabaya** (Rata-rata **66,4%**).
4. **Kondisi Cuaca Dominan**:
   - **Cerah**: 304 pengamatan (**30,4%**).
   - **Berawan**: 297 pengamatan (**29,7%**).
   - **Mendung**: 185 pengamatan (**18,5%**).
   - **Hujan**: 139 pengamatan (**13,9%**).
   - **Hujan Lebat**: 75 pengamatan (**7,5%**).
5. **Korelasi Negatif Kuat**:
   - Pearson $r = -0,7997$ (Spearman $\rho = -0,8088$).
   - Hubungan ini merefleksikan termodinamika atmosfer Clausius-Clapeyron (kenaikan suhu meningkatkan kapasitas tampung uap air udara, sehingga kelembapan relatif turun).

---

## 🌡️ Penjelasan Ilmiah Skala Pengukuran Data

1. **Suhu Celsius (°C) — Skala Interval**:
   - Memiliki titik nol arbitrer (titik beku air), bukan nol mutlak (*absolute zero*).
   - Selisih angka bermakna ($30^\circ\text{C} - 20^\circ\text{C} = 10^\circ\text{C}$), tetapi perbandingan rasio proporsional tidak berlaku: **Suhu 20 °C bukan berarti dua kali lebih panas daripada 10 °C**.
2. **Kelembapan Relatif (%) — Skala Rasio Kapasitas**:
   - Merupakan rasio persentase tekanan uap air aktual terhadap kapasitas jenuh pada suhu tertentu, bukan massa absolut uap air.
3. **Kota dan Kondisi Cuaca — Skala Nominal**:
   - Data kategorik label tanpa peringkat matematis.
4. **Peringatan Kausalitas**:
   - Korelasi negatif tinggi antara suhu dan kelembapan tidak membuktikan kausalitas tunggal sepihak (*correlation does not imply causation*).

---

## 🌟 Fitur Dashboard Streamlit (`app.py`)

1. **Header Resmi & Identitas Mahasiswa**: Menampilkan Nama: **Herlinda Artika Sari**, NIM: **241041011**, dan keterangan 1.000 data cuaca sintetis.
2. **Sidebar Filter Multi-Dimensi**:
   - Filter Rentang Tanggal (Date Picker).
   - Filter Kota (Multi-select).
   - Filter Kondisi Cuaca (Multi-select).
   - Slider Rentang Suhu (°C).
   - Slider Rentang Kelembapan Relatif (%).
3. **Kartu KPI Dinamis**: Total Pengamatan, Suhu Rata-rata, Kelembapan Rata-rata, dan Jumlah Kota Teramati yang berubah otomatis mengikuti filter.
4. **Visualisasi Interaktif Plotly**:
   - Diagram batang & Donut chart distribusi kondisi cuaca.
   - Peringkat suhu dan kelembapan rata-rata antarkota.
   - Histogram distribusi suhu dan kelembapan dengan garis Mean & Median.
   - Box plot suhu dan kelembapan per kota untuk deteksi outlier.
   - Scatter plot hubungan suhu vs kelembapan dengan garis regresi OLS.
   - Grafik tren runtun waktu suhu dan kelembapan (pilihan bulanan, mingguan, harian).
5. **Data Explorer & Download**: Tabel data dengan pencarian teks cepat dan tombol **Unduh CSV** data aktif.
6. **Wawasan Otomatis (*Automated Insights*)**: Ringkasan temuan iklim yang otomatis disesuaikan dengan data aktif.
7. **Penanganan Filter Kosong (*Empty State*)**: Pesan panduan yang ramah tanpa menimbulkan galat/crash saat filter tidak menghasilkan data.

---

## 📤 Panduan Pengumpulan & Unggah ke Google Drive

1. **Pastikan Seluruh Berkas Lengkap di Folder `case3`**:
   - `app.py`
   - `analisis.py`
   - `generate_data.py`
   - `requirements.txt`
   - `README.md`
   - Folder `data/` (`data_sintesis_1000.csv`)
   - Folder `output/` (`ringkasan_analisis.csv` dan 7 grafik PNG)
   - Folder `laporan/` (`laporan_analisis.md`)
2. **Kompresi Folder**:
   - Klik kanan folder `case3` > pilih **Compress to ZIP file** (misal menjadi `case3_241041011_Herlinda_Artika_Sari.zip`).
3. **Unggah ke Google Drive**:
   - Buka Google Drive pada peramban web.
   - Masuk ke folder pengumpulan tugas mata kuliah Bedah Kasus 3 yang diarahkan dosen.
   - Seret (*drag and drop*) folder `case3` atau file `.zip` ke dalam folder Google Drive hingga proses unggah selesai 100%.

---

*Disusun dengan dedikasi dan integritas akademik oleh:*  
**Herlinda Artika Sari (NIM: 241041011)**  
*Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca*
