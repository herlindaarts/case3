"""
================================================================================
PROYEK BEDAH KASUS 3 — DATASET PENGAMATAN CUACA
Aplikasi Dashboard Interaktif Streamlit (Weather Observation Analytics)

IDENTITAS MAHASISWA:
- Nama Mahasiswa : Herlinda Artika Sari
- NIM            : 241041011
- Mata Kuliah    : Bedah Kasus 3 — Analisis Dataset Pengamatan Cuaca

DESKRIPSI:
Aplikasi dashboard interaktif modern, bersih, profesional, dan responsif
yang dibangun dengan Streamlit dan Plotly. Menyajikan pemantauan KPI cuaca,
distribusi frekuensi kondisi atmosfer, perbandingan iklim mikro antarkota,
analisis sebaran suhu & kelembapan, scatter plot korelasi fisik udara,
tren temporal sepanjang tahun 2024, serta wawasan otomatis (automated insights).
================================================================================
"""

import os
import io
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Weather Observation Analytics — Herlinda Artika Sari",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS modern bertema meteorologi profesional
st.markdown("""
<style>
    /* Styling Header & Identitas */
    .weather-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #009ffd 100%);
        color: white;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0, 159, 253, 0.2);
    }
    .weather-header h2 {
        color: #ffffff;
        margin: 0;
        font-size: 1.65rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .weather-header p {
        color: #e0f2fe;
        margin: 6px 0 0 0;
        font-size: 0.95rem;
    }
    
    /* KPI Metric Cards */
    .metric-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0284c7;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* Automated Insight Box */
    .insight-box {
        background-color: #f0fdfa;
        border-left: 4px solid #0d9488;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .insight-box h4 {
        margin: 0 0 8px 0;
        color: #115e59;
        font-size: 1.05rem;
    }

    /* Glosarium Teori Box */
    .theory-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 30px 0 10px 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. FUNGSI PEMUATAN DATASET
# ==============================================================================
@st.cache_data
def load_weather_data() -> pd.DataFrame:
    """
    Memuat dataset cuaca dari 'data/data_sintesis_1000.csv'.
    Jika berkas belum ada, otomatis memicu generate_weather_dataset().
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "data_sintesis_1000.csv")

    if not os.path.exists(data_path):
        from generate_data import generate_weather_dataset
        df = generate_weather_dataset(output_path=data_path)
    else:
        df = pd.read_csv(data_path)

    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    df["Suhu"] = df["Suhu"].astype(float)
    df["Kelembapan"] = df["Kelembapan"].astype(int)
    return df


try:
    df_raw = load_weather_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()


# ==============================================================================
# 3. SIDEBAR: IDENTITAS MAHASISWA & FILTER ANALISIS
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎓 Identitas Mahasiswa")
    st.markdown("""
    **Nama:** Herlinda Artika Sari  
    **NIM:** 241041011  
    **Program:** Bedah Kasus 3  
    **Topik:** Dataset Pengamatan Cuaca  
    """)
    st.markdown("---")

    st.markdown("### 🔍 Filter Analisis Cuaca")

    # 1. Filter Rentang Tanggal
    min_date = df_raw["Tanggal"].min().date()
    max_date = df_raw["Tanggal"].max().date()
    date_range = st.date_input(
        "Pilih Rentang Tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Saring periode observasi cuaca sepanjang tahun."
    )

    # 2. Filter Kota
    all_cities = sorted(df_raw["Kota"].unique().tolist())
    selected_cities = st.multiselect(
        "Pilih Kota:",
        options=all_cities,
        default=all_cities,
        help="Pilih satu atau lebih stasiun kota observasi."
    )

    # 3. Filter Kondisi Cuaca
    all_conditions = sorted(df_raw["Kondisi"].unique().tolist())
    selected_conditions = st.multiselect(
        "Pilih Kondisi Cuaca:",
        options=all_conditions,
        default=all_conditions,
        help="Saring data berdasarkan kategori cuaca teramati."
    )

    # 4. Filter Rentang Suhu
    min_temp = float(df_raw["Suhu"].min())
    max_temp = float(df_raw["Suhu"].max())
    temp_range = st.slider(
        "Rentang Suhu Udara (°C):",
        min_value=min_temp,
        max_value=max_temp,
        value=(min_temp, max_temp),
        step=0.5,
        format="%.1f °C"
    )

    # 5. Filter Rentang Kelembapan
    min_hum = int(df_raw["Kelembapan"].min())
    max_hum = int(df_raw["Kelembapan"].max())
    hum_range = st.slider(
        "Rentang Kelembapan Relatif (%):",
        min_value=min_hum,
        max_value=max_hum,
        value=(min_hum, max_hum),
        step=1,
        format="%d%%"
    )

    st.markdown("---")
    st.caption("ℹ️ *Data merupakan 1.000 data pengamatan sintetis untuk pembelajaran pemodelan meteorologi.*")


# ==============================================================================
# 4. PENYARINGAN DATA AKTIF (FILTERING)
# ==============================================================================
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_filter, end_filter = date_range
else:
    start_filter = min_date
    end_filter = max_date

mask = (
    (df_raw["Tanggal"].dt.date >= start_filter) &
    (df_raw["Tanggal"].dt.date <= end_filter) &
    (df_raw["Kota"].isin(selected_cities)) &
    (df_raw["Kondisi"].isin(selected_conditions)) &
    (df_raw["Suhu"] >= temp_range[0]) &
    (df_raw["Suhu"] <= temp_range[1]) &
    (df_raw["Kelembapan"] >= hum_range[0]) &
    (df_raw["Kelembapan"] <= hum_range[1])
)
df_filtered = df_raw[mask].copy()


# ==============================================================================
# 5. HEADER UTAMA DASHBOARD
# ==============================================================================
st.markdown("""
<div class="weather-header">
    <h2>⛅ Weather Observation Analytics</h2>
    <p>Bedah Kasus 3: Analisis Komprehensif Dataset Pengamatan Cuaca & Dinamika Iklim Mikro</p>
    <p style="margin-top: 8px; font-weight: 500;">
        👤 <strong>Herlinda Artika Sari</strong> | NIM: <strong>241041011</strong> | 📂 1.000 Baris Data Cuaca Sintetis
    </p>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 6. PENANGANAN FILTER KOSONG (EMPTY STATE)
# ==============================================================================
if df_filtered.empty:
    st.warning("⚠️ Tidak ada data observasi cuaca yang memenuhi kombinasi kriteria filter yang Anda pilih.")
    st.info("💡 **Solusi:** Perluas rentang suhu atau kelembapan di sidebar, atau centang lebih banyak kota/kondisi cuaca.")
    st.stop()


# ==============================================================================
# 7. KARTU KPI UTAMA (METRICS OVERVIEW)
# ==============================================================================
total_obs = len(df_filtered)
avg_temp = df_filtered["Suhu"].mean()
avg_hum = df_filtered["Kelembapan"].mean()
total_cities = df_filtered["Kota"].nunique()

col_k1, col_k2, col_k3, col_k4 = st.columns(4)

with col_k1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #0284c7;">
        <div class="metric-title">Total Pengamatan Aktif</div>
        <div class="metric-value">{total_obs:,} <span style="font-size: 1rem; font-weight: normal;">log</span></div>
        <div class="metric-sub">{(total_obs / len(df_raw) * 100):.1f}% dari 1.000 total data</div>
    </div>
    """, unsafe_allow_html=True)

with col_k2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #ea580c;">
        <div class="metric-title">Suhu Rata-rata</div>
        <div class="metric-value">{avg_temp:.1f} <span style="font-size: 1rem; font-weight: normal;">°C</span></div>
        <div class="metric-sub">Median: {df_filtered['Suhu'].median():.1f} °C | Std: {df_filtered['Suhu'].std():.2f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with col_k3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #0d9488;">
        <div class="metric-title">Kelembapan Rata-rata</div>
        <div class="metric-value">{avg_hum:.1f} <span style="font-size: 1rem; font-weight: normal;">%</span></div>
        <div class="metric-sub">Median: {df_filtered['Kelembapan'].median():.0f}% | Std: {df_filtered['Kelembapan'].std():.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col_k4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #7c3aed;">
        <div class="metric-title">Cakupan Wilayah</div>
        <div class="metric-value">{total_cities} <span style="font-size: 1rem; font-weight: normal;">kota</span></div>
        <div class="metric-sub">{df_filtered['Kondisi'].nunique()} kondisi cuaca unik teramati</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 8. TABS ANALISIS MULTI-PERSPEKTIF
# ==============================================================================
tab_overview, tab_city, tab_distribution, tab_correlation, tab_trend, tab_data, tab_theory = st.tabs([
    "🌦️ Kondisi Cuaca",
    "🏙️ Komparasi Antarkota",
    "📊 Sebaran & Outlier",
    "🔗 Korelasi Suhu vs Lembap",
    "📈 Tren Waktu (Temporal)",
    "📋 Data Explorer",
    "📖 Teori Skala Pengukuran"
])

# ------------------------------------------------------------------------------
# TAB 1: KONDISI CUACA
# ------------------------------------------------------------------------------
with tab_overview:
    st.subheader("Distribusi Kondisi Cuaca & Karakteristik Termal")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        cond_counts = df_filtered["Kondisi"].value_counts().reset_index()
        cond_counts.columns = ["Kondisi", "Jumlah"]
        fig_cond_bar = px.bar(
            cond_counts,
            x="Kondisi",
            y="Jumlah",
            color="Kondisi",
            title="Frekuensi Observasi Tiap Kondisi Cuaca",
            text="Jumlah",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_cond_bar.update_layout(
            xaxis=dict(title=""),
            yaxis=dict(title="Jumlah Hari Pengamatan"),
            showlegend=False,
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_cond_bar, use_container_width=True)

    with col_c2:
        fig_cond_pie = px.pie(
            cond_counts,
            names="Kondisi",
            values="Jumlah",
            hole=0.45,
            title="Proporsi Kondisi Cuaca Teramati (%)",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_cond_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_cond_pie.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_cond_pie, use_container_width=True)

    # Karakteristik Kondisi Cuaca
    st.markdown("#### Karakteristik Rata-rata Suhu & Kelembapan Tiap Kondisi Cuaca")
    cond_summary = df_filtered.groupby("Kondisi").agg(
        Jumlah=("Suhu", "count"),
        Rata_Suhu=("Suhu", "mean"),
        Median_Suhu=("Suhu", "median"),
        Rata_Lembap=("Kelembapan", "mean"),
        Median_Lembap=("Kelembapan", "median")
    ).reset_index().sort_values(by="Rata_Suhu", ascending=False)

    st.dataframe(
        cond_summary.rename(columns={
            "Rata_Suhu": "Rata-rata Suhu (°C)",
            "Median_Suhu": "Median Suhu (°C)",
            "Rata_Lembap": "Rata-rata Lembap (%)",
            "Median_Lembap": "Median Lembap (%)",
            "Jumlah": "Jumlah Hari Teramati"
        }).round({"Rata-rata Suhu (°C)": 1, "Median Suhu (°C)": 1, "Rata-rata Lembap (%)": 1, "Median Lembap (%)": 0}),
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------------------------
# TAB 2: KOMPARASI ANTARKOTA
# ------------------------------------------------------------------------------
with tab_city:
    st.subheader("Perbandingan Iklim Mikro Antarkota")

    col_ct1, col_ct2 = st.columns(2)

    city_stats = df_filtered.groupby("Kota").agg(
        Rata_Suhu=("Suhu", "mean"),
        Rata_Kelembapan=("Kelembapan", "mean"),
        Min_Suhu=("Suhu", "min"),
        Max_Suhu=("Suhu", "max"),
        Jumlah_Pengamatan=("Suhu", "count")
    ).reset_index()

    with col_ct1:
        # Peringkat Suhu Rata-rata
        fig_city_temp = px.bar(
            city_stats.sort_values(by="Rata_Suhu", ascending=True),
            x="Rata_Suhu",
            y="Kota",
            orientation="h",
            color="Rata_Suhu",
            title="Suhu Rata-rata per Kota (°C)",
            text=city_stats.sort_values(by="Rata_Suhu", ascending=True)["Rata_Suhu"].apply(lambda v: f"{v:.1f} °C"),
            color_continuous_scale="Reds"
        )
        fig_city_temp.update_layout(
            xaxis=dict(title="Suhu (°C)", range=[15, 38]),
            yaxis=dict(title=""),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_city_temp, use_container_width=True)

    with col_ct2:
        # Peringkat Kelembapan Rata-rata
        fig_city_hum = px.bar(
            city_stats.sort_values(by="Rata_Kelembapan", ascending=True),
            x="Rata_Kelembapan",
            y="Kota",
            orientation="h",
            color="Rata_Kelembapan",
            title="Kelembapan Relatif Rata-rata per Kota (%)",
            text=city_stats.sort_values(by="Rata_Kelembapan", ascending=True)["Rata_Kelembapan"].apply(lambda v: f"{v:.1f}%"),
            color_continuous_scale="Blues"
        )
        fig_city_hum.update_layout(
            xaxis=dict(title="Kelembapan (%)", range=[40, 100]),
            yaxis=dict(title=""),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_city_hum, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 3: SEBARAN & OUTLIER
# ------------------------------------------------------------------------------
with tab_distribution:
    st.subheader("Distribusi Probabilitas & Evaluasi Pencilan (Outlier IQR)")

    col_dst1, col_dst2 = st.columns(2)

    with col_dst1:
        # Histogram Suhu
        fig_h_temp = px.histogram(
            df_filtered,
            x="Suhu",
            nbins=30,
            title="Histogram Sebaran Suhu Udara (°C)",
            color_discrete_sequence=["#f97316"]
        )
        fig_h_temp.add_vline(
            x=df_filtered["Suhu"].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {df_filtered['Suhu'].mean():.1f} °C"
        )
        fig_h_temp.add_vline(
            x=df_filtered["Suhu"].median(),
            line_dash="dot",
            line_color="blue",
            annotation_text=f"Median: {df_filtered['Suhu'].median():.1f} °C"
        )
        fig_h_temp.update_layout(
            xaxis=dict(title="Suhu (°C)"),
            yaxis=dict(title="Frekuensi"),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_h_temp, use_container_width=True)

    with col_dst2:
        # Histogram Kelembapan
        fig_h_hum = px.histogram(
            df_filtered,
            x="Kelembapan",
            nbins=30,
            title="Histogram Sebaran Kelembapan Relatif (%)",
            color_discrete_sequence=["#0ea5e9"]
        )
        fig_h_hum.add_vline(
            x=df_filtered["Kelembapan"].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {df_filtered['Kelembapan'].mean():.1f}%"
        )
        fig_h_hum.add_vline(
            x=df_filtered["Kelembapan"].median(),
            line_dash="dot",
            line_color="green",
            annotation_text=f"Median: {df_filtered['Kelembapan'].median():.0f}%"
        )
        fig_h_hum.update_layout(
            xaxis=dict(title="Kelembapan Relatif (%)"),
            yaxis=dict(title="Frekuensi"),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_h_hum, use_container_width=True)

    # Box Plot Suhu & Kelembapan per Kota
    st.markdown("---")
    st.markdown("#### Box Plot Sebaran Parameter Cuaca per Kota (Deteksi Outlier IQR)")

    col_bx1, col_bx2 = st.columns(2)
    with col_bx1:
        fig_bx_temp = px.box(
            df_filtered,
            x="Kota",
            y="Suhu",
            color="Kota",
            points="all",
            title="Box Plot Sebaran Suhu per Kota (°C)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bx_temp.update_layout(xaxis=dict(title=""), showlegend=False, height=380)
        st.plotly_chart(fig_bx_temp, use_container_width=True)

    with col_bx2:
        fig_bx_hum = px.box(
            df_filtered,
            x="Kota",
            y="Kelembapan",
            color="Kota",
            points="all",
            title="Box Plot Sebaran Kelembapan per Kota (%)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bx_hum.update_layout(xaxis=dict(title=""), showlegend=False, height=380)
        st.plotly_chart(fig_bx_hum, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 4: KORELASI SUHU VS KELEMBAPAN
# ------------------------------------------------------------------------------
with tab_correlation:
    st.subheader("Hubungan Fisik Antara Suhu Udara dan Kelembapan Relatif")

    fig_sc = px.scatter(
        df_filtered,
        x="Suhu",
        y="Kelembapan",
        color="Kondisi",
        hover_name="Kota",
        trendline="ols",
        title="Scatter Plot: Hubungan Suhu (°C) vs Kelembapan Relatif (%) dengan Garis Tren OLS",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig_sc.update_layout(
        xaxis=dict(title="Suhu Udara (°C) — Skala Interval"),
        yaxis=dict(title="Kelembapan Relatif (%)"),
        height=450
    )
    st.plotly_chart(fig_sc, use_container_width=True)

    corr_val = df_filtered[["Suhu", "Kelembapan"]].corr().iloc[0, 1]
    st.markdown(f"""
    <div class="insight-box">
        <h4>Analisis Korelasi & Refleksi Kausalitas:</h4>
        <ul>
            <li><strong>Koefisien Korelasi Pearson (r):</strong> <code>{corr_val:.4f}</code> (Korelasi Negatif Kuat).</li>
            <li><strong>Makna Termodinamika:</strong> Sesuai persamaan Clausius-Clapeyron, peningkatan suhu meningkatkan kapasitas udara dalam menampung uap air sebelum mencapai titik jenuh (*saturation vapor pressure*). Akibatnya, pada massa uap air yang sama, peningkatan suhu menurunkan nilai kelembapan relatif (*relative humidity*).</li>
            <li><strong>Peringatan Kausalitas (Correlation ≠ Causation):</strong> Hubungan statistik ini tidak membuktikan bahwa perubahan suhu secara sepihak menjadi satu-satunya penyebab perubahan kelembapan. Faktor eksternal lain seperti pergerakan massa udara, radiasi matahari, dan evaporasi lokal saling mempengaruhi secara simultan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 5: TREN WAKTU
# ------------------------------------------------------------------------------
with tab_trend:
    st.subheader("Tren Dinamika Suhu & Kelembapan Sepanjang Periode Waktu")
    st.caption("ℹ️ *Fitur ini memanfaatkan kolom tambahan 'Tanggal' yang diekstensikan khusus untuk analisis runtun waktu.*")

    col_t_opt, _ = st.columns([2, 4])
    with col_t_opt:
        freq_opt = st.selectbox("Pilih Agregasi Waktu:", ["Bulanan (Monthly)", "Mingguan (Weekly)", "Harian (Daily)"])

    df_t = df_filtered.copy()
    if "Bulanan" in freq_opt:
        df_t["Periode"] = df_t["Tanggal"].dt.to_period("M").dt.to_timestamp()
    elif "Mingguan" in freq_opt:
        df_t["Periode"] = df_t["Tanggal"].dt.to_period("W").dt.start_time
    else:
        df_t["Periode"] = df_t["Tanggal"].dt.date

    t_grp = df_t.groupby("Periode").agg(
        Rata_Suhu=("Suhu", "mean"),
        Rata_Lembap=("Kelembapan", "mean"),
        Pengamatan=("Suhu", "count")
    ).reset_index()

    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        x=t_grp["Periode"],
        y=t_grp["Rata_Suhu"],
        name="Suhu Rata-rata (°C)",
        mode="lines+markers",
        line=dict(color="#ef4444", width=3),
        hovertemplate="Periode: %{x}<br>Suhu: %{y:.1f} °C<extra></extra>"
    ))
    fig_time.add_trace(go.Scatter(
        x=t_grp["Periode"],
        y=t_grp["Rata_Lembap"],
        name="Kelembapan Rata-rata (%)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#0284c7", width=3, dash="dot"),
        hovertemplate="Periode: %{x}<br>Kelembapan: %{y:.1f}%<extra></extra>"
    ))
    fig_time.update_layout(
        title=f"Pergerakan Suhu dan Kelembapan Rata-rata ({freq_opt.split()[0]})",
        yaxis=dict(title="Suhu (°C)", titlefont=dict(color="#ef4444"), tickfont=dict(color="#ef4444")),
        yaxis2=dict(title="Kelembapan (%)", titlefont=dict(color="#0284c7"), tickfont=dict(color="#0284c7"), overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        height=420,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_time, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 6: DATA EXPLORER & UNDUH CSV
# ------------------------------------------------------------------------------
with tab_data:
    st.subheader("Eksplorasi Data Tabular Pengamatan Cuaca")
    st.write(f"Menampilkan **{len(df_filtered):,}** dari total **{len(df_raw):,}** baris data observasi cuaca aktif.")

    search_txt = st.text_input("🔍 Cari Kota atau Kondisi Cuaca:", "")
    df_show = df_filtered.copy()
    if search_txt:
        df_show = df_show[
            df_show["Kota"].str.contains(search_txt, case=False) |
            df_show["Kondisi"].str.contains(search_txt, case=False)
        ]

    # Format tampilan
    df_show_fmt = df_show.copy()
    df_show_fmt["Tanggal"] = df_show_fmt["Tanggal"].dt.strftime("%Y-%m-%d")
    df_show_fmt["Suhu"] = df_show_fmt["Suhu"].apply(lambda v: f"{v:.1f} °C")
    df_show_fmt["Kelembapan"] = df_show_fmt["Kelembapan"].apply(lambda v: f"{v}%")

    st.dataframe(
        df_show_fmt[["Kota", "Suhu", "Kelembapan", "Kondisi", "Tanggal"]],
        use_container_width=True,
        height=360,
        hide_index=True
    )

    # Tombol Unduh CSV
    csv_buf = io.StringIO()
    df_filtered.to_csv(csv_buf, index=False)
    csv_data = csv_buf.getvalue().encode("utf-8")

    st.download_button(
        label="📥 Unduh Data Cuaca Tersaring (CSV)",
        data=csv_data,
        file_name=f"cuaca_filtered_{datetime.date.today()}.csv",
        mime="text/csv",
        help="Unduh data pengamatan cuaca aktif ke berkas CSV."
    )


# ------------------------------------------------------------------------------
# TAB 7: GLOSARIUM TEORI SKALA PENGUKURAN
# ------------------------------------------------------------------------------
with tab_theory:
    st.subheader("Glosarium Teori Skala Pengukuran & Metodologi Sains Data")

    col_th1, col_th2 = st.columns(2)

    with col_th1:
        st.markdown("""
        <div class="theory-box">
            <h4>🌡️ Teori Skala Pengukuran Data Cuaca:</h4>
            <ul>
                <li><strong>Suhu (°C) — Skala Interval:</strong> Memiliki jarak yang bermakna (selisih 30°C - 20°C = 10°C), tetapi titik nol (0°C) adalah titik beku air pada 1 atm, BUKAN ketiadaan panas mutlak. Oleh sebab itu, <strong>20°C bukan berarti dua kali lebih panas dari 10°C</strong>.</li>
                <li><strong>Kelembapan (%) — Kelembapan Relatif (RH):</strong> Rasio tekanan uap air terhadap tekanan jenuh dikali 100%. Memiliki nilai nol fisik (udara kering), namun nilai persentase bersifat komparasi relatif terhadap kapasitas udara pada suhu terkait.</li>
                <li><strong>Kota & Kondisi — Skala Nominal:</strong> Label kategorik murni tanpa peringkat atau hierarki matematis (misal: 'Jakarta' tidak lebih tinggi dari 'Bandung').</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_th2:
        st.markdown("""
        <div class="theory-box">
            <h4>📋 Keterbatasan Metodologi & Disclaimer:</h4>
            <ul>
                <li><strong>Data Sintetis:</strong> Seluruh 1.000 baris data dibangkitkan secara komputasi dengan random seed untuk keperluan edukasi analitik data.</li>
                <li><strong>Bukan Data BMKG:</strong> Data ini tidak bersumber dari stasiun pengamatan resmi BMKG atau sensor meteorologi aktual.</li>
                <li><strong>Kolom Tanggal:</strong> Kolom 'Tanggal' merupakan penambahan terarah untuk memfasilitasi analisis runtun waktu (*time-series*) yang memperkaya 4 kolom dasar dosen.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 9. BAGIAN INSIGHT OTOMATIS BERBASIS DATA AKTIF
# ==============================================================================
st.markdown("---")
st.subheader("💡 Ringkasan Wawasan Meteorologi Otomatis (Automated Insights)")

hottest_c = df_filtered.groupby("Kota")["Suhu"].mean().idxmax()
hottest_c_val = df_filtered.groupby("Kota")["Suhu"].mean().max()

coolest_c = df_filtered.groupby("Kota")["Suhu"].mean().idxmin()
coolest_c_val = df_filtered.groupby("Kota")["Suhu"].mean().min()

humid_c = df_filtered.groupby("Kota")["Kelembapan"].mean().idxmax()
humid_c_val = df_filtered.groupby("Kota")["Kelembapan"].mean().max()

dominant_cond = df_filtered["Kondisi"].value_counts().idxmax()
dominant_cond_cnt = df_filtered["Kondisi"].value_counts().max()
dominant_cond_pct = (dominant_cond_cnt / total_obs) * 100

st.markdown(f"""
<div class="insight-box">
    <h4>Temuan Kunci Berdasarkan Data Aktif:</h4>
    <ul>
        <li><strong>Kota Terpanas:</strong> Kota <strong>{hottest_c}</strong> mencatat suhu rata-rata tertinggi sebesar <strong>{hottest_c_val:.1f} °C</strong>.</li>
        <li><strong>Kota Paling Sejuk:</strong> Kota <strong>{coolest_c}</strong> memiliki suhu rata-rata terendah yaitu <strong>{coolest_c_val:.1f} °C</strong> (selisih topografi <strong>{(hottest_c_val - coolest_c_val):.1f} °C</strong>).</li>
        <li><strong>Wilayah Paling Lembap:</strong> Kota <strong>{humid_c}</strong> memiliki tingkat kelembapan relatif tertinggi yaitu <strong>{humid_c_val:.1f}%</strong>.</li>
        <li><strong>Kondisi Cuaca Dominan:</strong> Kondisi <strong>{dominant_cond}</strong> paling sering teramati dengan frekuensi <strong>{dominant_cond_cnt} kali ({dominant_cond_pct:.1f}%)</strong> dari data aktif.</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 10. FOOTER IDENTITAS MAHASISWA
# ==============================================================================
st.markdown(f"""
<div class="footer-text">
    <strong>Proyek Bedah Kasus 3: Dataset Pengamatan Cuaca</strong><br>
    Disusun oleh: <strong>Herlinda Artika Sari</strong> | NIM: <strong>241041011</strong><br>
    Dibangun menggunakan Python, Streamlit, Pandas, NumPy, dan Plotly | Tahun Akademik 2024/2025
</div>
""", unsafe_allow_html=True)
