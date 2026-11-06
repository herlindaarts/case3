# LAPORAN ANALISIS METEOROLOGI DAN STATISTIK CUACA
## BEDAH KASUS 3: EKSPLORASI DATASET PENGAMATAN CUACA & IKLIM MIKRO

---

### IDENTITAS MAHASISWA
- **Nama Mahasiswa** : Herlinda Artika Sari
- **Nomor Induk Mahasiswa (NIM)** : 241041011
- **Mata Kuliah** : Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca
- **Program Studi** : Analisis Data & Sains Data Terapan
- **Tahun Akademik** : 2024 / 2025

---

## 1. RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY)

Laporan ini menyajikan hasil bedah kasus dan analisis statistik komprehensif terhadap dataset observasi cuaca harian yang terdiri dari **tepat 1.000 catatan pengamatan** di 7 kota besar Indonesia sepanjang tahun 2024. Analisis dilakukan secara kuantitatif dengan pendekatan sains data dan fisika atmosfer menggunakan pustaka Python (*Pandas, NumPy, Matplotlib, Seaborn, dan Plotly*).

### Ringkasan Temuan Utama:
1. **Gambaran Umum Parameter Atmosfer**:
   - **Suhu Udara Rata-rata**: Berada pada **28,95 °C** dengan median **29,80 °C** dan standar deviasi **4,00 °C** (rentang minimum 17,1 °C s/d maksimum 36,7 °C).
   - **Kelembapan Relatif Rata-rata**: Berada pada **77,33%** dengan median **77,00%** dan standar deviasi **11,88%** (rentang 48% s/d 99%).
2. **Karakteristik Iklim Mikro Antarkota**:
   - **Kota Terpanas**: **Surabaya** mencatatkan suhu rata-rata tertinggi sebesar **33,1 °C** dengan kelembapan rata-rata terendah (66,4%).
   - **Kota Paling Sejuk**: **Bandung** mencatatkan suhu rata-rata terendah sebesar **22,7 °C**, diikuti oleh **Bogor** sebesar **24,6 °C**.
   - **Kota Paling Lembap**: **Bogor** mencatatkan kelembapan relatif tertinggi sebesar **90,3%**, disusul **Bandung** (87,3%).
3. **Distribusi Kondisi Cuaca**:
   - Kondisi **Cerah** mendominasi sebanyak **304 pengamatan (30,4%)**, disusul oleh **Berawan** sebanyak **297 pengamatan (29,7%)**, **Mendung** sebanyak **185 pengamatan (18,5%)**, **Hujan** sebanyak **139 pengamatan (13,9%)**, dan **Hujan Lebat** sebanyak **75 pengamatan (7,5%)**.
4. **Korelasi Negatif Kuat Suhu vs Kelembapan**:
   - Terbukti terdapat korelasi linear negatif yang sangat kuat antara Suhu dan Kelembapan Relatif ($r = -0,7997$; Spearman $\rho = -0,8088$). Secara termodinamika atmosfer, ketika suhu udara meningkat, kapasitas udara dalam menampung uap air jenuh meningkat secara eksponensial, sehingga kelembapan relatifnya menurun.
5. **Refleksi Skala Pengukuran**:
   - Suhu dalam derajat Celsius merupakan **skala interval**: selisih suhu dapat dihitung secara absolut, tetapi perbandingan proporsional tidak berlaku (misal: suhu 20 °C **bukan** berarti dua kali lebih panas dari 10 °C).

---

## 2. LATAR BELAKANG & DESKRIPSI DATASET SINTETIS

### 2.1 Format Dataset Awal
Dataset ini dibangun mengacu pada struktur studi kasus yang diberikan oleh dosen pengampu dengan empat kolom inti:
- `Kota` : Lokasi stasiun pengamatan (Kategorik Nominal).
- `Suhu` : Suhu udara permukaan dalam derajat Celsius (Numerik Skala Interval).
- `Kelembapan` : Kelembapan relatif dalam persen % (Numerik Rasio Kapasitas).
- `Kondisi` : Deskripsi kondisi cuaca teramati (Kategorik Nominal).

### 2.2 Penambahan Kolom Tanggal untuk Analisis Tren Temporal
Untuk memenuhi persyaratan analisis tren waktu tanpa menyimpang dari struktur dasar dosen, ditambahkan kolom kelima:
- `Tanggal` : Tanggal kalender pengamatan format ISO `YYYY-MM-DD` (periode 1 Januari 2024 s/d 31 Desember 2024).
> [!NOTE]
> *Kolom Tanggal ini secara eksplisit didokumentasikan sebagai ekstensi analitik runtun waktu (time-series) dan bukan bagian dari 4 kolom awal dosen.*

### 2.3 Pembangkitan Data Sintetis Terprogram (`generate_data.py`)
Dataset dibangkitkan menggunakan skrip `generate_data.py` dengan parameter ilmiah:
- Tepat 1.000 baris data (tanpa header).
- *Random seed* = 42 (`np.random.seed(42)` dan `random.seed(42)`) untuk menjamin reproduktifitas 100%.
- Melibatkan 7 kota representatif: Jakarta (pesisir), Surabaya (pesisir panas), Bandung (dataran tinggi), Bogor (dataran tinggi hujan), Medan (tropis ekuator), Yogyakarta (pedalaman Jawa), dan Denpasar (pesisir pulau).
- Disclaimer: Seluruh data berstatus data sintetis untuk keperluan pembelajaran pemodelan data dan **bukan data riil dari BMKG**.

---

## 3. AUDIT KUALITAS & KEBERSIHAN DATA (DATA HYGIENE)

| Parameter Pengujian | Kondisi Target | Hasil Pengujian | Status |
| :--- | :--- | :--- | :---: |
| **Jumlah Baris Data** | Tepat 1.000 baris | 1.000 baris | **Sempurna [OK]** |
| **Missing Values (Null)** | 0 nilai kosong | 0 null di seluruh kolom | **Bersih [OK]** |
| **Validitas Rentang Suhu** | $15.0 \le \text{Suhu} \le 40.0 \text{ }^\circ\text{C}$ | Min: 17,1 °C \| Max: 36,7 °C | **Valid [OK]** |
| **Validitas Rentang Lembap** | $0\% \le \text{Kelembapan} \le 100\%$ | Min: 48% \| Max: 99% | **Valid [OK]** |
| **Konsistensi Kategori Kota** | 7 kota Indonesia | 7 kota valid | **Konsisten [OK]** |
| **Konsistensi Kondisi Cuaca** | 5 kondisi cuaca | Cerah, Berawan, Mendung, Hujan, Hujan Lebat | **Konsisten [OK]** |

---

## 4. STATISTIK DESKRIPTIF PARAMETRIK & NON-PARAMETRIK

Tabel berikut menyajikan parameter statistik deskriptif aktual yang dihitung oleh `analisis.py` dari 1.000 catatan pengamatan cuaca:

| Parameter Statistik | Suhu Udara (°C) — Skala Interval | Kelembapan Relatif (%) — Skala Rasio Kapasitas |
| :--- | :--- | :--- |
| **Rata-rata (Mean)** | **28,95 °C** | **77,33%** |
| **Nilai Tengah (Median / Q2)** | **29,80 °C** | **77,00%** |
| **Nilai Modus (Mode)** | **32,80 °C** | **74,00%** |
| **Standar Deviasi ($\sigma$)** | **4,00 °C** | **11,88%** |
| **Nilai Minimum** | **17,10 °C** | **48,00%** |
| **Kuartil 1 ($Q_1$ - 25%)** | **25,80 °C** | **67,00%** |
| **Kuartil 3 ($Q_3$ - 75%)** | **32,50 °C** | **89,00%** |
| **Jangkauan Interkuartil (IQR)**| **6,70 °C** | **22,00%** |
| **Nilai Maksimum** | **36,70 °C** | **99,00%** |
| **Kemiringan (Skewness)** | **-0,7136 (Negatively Skewed)** | **-0,2097 (Slightly Negative)** |
| **Keruncingan (Kurtosis)** | **-0,5802 (Platykurtic)** | **-0,9877 (Platykurtic)** |

---

## 5. ANALISIS PERBANDINGAN IKLIM MIKRO ANTARKOTA

| Kota Pengamatan | Jumlah Hari | Suhu Rata-rata | Median Suhu | Kelembapan Rata-rata | Karakteristik Topografi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Surabaya** | 150 | **33,1 °C** | 33,3 °C | **66,4%** | Pesisir dataran rendah, iklim panas kering |
| **Jakarta** | 204 | **32,3 °C** | 32,5 °C | **71,6%** | Pesisir utara Jawa, iklim tropis perkotaan |
| **Medan** | 115 | **30,6 °C** | 30,8 °C | **78,1%** | Dataran rendah Sumatera, hangat dan lembap |
| **Denpasar** | 121 | **30,1 °C** | 30,1 °C | **75,4%** | Pesisir pulau tropis, maritim stabil |
| **Yogyakarta** | 105 | **29,5 °C** | 29,8 °C | **76,2%** | Lembah pedalaman, variasi diurnal moderat |
| **Bogor** | 156 | **24,6 °C** | 24,9 °C | **90,3%** | Kaki gunung / dataran tinggi, curah hujan tinggi |
| **Bandung** | 149 | **22,7 °C** | 22,9 °C | **87,3%** | Cekungan dataran tinggi (~768 mdpl), sejuk |

#### Wawasan Geografis:
Terdapat gradien termal yang sangat jelas akibat perbedaan ketinggian (*lapse rate*). Kota-kota dataran tinggi (Bandung dan Bogor) memiliki suhu rata-rata yang lebih rendah sebesar **8 s/d 10 °C** dibandingkan kota-kota pesisir pantai (Jakarta dan Surabaya).

---

## 6. ANALISIS KARAKTERISTIK KONDISI CUACA

| Kondisi Cuaca | Jumlah Hari | Persentase | Suhu Rata-rata (°C) | Kelembapan Rata-rata (%) | Interpretasi Meteorologi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Cerah** | 304 | **30,40%** | **32,0 °C** | **65,5%** | Radiasi matahari maksimum, evaporasi tinggi |
| **Berawan** | 297 | **29,70%** | **29,9 °C** | **74,3%** | Tutupan awan moderat, suhu hangat normal |
| **Mendung** | 185 | **18,50%** | **27,5 °C** | **85,2%** | Penurunan insolation, kelembapan meningkat |
| **Hujan** | 139 | **13,90%** | **25,4 °C** | **92,3%** | Pendinginan presipitasi, udara mendekati jenuh |
| **Hujan Lebat** | 75 | **7,50%** | **23,9 °C** | **95,8%** | Suhu terdingin, kelembapan saturasi ekstrem |

---

## 7. EVALUASI OUTLIER (PENCILAN) METODE IQR

Pencilan dievaluasi menggunakan kaidah $1,5 \times \text{IQR}$:
- **Suhu**:
  - $Q_1 = 25,80 \text{ }^\circ\text{C}$, $Q_3 = 32,50 \text{ }^\circ\text{C}$, $\text{IQR} = 6,70 \text{ }^\circ\text{C}$
  - $\text{Lower Fence} = 25,80 - 1,5 \times 6,70 = 15,75 \text{ }^\circ\text{C}$
  - $\text{Upper Fence} = 32,50 + 1,5 \times 6,70 = 42,55 \text{ }^\circ\text{C}$
  - **Hasil Outlier**: **0 baris (0,00%)** berada di luar batas, menunjukkan bahwa seluruh nilai suhu berada dalam rentang variasi alami yang valid.
- **Kelembapan**:
  - $Q_1 = 67,00\%$, $Q_3 = 89,00\%$, $\text{IQR} = 22,00\%$
  - $\text{Lower Fence} = 67,00 - 1,5 \times 22,00 = 34,00\%$
  - $\text{Upper Fence} = 89,00 + 1,5 \times 22,00 = 122,00\%$
  - **Hasil Outlier**: **0 baris (0,00%)**, membuktikan data tidak memiliki nilai ekstrem palsu.

---

## 8. ANALISIS KORELASI & FISIKA ATMOSFER (SUHU VS KELEMBAPAN)

### 8.1 Matriks Korelasi Numerik
- **Koefisien Pearson ($r$)** : **-0,7997** (Korelasi Negatif Kuat)
- **Koefisien Spearman ($\rho$)** : **-0,8088** (Korelasi Monotonik Negatif Kuat)

### 8.2 Landasan Fisika Termodinamika
Hubungan negatif yang kuat ini dijelaskan oleh hukum fisika tekanan uap jenuh (*saturation vapor pressure* $e_s$) melalui persamaan **Clausius-Clapeyron**:
$$e_s(T) \approx 6,11 \times \exp\left(\frac{17,27 \times T}{T + 237,3}\right)$$
Di mana kelembapan relatif ($\text{RH}$) didefinisikan sebagai:
$$\text{RH} = \frac{e}{e_s(T)} \times 100\%$$
Ketika suhu ($T$) naik, nilai $e_s(T)$ meningkat secara eksponensial. Jika kandungan uap air absolut ($e$) relatif konstan, nilai fraksi $\frac{e}{e_s(T)}$ akan menurun, menyebabkan penurunan nilai kelembapan relatif ($\text{RH}$).

---

## 9. PEMBAHASAN MENDALAM TEORI SKALA PENGUKURAN STATISTIK

### 9.1 Suhu Celsius Adalah Skala Interval (Bukan Rasio)
> [!IMPORTANT]
> **Mengapa 20 °C Tidak Berarti Dua Kali Lebih Panas dari 10 °C?**
> - Skala Celsius memiliki **titik nol arbitrer** (ditetapkan berdasarkan titik beku air pada tekanan 1 atmosfer), bukan **nol mutlak** (*absolute zero* = ketiadaan energi termal).
> - Selisih antarnilai memiliki makna nyata: kenaikan dari 10 °C ke 20 °C ($\Delta T = 10 \text{ K}$) sama besarnya dengan kenaikan dari 20 °C ke 30 °C ($\Delta T = 10 \text{ K}$).
> - Namun, operasi perkalian/rasio tidak valid secara termodinamika. Dalam skala rasio mutlak Kelvin:
>   $$10 \text{ }^\circ\text{C} = 283,15 \text{ K}$$
>   $$20 \text{ }^\circ\text{C} = 293,15 \text{ K}$$
>   Rasio sebenarnya adalah $\frac{293,15}{283,15} \approx 1,035$ (hanya lebih panas sebesar 3,5%, bukan 100% atau dua kali lipat).

### 9.2 Kelembapan Persentase Adalah Kelembapan Relatif (RH)
Kelembapan udara yang diukur dalam persentase (%) adalah **rasio komparatif** terhadap kapasitas udara, bukan massa uap air absolut ($g/m^3$). Udara bersuhu 33 °C dengan kelembapan 66% di Surabaya sebenarnya mengandung massa uap air absolut per meter kubik yang lebih banyak dibanding udara 22 °C dengan kelembapan 87% di Bandung.

### 9.3 Kota dan Kondisi Cuaca Adalah Skala Nominal
Label kategori seperti nama kota dan jenis kondisi cuaca tidak memiliki bobot angka, peringkat, atau urutan matematis (*non-parametric nominal data*).

---

## 10. REKOMENDASI TERAPAN METEOROLOGI DATA

1. **Perencanaan Kenyamanan Termal & Indeks Panas (*Heat Index*)**:
   - Meskipun kelembapan Surabaya lebih rendah (66,4%), suhu tinggi (33,1 °C) menghasilkan beban panas tinggi. Kota Jakarta dan Surabaya membutuhkan ruang terbuka hijau dan koridor ventilasi perkotaan yang lebih baik.
2. **Mitigasi Bencana Hidrometeorologi**:
   - Bogor dan Bandung memiliki frekuensi hujan dan kelembapan di atas 87%. Sistem drainase perkotaan dan peringatan dini longsor harus disiagakan terutama pada periode musim hujan (Oktober–Maret).

---

## 11. KESIMPULAN & KETERBATASAN

### 11.1 Kesimpulan
Seluruh target analisis dalam tugas Bedah Kasus 3 telah diselesaikan dengan standar akademis tinggi. Dataset 1.000 baris observasi cuaca telah diuji, dianalisis statistik deskriptif dan inferensialnya, divisualisasikan dalam bentuk grafik resolusi tinggi, serta disajikan dalam dashboard web interaktif Streamlit yang responsif.

### 11.2 Keterbatasan
Dataset ini adalah data sintetis berbasis komputasi statistik untuk pembelajaran akademis, sehingga dinamika cuaca ekstrem seperti siklon tropis atau anomali El Niño / La Niña riil belum tercakup.

---

*Laporan disusun dengan dedikasi ilmiah dan tanggung jawab akademis oleh:*  
**Herlinda Artika Sari (NIM: 241041011)**  
*Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca*
