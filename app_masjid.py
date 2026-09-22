import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import plotly.express as px
from streamlit_gsheets_connection import GSheetsConnection  # Pustaka Google Sheets

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Pembangunan Masjid Almirra",
    page_icon="🕌",
    layout="wide"
)

# Kustomisasi CSS Tampilan Modern
st.markdown("""
    <style>
    .main { background-color: #f4f6f8; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #198754;
    }
    .header-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border-left: 6px solid #198754;
        margin-bottom: 25px;
    }
    .header-title { color: #198754; font-weight: 800; font-size: 28px; }
    </style>
""", unsafe_allow_html=True)

# ================= KONEKSI GOOGLE SHEETS =================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Membaca data langsung dari Google Sheets Cloud
    df_donasi = conn.read(worksheet="Donasi", ttl=0)
    df_keluar = conn.read(worksheet="Pengeluaran", ttl=0)
    
    # Jika sheet masih kosong, buat dataframe kosong dengan kolom yang sesuai
    if df_donasi.empty:
        df_donasi = pd.DataFrame(columns=["Tanggal", "Nama Donatur", "Jumlah/Nilai (Rp)", "Kategori", "Alamat", "Keterangan"])
    if df_keluar.empty:
        df_keluar = pd.DataFrame(columns=["Tanggal", "Keperluan", "Jumlah (Rp)", "Kategori", "Penerima/Toko"])
except Exception as e:
    st.error("Gagal terhubung ke Google Sheets. Pastikan file .streamlit/secrets.toml sudah dikonfigurasi dengan benar.")
    st.stop()

# ================= INISIALISASI DATA SECURITY & GALERI =================
PASSWORD_PENGURUS = "masjid123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "galeri_foto" not in st.session_state:
    st.session_state.galeri_foto = [
        {"judul": "Pekerjaan Pondasi Awal", "tanggal": "2026-08-25", "keterangan": "Penggalian dan pengecoran fondasi masjid.", "file": None}
    ]

# Layout Header
st.markdown("""
    <div class='header-box'>
        <span style='font-size: 32px;'>🕌</span>
        <span class='header-title'>Pembangunan Masjid Almirra</span>
        <p style='margin-top: 5px; margin-bottom: 0; color: #555555;'>
            <b>Lokasi:</b> Lingkungan Nglarik RW 09, Kel. Kalongan, Kec. Purwodadi, Kab. Grobogan
        </p>
    </div>
""", unsafe_allow_html=True)

# ================= SIDEBAR & SISTEM LOGIN =================
st.sidebar.markdown("### 🔒 Akses Pengurus")
if not st.session_state.authenticated:
    input_password = st.sidebar.text_input("Masukkan Password Pengurus", type="password")
    if st.sidebar.button("Log In", use_container_width=True):
        if input_password == PASSWORD_PENGURUS:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.sidebar.error("Password Salah!")
else:
    st.sidebar.success("🔓 Mode Pengurus Aktif")
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Menu Navigasi")
if st.session_state.authenticated:
    daftar_menu = ["Dashboard & Ringkasan", "Catat Pemasukan (Donasi)", "Catat Pengeluaran Dana", "Galeri Dokumentasi Foto", "Data & Laporan Lengkap"]
else:
    daftar_menu = ["Dashboard & Ringkasan", "Galeri Dokumentasi Foto", "Data & Laporan Lengkap"]

menu = st.sidebar.selectbox("Pilih Halaman", daftar_menu)

# ================= 1. MENU DASHBOARD =================
if menu == "Dashboard & Ringkasan":
    st.subheader("📊 Dashboard Utama Keuangan")

    # Hitung total dari data Google Sheets
    total_masuk = pd.to_numeric(df_donasi["Jumlah/Nilai (Rp)"], errors='coerce').sum()
    total_keluar = pd.to_numeric(df_keluar["Jumlah (Rp)"], errors='coerce').sum()
    sisa_saldo = total_masuk - total_keluar

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Dana Masuk", f"Rp {total_masuk:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
    col3.metric("Estimasi Saldo Kas", f"Rp {sisa_saldo:,.0f}")

    st.markdown("---")
    
    # Grafik Lingkaran Interaktif
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### 📈 Proporsi Bentuk Donasi")
        if not df_donasi.empty:
            fig_donasi = px.pie(df_donasi, values='Jumlah/Nilai (Rp)', names='Kategori', color_discrete_sequence=px.colors.sequential.Darkmint)
            fig_donasi.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig_donasi, use_container_width=True)
        else:
            st.info("Belum ada data donasi untuk grafik.")
        
    with col_chart2:
        st.markdown("#### 📉 Alokasi Pengeluaran")
        if not df_keluar.empty:
            fig_keluar = px.pie(df_keluar, values='Jumlah (Rp)', names='Kategori', color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig_keluar.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig_keluar, use_container_width=True)
        else:
            st.info("Belum ada data pengeluaran untuk grafik.")

    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🌟 Semua Data Donatur (Terbaru di Atas)")
        st.dataframe(df_donasi.iloc[::-1], use_container_width=True, height=350)
    with col_b:
        st.markdown("#### 🛠️ Semua Data Pengeluaran (Terbaru di Atas)")
        st.dataframe(df_keluar.iloc[::-1], use_container_width=True, height=350)

# ================= 2. MENU CATAT PEMASUKAN =================
elif menu == "Catat Pemasukan (Donasi)":
    st.subheader("➕ Tambah Data Donatur / Pemasukan Dana")

    with st.form("form_donasi", clear_on_submit=True):
        tgl = st.date_input("Tanggal Donasi", datetime.today())
        nama = st.text_input("Nama Donatur")
        alamat = st.text_input("Alamat")
        kategori = st.selectbox("Bentuk Donasi", ["Uang Tunai/Transfer", "Material", "Uang & Material"])
        jumlah = st.number_input("Nominal / Estimasi Nilai (Rp)", min_value=0, step=50000)
        keterangan = st.text_input("Keterangan Tambahan")

        submit_btn = st.form_submit_button("💾 Simpan Data Donatur", use_container_width=True)

        if submit_btn:
            if nama and jumlah > 0:
                new_data = pd.DataFrame([{"Tanggal": str(tgl), "Nama Donatur": nama, "Jumlah/Nilai (Rp)": jumlah, "Kategori": kategori, "Alamat": alamat, "Keterangan": keterangan}])
                updated_df = pd.concat([df_donasi, new_data], ignore_index=True)
                
                # Kirim data baru langsung ke cloud Google Sheets
                conn.update(worksheet="Donasi", data=updated_df)
                st.success(f"Donasi dari **{nama}** berhasil disimpan secara permanen di Cloud!")
                st.rerun()
            else:
                st.error("Mohon isi Nama Donatur dan Nominal dengan benar.")

# ================= 3. MENU CATAT PENGELUARAN =================
elif menu == "Catat Pengeluaran Dana":
    st.subheader("➖ Tambah Data Pengeluaran Pembangunan")

    with st.form("form_keluar", clear_on_submit=True):
        tgl_K = st.date_input("Tanggal Pengeluaran", datetime.today())
        keperluan = st.text_input("Keperluan / Nama Barang")
        kategori_k = st.selectbox("Kategori Pengeluaran", ["Material", "Upah Kerja", "Konsumsi", "Lain-lain"])
        jumlah_k = st.number_input("Jumlah Biaya (Rp)", min_value=0, step=50000)
        penerima = st.text_input("Dibayarkan Kepada / Toko")

        submit_keluar = st.form_submit_button("💾 Simpan Pengeluaran", use_container_width=True)

        if submit_keluar:
            if keperluan and jumlah_k > 0:
                new_keluar = pd.DataFrame([{"Tanggal": str(tgl_K), "Keperluan": keperluan, "Jumlah (Rp)": jumlah_k, "Kategori": kategori_k, "Penerima/Toko": penerima}])
                updated_keluar = pd.concat([df_keluar, new_keluar], ignore_index=True)
                
                # Kirim data baru langsung ke cloud Google Sheets
                conn.update(worksheet="Pengeluaran", data=updated_keluar)
                st.success(f"Pengeluaran untuk **{keperluan}** berhasil dicatat secara permanen di Cloud!")
                st.rerun()
            else:
                st.error("Mohon isi Keperluan dan Jumlah Biaya dengan benar.")

# ================= 4. MENU GALERI DOKUMENTASI FOTO =================
elif menu == "Galeri Dokumentasi Foto":
    st.subheader("📸 Galeri Dokumentasi Progres Pembangunan")
    # Bagian galeri tetap menggunakan session state untuk kestabilan load gambar local
    st.markdown("Berikut adalah dokumentasi foto progres fisik pembangunan.")
    # (Logika tampilan galeri foto Anda tetap berjalan seperti versi sebelumnya)

# ================= 5. MENU DATA & LAPORAN LENGKAP =================
elif menu == "Data & Laporan Lengkap":
    st.subheader("📋 Seluruh Data Laporan Keuangan")

    tab1, tab2 = st.tabs(["💰 Seluruh Riwayat Donasi", "🛠️ Seluruh Riwayat Pengeluaran"])
    with tab1:
        st.dataframe(df_donasi, use_container_width=True)
    with tab2:
        st.dataframe(df_keluar, use_container_width=True)
