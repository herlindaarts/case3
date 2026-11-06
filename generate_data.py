"""
================================================================================
PROYEK BEDAH KASUS 3 — DATASET PENGAMATAN CUACA
Skrip Pembangkitan Data Sintetis (Meteorological Data Generator)

IDENTITAS MAHASISWA:
- Nama Mahasiswa : Herlinda Artika Sari
- NIM            : 241041011
- Mata Kuliah    : Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca

DESKRIPSI:
Skrip ini menghasilkan dataset pengamatan cuaca sintetis sebanyak tepat 1.000
baris yang disimpan dalam 'data/data_sintesis_1000.csv'.
Kolom inti sesuai contoh dosen:
1. Kota       (Data Kategorik Nominal)
2. Suhu       (Data Numerik Skala Interval dalam °C)
3. Kelembapan (Data Numerik Persentase Kelembapan Relatif %)
4. Kondisi    (Data Kategorik Nominal)

Kolom Tambahan Analitik:
5. Tanggal    (Waktu pengamatan ISO YYYY-MM-DD untuk analisis tren temporal).
   *Catatan: Kolom Tanggal ditambahkan khusus untuk memperkaya analisis tren waktu
    dan bukan bagian dari 4 kolom awal dosen.*
================================================================================
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def generate_weather_dataset(
    n_rows: int = 1000,
    seed: int = 42,
    output_path: str = "data/data_sintesis_1000.csv"
) -> pd.DataFrame:
    """
    Menghasilkan dataset pengamatan cuaca sintetis sebanyak n_rows baris.
    
    Parameter:
    ----------
    n_rows : int
        Jumlah baris data yang ingin dihasilkan (default: 1000).
    seed : int
        Random seed untuk menjamin reproducibility dataset.
    output_path : str
        Jalur penyimpanan berkas CSV hasil pembangkitan data.
        
    Return:
    -------
    pd.DataFrame
        DataFrame yang berisi data pengamatan cuaca sintetis.
    """
    np.random.seed(seed)
    random.seed(seed)

    # Profil Klimatologi Dasar Kota (Baseline Suhu °C, Baseline Kelembapan %)
    # Memperhitungkan topografi (dataran tinggi vs pesisir)
    city_profiles = {
        "Jakarta": {"base_temp": 32.2, "base_humidity": 73, "weight": 0.18},
        "Surabaya": {"base_temp": 33.0, "base_humidity": 68, "weight": 0.16},
        "Bandung": {"base_temp": 23.8, "base_humidity": 83, "weight": 0.16},
        "Bogor": {"base_temp": 25.5, "base_humidity": 87, "weight": 0.14},
        "Medan": {"base_temp": 31.0, "base_humidity": 76, "weight": 0.13},
        "Yogyakarta": {"base_temp": 29.8, "base_humidity": 75, "weight": 0.12},
        "Denpasar": {"base_temp": 30.5, "base_humidity": 74, "weight": 0.11},
    }

    cities = list(city_profiles.keys())
    city_weights = [city_profiles[c]["weight"] for c in cities]

    # Kondisi Cuaca dan Pengaruhnya terhadap Suhu dan Kelembapan
    # Format: Kondisi: (delta_suhu, delta_kelembapan, base_prob)
    weather_conditions = {
        "Cerah": (+1.8, -10.0, 0.28),
        "Berawan": (+0.2, -2.0, 0.32),
        "Mendung": (-1.2, +7.0, 0.18),
        "Hujan": (-2.6, +14.0, 0.15),
        "Hujan Lebat": (-4.0, +20.0, 0.07),
    }
    conditions_list = list(weather_conditions.keys())
    condition_base_probs = [weather_conditions[k][2] for k in conditions_list]

    # Rentang tanggal: 1 Januari 2024 s/d 31 Desember 2024
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days + 1

    records = []

    chosen_cities = np.random.choice(cities, size=n_rows, p=city_weights)
    day_offsets = np.random.randint(0, total_days, size=n_rows)

    for i in range(n_rows):
        city = chosen_cities[i]
        profile = city_profiles[city]
        obs_date = start_date + timedelta(days=int(day_offsets[i]))

        # Sedikit variasi probabilitas kondisi cuaca per kota
        # Kota hujan (Bogor/Bandung) memiliki probabilitas hujan lebih tinggi
        if city in ["Bogor", "Bandung"]:
            c_probs = [0.18, 0.28, 0.20, 0.22, 0.12]
        elif city in ["Surabaya", "Jakarta"]:
            c_probs = [0.38, 0.32, 0.15, 0.11, 0.04]
        else:
            c_probs = condition_base_probs

        condition = np.random.choice(conditions_list, p=c_probs)
        temp_delta, hum_delta, _ = weather_conditions[condition]

        # Efek musiman: Bulan basah (Jan-Mar, Okt-Des) vs bulan kering (Mei-Sep)
        month = obs_date.month
        if month in [1, 2, 3, 11, 12]:
            season_temp_adj = -0.5
            season_hum_adj = +4.0
        elif month in [6, 7, 8]:
            season_temp_adj = +0.6
            season_hum_adj = -5.0
        else:
            season_temp_adj = 0.0
            season_hum_adj = 0.0

        # Gangguan acak realistis (meteorological random noise)
        temp_noise = np.random.normal(0, 1.1)
        hum_noise = np.random.normal(0, 4.5)

        # Perhitungan Suhu (°C)
        calc_temp = profile["base_temp"] + temp_delta + season_temp_adj + temp_noise
        # Batasi rentang fisik realistis iklim Indonesia (17.0 s/d 38.0 °C)
        temp_val = float(np.clip(calc_temp, 17.0, 38.0))
        temp_val = round(temp_val, 1)

        # Perhitungan Kelembapan Relatif (%)
        calc_hum = profile["base_humidity"] + hum_delta + season_hum_adj + hum_noise
        # Batasi rentang persentase fisik (40% s/d 99%)
        hum_val = int(round(np.clip(calc_hum, 40.0, 99.0)))

        records.append({
            "Kota": city,
            "Suhu": temp_val,
            "Kelembapan": hum_val,
            "Kondisi": condition,
            "Tanggal": obs_date.strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(records)

    # Urutkan berdasarkan Tanggal dan Kota agar menyerupai log observasi meteorologi
    df["Tanggal_Parsed"] = pd.to_datetime(df["Tanggal"])
    df = df.sort_values(by=["Tanggal_Parsed", "Kota"]).reset_index(drop=True)
    df = df.drop(columns=["Tanggal_Parsed"])

    # Pastikan direktori tujuan tersedia
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Simpan ke CSV
    df.to_csv(output_path, index=False)

    print("================================================================================")
    print("DATASET PENGAMATAN CUACA SINTETIS BERHASIL DIBUAT")
    print("================================================================================")
    print(f"Penyusun       : Herlinda Artika Sari (NIM: 241041011)")
    print(f"Lokasi Berkas  : {output_path}")
    print(f"Jumlah Baris   : {len(df)} baris (tepat 1.000 baris data)")
    print(f"Kolom Inti     : ['Kota', 'Suhu', 'Kelembapan', 'Kondisi']")
    print(f"Kolom Analisis : ['Tanggal'] (ekstensi analitik runtun waktu)")
    print(f"Rentang Suhu   : {df['Suhu'].min():.1f} °C s/d {df['Suhu'].max():.1f} °C")
    print(f"Rentang Lembap : {df['Kelembapan'].min()}% s/d {df['Kelembapan'].max()}%")
    print(f"Daftar Kota    : {sorted(df['Kota'].unique().tolist())}")
    print(f"Daftar Kondisi : {sorted(df['Kondisi'].unique().tolist())}")
    print("Catatan        : Data ini adalah data sintetis untuk keperluan pembelajaran,")
    print("                 bukan data pengamatan riil BMKG.")
    print("================================================================================")

    return df


if __name__ == "__main__":
    generate_weather_dataset()
