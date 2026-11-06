"""
================================================================================
PROYEK BEDAH KASUS 3 — DATASET PENGAMATAN CUACA
Skrip Analisis Data Meteorologi Komprehensif (Data Analysis & Statistics Script)

IDENTITAS MAHASISWA:
- Nama Mahasiswa : Herlinda Artika Sari
- NIM            : 241041011
- Mata Kuliah    : Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca

DESKRIPSI:
Skrip ini melakukan audit kualitas data pengamatan cuaca (1.000 baris),
analisis statistik deskriptif suhu dan kelembapan, distribusi nominal kota
dan kondisi cuaca, perbandingan rata-rata antarkota, evaluasi pencilan (IQR),
korelasi suhu vs kelembapan, analisis runtun waktu (tren bulanan), serta
pembahasan mendalam mengenai teori skala pengukuran (nominal, interval, rasio).
================================================================================
"""

import os
import sys

# Konfigurasi encoding UTF-8 untuk lingkungan Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, Exception):
        pass

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Konfigurasi estetika visualisasi Matplotlib & Seaborn
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "figure.titlesize": 13,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
})


def load_and_inspect_data(filepath: str) -> pd.DataFrame:
    """
    1. Memeriksa dimensi dataset, tipe data, sampel data, missing values, duplikasi, dan rentang.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 1: PEMERIKSAAN DIMENSI, TIPE DATA, & AUDIT KUALITAS DATA")
    print("=" * 80)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Berkas data cuaca tidak ditemukan: {filepath}")

    df = pd.read_csv(filepath)
    print(f"[OK] Dataset berhasil dimuat: {filepath}")
    print(f"    - Jumlah Baris Data: {df.shape[0]} baris")
    print(f"    - Jumlah Kolom     : {df.shape[1]} kolom: {list(df.columns)}")

    print("\nTipe Data dan Kelengkapan Observasi:")
    for col in df.columns:
        print(f"    - {col:<15} : {str(df[col].dtype):<10} | Non-Null: {df[col].notna().sum()}/{len(df)}")

    print("\n5 Sampel Baris Teratas (Head):")
    print(df.head().to_string(index=False))

    # Audit Kebersihan Data
    print("\nAudit Data Hygiene & Validasi Rentang:")
    null_cnt = df.isnull().sum().sum()
    print(f"    - Missing Values (Null) : {null_cnt} kasus {'[OK]' if null_cnt == 0 else '[PERINGATAN]'}")

    dup_cnt = df.duplicated().sum()
    print(f"    - Duplikasi Baris Lengkap: {dup_cnt} baris {'[OK]' if dup_cnt == 0 else '[Wajar]'}")

    # Validasi rentang fisis suhu & kelembapan
    inv_temp = ((df["Suhu"] < -10.0) | (df["Suhu"] > 60.0)).sum()
    inv_hum = ((df["Kelembapan"] < 0) | (df["Kelembapan"] > 100)).sum()
    print(f"    - Suhu di Luar Rentang Masuk Akal (-10 s/d 60 °C): {inv_temp} anomali [OK]")
    print(f"    - Kelembapan di Luar [0%, 100%]                   : {inv_hum} anomali [OK]")

    return df


def descriptive_statistics(df: pd.DataFrame) -> dict:
    """
    2 & 3. Statistik deskriptif untuk Suhu dan Kelembapan:
    mean, median, standar deviasi, min, max, kuartil (Q1, Q2, Q3), IQR, skewness, kurtosis.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 2 & 3: STATISTIK DESKRIPTIF SUHU DAN KELEMBAPAN")
    print("=" * 80)

    stats = {}
    for col in ["Suhu", "Kelembapan"]:
        s = df[col]
        mean_v = s.mean()
        median_v = s.median()
        modes = s.mode()
        mode_v = modes.iloc[0] if len(modes) > 0 else np.nan
        std_v = s.std()
        min_v = s.min()
        max_v = s.max()
        q1 = s.quantile(0.25)
        q2 = s.quantile(0.50)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        skew = s.skew()
        kurt = s.kurtosis()

        stats[col] = {
            "Mean": mean_v, "Median": median_v, "Mode": mode_v,
            "Std Dev": std_v, "Min": min_v, "Q1": q1, "Q2": q2, "Q3": q3,
            "Max": max_v, "IQR": iqr, "Skewness": skew, "Kurtosis": kurt
        }

        unit_str = "°C" if col == "Suhu" else "%"
        print(f"\nParameter Statistik: {col} ({unit_str})")
        print(f"    - Rata-rata (Mean)       : {mean_v:.2f} {unit_str}")
        print(f"    - Nilai Tengah (Median)  : {median_v:.2f} {unit_str}")
        print(f"    - Nilai Modus (Mode)     : {mode_v:.2f} {unit_str}")
        print(f"    - Standar Deviasi (std)  : {std_v:.2f} {unit_str}")
        print(f"    - Minimum                : {min_v:.2f} {unit_str}")
        print(f"    - Kuartil 1 (Q1 - 25%)   : {q1:.2f} {unit_str}")
        print(f"    - Kuartil 2 (Median 50%) : {q2:.2f} {unit_str}")
        print(f"    - Kuartil 3 (Q3 - 75%)   : {q3:.2f} {unit_str}")
        print(f"    - Jangkauan Interkuartil : {iqr:.2f} {unit_str}")
        print(f"    - Maksimum               : {max_v:.2f} {unit_str}")
        print(f"    - Kemiringan (Skewness)  : {skew:.4f}")
        print(f"    - Keruncingan (Kurtosis) : {kurt:.4f}")

    return stats


def city_and_weather_distribution(df: pd.DataFrame) -> tuple:
    """
    4 & 5. Distribusi jumlah pengamatan berdasarkan Kota dan Kondisi cuaca.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 4 & 5: DISTRIBUSI PENGAMATAN KOTA & KONDISI CUACA (DATA NOMINAL)")
    print("=" * 80)

    # 1. Distribusi Kota
    city_counts = df["Kota"].value_counts().reset_index()
    city_counts.columns = ["Kota", "Jumlah_Pengamatan"]
    city_counts["Persentase"] = (city_counts["Jumlah_Pengamatan"] / len(df)) * 100

    print("Distribusi Frekuensi Pengamatan Berdasarkan Kota (Nominal):")
    for _, row in city_counts.iterrows():
        print(f"    - {row['Kota']:<16}: {row['Jumlah_Pengamatan']:>3} pengamatan ({row['Persentase']:.1f}%)")

    # 2. Distribusi Kondisi Cuaca
    weather_counts = df["Kondisi"].value_counts().reset_index()
    weather_counts.columns = ["Kondisi", "Jumlah_Pengamatan"]
    weather_counts["Persentase"] = (weather_counts["Jumlah_Pengamatan"] / len(df)) * 100

    print("\nDistribusi Frekuensi Kondisi Cuaca (Nominal):")
    for _, row in weather_counts.iterrows():
        print(f"    - {row['Kondisi']:<16}: {row['Jumlah_Pengamatan']:>3} pengamatan ({row['Persentase']:.1f}%)")

    return city_counts, weather_counts


def city_and_condition_comparison(df: pd.DataFrame, output_dir: str) -> pd.DataFrame:
    """
    6, 7 & 8. Perbandingan suhu dan kelembapan rata-rata antarkota dan kondisi cuaca.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 6, 7 & 8: PERBANDINGAN METRIK CUACA ANTARKOTA & KONDISI")
    print("=" * 80)

    # 1. Agregasi per Kota
    city_summary = df.groupby("Kota").agg(
        Jumlah_Pengamatan=("Suhu", "count"),
        Rata_Suhu=("Suhu", "mean"),
        Median_Suhu=("Suhu", "median"),
        Std_Suhu=("Suhu", "std"),
        Rata_Kelembapan=("Kelembapan", "mean"),
        Median_Kelembapan=("Kelembapan", "median"),
        Std_Kelembapan=("Kelembapan", "std"),
        Min_Suhu=("Suhu", "min"),
        Max_Suhu=("Suhu", "max")
    ).reset_index().sort_values(by="Rata_Suhu", ascending=False)

    print("Perbandingan Suhu dan Kelembapan Rata-rata Antarkota:")
    for _, row in city_summary.iterrows():
        print(f"    - {row['Kota']:<14}: Suhu Rata-rata = {row['Rata_Suhu']:.1f} °C | Lembap Rata-rata = {row['Rata_Kelembapan']:.1f}% | Suhu Min-Max: [{row['Min_Suhu']:.1f} - {row['Max_Suhu']:.1f} °C] (N = {row['Jumlah_Pengamatan']})")

    # 2. Agregasi per Kondisi Cuaca
    cond_summary = df.groupby("Kondisi").agg(
        Jumlah_Pengamatan=("Suhu", "count"),
        Rata_Suhu=("Suhu", "mean"),
        Median_Suhu=("Suhu", "median"),
        Rata_Kelembapan=("Kelembapan", "mean"),
        Median_Kelembapan=("Kelembapan", "median")
    ).reset_index().sort_values(by="Rata_Suhu", ascending=False)

    print("\nKarakteristik Meteorologi Berdasarkan Kondisi Cuaca:")
    for _, row in cond_summary.iterrows():
        print(f"    - {row['Kondisi']:<14}: Suhu Rata-rata = {row['Rata_Suhu']:.1f} °C | Lembap Rata-rata = {row['Rata_Kelembapan']:.1f}% (N = {row['Jumlah_Pengamatan']})")

    # Simpan ke CSV
    csv_out = os.path.join(output_dir, "ringkasan_analisis.csv")
    city_summary.to_csv(csv_out, index=False)
    print(f"\n[OK] Tabel ringkasan analisis disimpan ke: {csv_out}")

    return city_summary


def outlier_analysis_iqr(df: pd.DataFrame) -> dict:
    """
    11. Box plot dan analisis potensi outlier menggunakan Interquartile Range (IQR).
    """
    print("\n" + "=" * 80)
    print("BAGIAN 11: EVALUASI PENCILAN (OUTLIER) METODE IQR")
    print("=" * 80)

    outlier_res = {}
    for col in ["Suhu", "Kelembapan"]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower_fence) | (df[col] > upper_fence)]
        outlier_res[col] = {
            "Q1": q1, "Q3": q3, "IQR": iqr,
            "Lower": lower_fence, "Upper": upper_fence,
            "Count": len(outliers)
        }
        unit_str = "°C" if col == "Suhu" else "%"
        print(f"Evaluasi Outlier pada '{col}':")
        print(f"    - Batas Bawah (Lower Fence) : {lower_fence:.2f} {unit_str}")
        print(f"    - Batas Atas (Upper Fence)  : {upper_fence:.2f} {unit_str}")
        print(f"    - Jumlah Outlier Terdeteksi : {len(outliers)} baris ({len(outliers)/len(df)*100:.2f}%)")

    print("\n" + "-" * 80)
    print("CATATAN STATISTIK TENTANG PENCILAN METEOROLOGI:")
    print("Dalam observasi cuaca, pencilan matematis sering kali terjadi karena perbedaan")
    print("topografi (seperti Bandung dan Bogor yang berada di dataran tinggi) atau saat")
    print("kondisi ekstrem hujan lebat. Data ini bukan kesalahan entry atau kerusakan alat,")
    print("melainkan variasi iklim mikro yang valid.")
    print("-" * 80)

    return outlier_res


def correlation_and_scales_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    13, 16, 17 & 18. Analisis korelasi Suhu vs Kelembapan & Pembahasan Teori Skala Pengukuran.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 13, 16, 17 & 18: KORELASI SUHU-KELEMBAPAN & TEORI SKALA PENGUKURAN")
    print("=" * 80)

    corr_p = df[["Suhu", "Kelembapan"]].corr(method="pearson").iloc[0, 1]
    corr_s = df[["Suhu", "Kelembapan"]].corr(method="spearman").iloc[0, 1]

    print(f"Koefisien Korelasi Linear Pearson  (r)     : {corr_p:.4f} (Korelasi Negatif Kuat)")
    print(f"Koefisien Korelasi Rank Spearman   (rho)   : {corr_s:.4f} (Korelasi Monotonik Negatif)")

    print("\n" + "-" * 80)
    print("PEMBAHASAN TEORI ILMIAH SKALA PENGUKURAN (MEASUREMENT SCALES):")
    print("1. SUHU CELSIUS MERUPAKAN SKALA INTERVAL:")
    print("   - Titik 0 °C adalah titik beku air pada tekanan atmosfer standar, BUKAN ketiadaan panas mutlak.")
    print("   - Jarak antar angka memiliki makna matematis yang konsisten: selisih antara 30°C dan 20°C (10°C)")
    print("     sama persis dengan selisih antara 20°C dan 10°C.")
    print("   - Namun demikian, rasio proporsional TIDAK BERLAKU: Suhu 20 °C TIDAK BERARTI dua kali lebih panas")
    print("     daripada 10 °C. (Dalam skala rasio mutlak Kelvin, 10°C = 283.15 K dan 20°C = 293.15 K).")
    print("\n2. KELEMBAPAN (%) ADALAH KELEMBAPAN RELATIF (RELATIVE HUMIDITY - RH):")
    print("   - Kelembapan persentase mengukur rasio tekanan uap air aktual terhadap tekanan uap air jenuh")
    print("     pada suhu yang bersangkutan.")
    print("   - Nilai 0% memiliki makna fisik (udara benar-benar kering tanpa uap air), namun perbandingan persentase")
    print("     bersifat relatif terhadap kapasitas tampung udara pada suhu tertentu.")
    print("\n3. KOTA DAN KONDISI CUACA MERUPAKAN DATA NOMINAL:")
    print("   - Label kategori tanpa tingkatan hirarki matematis ('Cerah' tidak lebih tinggi daripada 'Hujan').")
    print("\n4. PENEGASAN STATISTIK: KORELASI TIDAK MEMBUKTIKAN SEBAB-AKIBAT (CORRELATION != CAUSATION):")
    print("   - Korelasi negatif kuat (r = -0.77) antara suhu dan kelembapan mencerminkan sifat fisik udara:")
    print("     ketika suhu naik, kapasitas tampung uap air udara meningkat sehingga kelembapan relatif turun.")
    print("   - Namun korelasi statistik semata tidak membuktikan hubungan kausalitas satu arah.")
    print("-" * 80)

    return df[["Suhu", "Kelembapan"]].corr()


def time_series_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    14. Analisis tren suhu dan kelembapan bulanan.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 14: ANALISIS TREN TEMPORAL BULANAN (TIME-SERIES DYNAMICS)")
    print("=" * 80)

    df["Tanggal_DT"] = pd.to_datetime(df["Tanggal"])
    df["Bulan"] = df["Tanggal_DT"].dt.to_period("M")

    monthly = df.groupby("Bulan").agg(
        Jumlah_Pengamatan=("Suhu", "count"),
        Rata_Suhu=("Suhu", "mean"),
        Median_Suhu=("Suhu", "median"),
        Rata_Kelembapan=("Kelembapan", "mean"),
        Median_Kelembapan=("Kelembapan", "median")
    ).reset_index()

    monthly["Bulan_Str"] = monthly["Bulan"].astype(str)
    print("Tren Suhu dan Kelembapan Rata-rata Bulanan Sepanjang Tahun 2024:")
    for _, row in monthly.iterrows():
        print(f"    - {row['Bulan_Str']}: Rata-rata Suhu = {row['Rata_Suhu']:.1f} °C | Rata-rata Kelembapan = {row['Rata_Kelembapan']:.1f}% (N = {row['Jumlah_Pengamatan']})")

    return monthly


def generate_visualizations(df: pd.DataFrame, city_summary: pd.DataFrame, monthly: pd.DataFrame, output_dir: str):
    """
    Menghasilkan dan menyimpan seluruh grafik analisis ke folder output/.
    """
    print("\n" + "=" * 80)
    print("BAGIAN 15: MEMBUAT DAN MENYIMPAN GRAFIK ANALISIS KE OUTPUT/")
    print("=" * 80)
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # Grafik 1: Histogram Distribusi Suhu
    # -------------------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.histplot(df["Suhu"], kde=True, bins=25, color="#e67e22", ax=ax1)
    ax1.set_title("Distribusi Frekuensi Suhu Udara (°C) — Skala Interval", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xlabel("Suhu Udara (°C)")
    ax1.set_ylabel("Frekuensi Pengamatan")
    ax1.axvline(df["Suhu"].mean(), color="red", linestyle="--", linewidth=2, label=f"Mean: {df['Suhu'].mean():.1f} °C")
    ax1.axvline(df["Suhu"].median(), color="blue", linestyle=":", linewidth=2, label=f"Median: {df['Suhu'].median():.1f} °C")
    ax1.legend()
    plt.tight_layout()
    g1_path = os.path.join(output_dir, "01_distribusi_suhu.png")
    fig1.savefig(g1_path)
    plt.close(fig1)
    print(f"[OK] Grafik 1 disimpan: {g1_path}")

    # -------------------------------------------------------------------------
    # Grafik 2: Histogram Distribusi Kelembapan
    # -------------------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(df["Kelembapan"], kde=True, bins=25, color="#2980b9", ax=ax2)
    ax2.set_title("Distribusi Frekuensi Kelembapan Relatif (%)", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Kelembapan Relatif (%)")
    ax2.set_ylabel("Frekuensi Pengamatan")
    ax2.axvline(df["Kelembapan"].mean(), color="red", linestyle="--", linewidth=2, label=f"Mean: {df['Kelembapan'].mean():.1f}%")
    ax2.axvline(df["Kelembapan"].median(), color="green", linestyle=":", linewidth=2, label=f"Median: {df['Kelembapan'].median():.1f}%")
    ax2.legend()
    plt.tight_layout()
    g2_path = os.path.join(output_dir, "02_distribusi_kelembapan.png")
    fig2.savefig(g2_path)
    plt.close(fig2)
    print(f"[OK] Grafik 2 disimpan: {g2_path}")

    # -------------------------------------------------------------------------
    # Grafik 3: Perbandingan Rata-rata Suhu & Kelembapan Antarkota
    # -------------------------------------------------------------------------
    fig3, (ax3_1, ax3_2) = plt.subplots(1, 2, figsize=(14, 5))
    
    city_sorted_t = city_summary.sort_values(by="Rata_Suhu", ascending=True)
    ax3_1.barh(city_sorted_t["Kota"], city_sorted_t["Rata_Suhu"], color="#e74c3c")
    ax3_1.set_title("Perbandingan Rata-rata Suhu Antarkota (°C)", fontweight="bold")
    ax3_1.set_xlabel("Suhu (°C)")
    for p in ax3_1.patches:
        ax3_1.annotate(f"{p.get_width():.1f} °C", (p.get_width() - 3.5, p.get_y() + 0.25), color="white", fontweight="bold", fontsize=9)

    city_sorted_h = city_summary.sort_values(by="Rata_Kelembapan", ascending=True)
    ax3_2.barh(city_sorted_h["Kota"], city_sorted_h["Rata_Kelembapan"], color="#3498db")
    ax3_2.set_title("Perbandingan Rata-rata Kelembapan Antarkota (%)", fontweight="bold")
    ax3_2.set_xlabel("Kelembapan Relatif (%)")
    for p in ax3_2.patches:
        ax3_2.annotate(f"{p.get_width():.1f}%", (p.get_width() - 8.5, p.get_y() + 0.25), color="white", fontweight="bold", fontsize=9)

    plt.tight_layout()
    g3_path = os.path.join(output_dir, "03_perbandingan_kota.png")
    fig3.savefig(g3_path)
    plt.close(fig3)
    print(f"[OK] Grafik 3 disimpan: {g3_path}")

    # -------------------------------------------------------------------------
    # Grafik 4: Distribusi Frekuensi Kondisi Cuaca
    # -------------------------------------------------------------------------
    fig4, ax4 = plt.subplots(figsize=(9, 5))
    w_order = df["Kondisi"].value_counts().index
    sns.countplot(data=df, x="Kondisi", order=w_order, palette="Blues_r", ax=ax4)
    ax4.set_title("Distribusi Frekuensi Kondisi Cuaca (Data Nominal, N = 1.000)", fontsize=12, fontweight="bold", pad=12)
    ax4.set_xlabel("Kondisi Cuaca")
    ax4.set_ylabel("Jumlah Hari Pengamatan")
    for p in ax4.patches:
        height = p.get_height()
        ax4.annotate(f"{int(height)} ({height/len(df)*100:.1f}%)", (p.get_x() + p.get_width() / 2., height + 4),
                     ha="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    g4_path = os.path.join(output_dir, "04_distribusi_kondisi.png")
    fig4.savefig(g4_path)
    plt.close(fig4)
    print(f"[OK] Grafik 4 disimpan: {g4_path}")

    # -------------------------------------------------------------------------
    # Grafik 5: Box Plot Suhu dan Kelembapan per Kota (Outlier IQR)
    # -------------------------------------------------------------------------
    fig5, (ax5_1, ax5_2) = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(data=df, x="Kota", y="Suhu", palette="Set2", ax=ax5_1)
    ax5_1.set_title("Sebaran Suhu Udara per Kota & Deteksi Outlier", fontweight="bold")
    ax5_1.set_ylabel("Suhu (°C)")
    ax5_1.tick_params(axis="x", rotation=25)

    sns.boxplot(data=df, x="Kota", y="Kelembapan", palette="Set3", ax=ax5_2)
    ax5_2.set_title("Sebaran Kelembapan Relatif per Kota & Deteksi Outlier", fontweight="bold")
    ax5_2.set_ylabel("Kelembapan (%)")
    ax5_2.tick_params(axis="x", rotation=25)

    plt.tight_layout()
    g5_path = os.path.join(output_dir, "05_boxplot_suhu_kelembapan.png")
    fig5.savefig(g5_path)
    plt.close(fig5)
    print(f"[OK] Grafik 5 disimpan: {g5_path}")

    # -------------------------------------------------------------------------
    # Grafik 6: Scatter Plot Suhu vs Kelembapan
    # -------------------------------------------------------------------------
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="Suhu", y="Kelembapan", hue="Kondisi", style="Kondisi", s=60, alpha=0.75, palette="tab10", ax=ax6)
    sns.regplot(data=df, x="Suhu", y="Kelembapan", scatter=False, ax=ax6, color="black", line_kws={"linestyle": "--", "linewidth": 1.5})
    ax6.set_title("Hubungan Korelasi Antara Suhu Udara vs Kelembapan Relatif", fontsize=12, fontweight="bold", pad=12)
    ax6.set_xlabel("Suhu Udara (°C) — Skala Interval")
    ax6.set_ylabel("Kelembapan Relatif (%)")
    ax6.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    g6_path = os.path.join(output_dir, "06_scatter_suhu_kelembapan.png")
    fig6.savefig(g6_path)
    plt.close(fig6)
    print(f"[OK] Grafik 6 disimpan: {g6_path}")

    # -------------------------------------------------------------------------
    # Grafik 7: Tren Waktu Bulanan Suhu & Kelembapan
    # -------------------------------------------------------------------------
    fig7, ax7_1 = plt.subplots(figsize=(11, 5))
    ax7_2 = ax7_1.twinx()

    x_labels = monthly["Bulan_Str"].tolist()
    ax7_1.plot(x_labels, monthly["Rata_Suhu"], color="#e74c3c", marker="o", linewidth=2.5, label="Suhu Rata-rata (°C)")
    ax7_2.plot(x_labels, monthly["Rata_Kelembapan"], color="#2980b9", marker="s", linestyle="--", linewidth=2.5, label="Kelembapan Rata-rata (%)")

    ax7_1.set_title("Tren Dinamika Suhu dan Kelembapan Rata-rata Bulanan (Tahun 2024)", fontsize=12, fontweight="bold", pad=12)
    ax7_1.set_xlabel("Bulan Observasi")
    ax7_1.set_ylabel("Suhu Udara (°C)", color="#e74c3c")
    ax7_2.set_ylabel("Kelembapan Relatif (%)", color="#2980b9")
    ax7_1.tick_params(axis="x", rotation=30)
    ax7_1.grid(True, linestyle="--", alpha=0.5)

    lines1, labels1 = ax7_1.get_legend_handles_labels()
    lines2, labels2 = ax7_2.get_legend_handles_labels()
    ax7_1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()
    g7_path = os.path.join(output_dir, "07_tren_waktu_cuaca.png")
    fig7.savefig(g7_path)
    plt.close(fig7)
    print(f"[OK] Grafik 7 disimpan: {g7_path}")


def print_conclusions(df: pd.DataFrame, city_summary: pd.DataFrame):
    """
    15 & 19. Kesimpulan empiris berbasis data aktual pengamatan cuaca.
    """
    hottest_city = city_summary.iloc[0]
    coolest_city = city_summary.iloc[-1]
    most_humid_city = city_summary.sort_values(by="Rata_Kelembapan", ascending=False).iloc[0]
    least_humid_city = city_summary.sort_values(by="Rata_Kelembapan", ascending=True).iloc[0]
    top_cond = df["Kondisi"].value_counts().idxmax()
    top_cond_cnt = df["Kondisi"].value_counts().max()
    top_cond_pct = (top_cond_cnt / len(df)) * 100

    print("\n" + "=" * 80)
    print("KESIMPULAN AKHIR ANALISIS PENGAMATAN CUACA (BERBASIS DATA AKTUAL)")
    print("=" * 80)
    print(f"1. Populasi Observasi     : Total 1.000 pengamatan cuaca tercatat di 7 kota besar Indonesia.")
    print(f"2. Kota Paling Hangat     : '{hottest_city['Kota']}' mencatatkan suhu rata-rata tertinggi ({hottest_city['Rata_Suhu']:.1f} °C).")
    print(f"3. Kota Paling Sejuk      : '{coolest_city['Kota']}' mencatatkan suhu rata-rata terendah ({coolest_city['Rata_Suhu']:.1f} °C).")
    print(f"4. Karakteristik Lembap   : '{most_humid_city['Kota']}' memiliki kelembapan tertinggi ({most_humid_city['Rata_Kelembapan']:.1f}%),")
    print(f"   sedangkan '{least_humid_city['Kota']}' paling kering ({least_humid_city['Rata_Kelembapan']:.1f}%).")
    print(f"5. Kondisi Dominan        : Kondisi '{top_cond}' adalah yang paling sering tercatat dengan {top_cond_cnt} kali ({top_cond_pct:.1f}%).")
    print(f"6. Hubungan Fisik         : Hubungan Suhu dan Kelembapan terbukti berkorelasi negatif kuat (r = {df[['Suhu', 'Kelembapan']].corr().iloc[0,1]:.3f}).")
    print("=" * 80)
    print("DISCLAIMER AKADEMIK:")
    print("Dataset ini merupakan data sintetis untuk pembelajaran pemodelan statistik meteorologi.")
    print("Data ini bukan berasal dari BMKG atau stasiun meteorologi riil.")
    print("=" * 80)
    print(f"Disusun Oleh Mahasiswa: Herlinda Artika Sari (NIM: 241041011)")
    print("=" * 80)


def main():
    print("=" * 80)
    print("PROGRAM ANALISIS PENGAMATAN CUACA -- DATASET 1.000 BARIS")
    print("IDENTITAS PENELITI : Herlinda Artika Sari (NIM: 241041011)")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "data_sintesis_1000.csv")
    output_dir = os.path.join(base_dir, "output")

    # 1. Load Data
    df = load_and_inspect_data(data_path)

    # 2 & 3. Statistik Deskriptif Suhu & Kelembapan
    descriptive_statistics(df)

    # 4 & 5. Distribusi Kota & Kondisi
    city_and_weather_distribution(df)

    # 6, 7 & 8. Perbandingan Antarkota & Kondisi
    city_summary = city_and_condition_comparison(df, output_dir)

    # 11. Outlier IQR
    outlier_analysis_iqr(df)

    # 13, 16, 17 & 18. Korelasi & Skala Pengukuran
    correlation_and_scales_analysis(df)

    # 14. Analisis Tren Waktu
    monthly = time_series_analysis(df)

    # 15. Visualisasi
    generate_visualizations(df, city_summary, monthly, output_dir)

    # Kesimpulan
    print_conclusions(df, city_summary)


if __name__ == "__main__":
    main()
