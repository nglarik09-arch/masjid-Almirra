import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import plotly.express as px  # Library tambahan untuk layout grafik interaktif

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Pembangunan Masjid Almirra",
    page_icon="🕌",
    layout="wide"
)

# Kustomisasi CSS Tampilan Modern & Elegan khas Islami
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f8;
    }
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
    .header-title {
        color: #198754;
        font-weight: 800;
        font-size: 28px;
    }
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# ================= INISIALISASI DATA SECURITY =================
PASSWORD_PENGURUS = "masjidalmirra123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ================= INISIALISASI DATA DEFAULT =================
if "df_donasi" not in st.session_state:
    st.session_state.df_donasi = pd.DataFrame([
        {"Tanggal": "2026-08-27", "Nama Donatur": "Pak Mat (Kulon Kali)", "Jumlah/Nilai (Rp)": 1400000, "Kategori": "Material", "Alamat": "Nglarik Kalongan", "Keterangan": "1 Rit Pasir"},
        {"Tanggal": "2026-09-11", "Nama Donatur": "Evrilian Mahendra", "Jumlah/Nilai (Rp)": 750000, "Kategori": "Uang Tunai/Transfer", "Alamat": "Nglarik 03/09 Kalongan", "Keterangan": "Transfer BCA"},
        {"Tanggal": "2026-09-18", "Nama Donatur": "Pak Mat (Kulon Kali)", "Jumlah/Nilai (Rp)": 1400000, "Kategori": "Material", "Alamat": "Nglarik Kalongan", "Keterangan": "1 Rit Pasir"},
        {"Tanggal": "2026-09-18", "Nama Donatur": "Mbah Suparti (RT 02)", "Jumlah/Nilai (Rp)": 1500000, "Kategori": "Uang & Material", "Alamat": "Nglarik 02/09 Kalongan", "Keterangan": "Uang Tunai & 10 Sak Semen"},
        {"Tanggal": "2026-09-18", "Nama Donatur": "AHMAD BAHRUDIN", "Jumlah/Nilai (Rp)": 500000, "Kategori": "Uang Tunai/Transfer", "Alamat": "Nglarik 03/09 Kalongan", "Keterangan": "Transfer BRI"},
        {"Tanggal": "2026-09-21", "Nama Donatur": "Slamet Riyadi", "Jumlah/Nilai (Rp)": 20000000, "Kategori": "Uang Tunai/Transfer", "Alamat": "Nglarik Kalongan", "Keterangan": "Donatur Utama"},
        {"Tanggal": "2026-09-21", "Nama Donatur": "Veny Diah Gustina", "Jumlah/Nilai (Rp)": 300000, "Kategori": "Uang Tunai/Transfer", "Alamat": "Nglarik Kalongan", "Keterangan": "Uang Tunai"}
    ])

if "df_keluar" not in st.session_state:
    st.session_state.df_keluar = pd.DataFrame([
        {"Tanggal": "2026-09-02", "Keperluan": "Pembelian Semen Tahap Awal", "Jumlah (Rp)": 4500000, "Kategori": "Material", "Penerima/Toko": "TB Maju Lancar"},
        {"Tanggal": "2026-09-12", "Keperluan": "Bayar Upah Tukang Minggu ke-1", "Jumlah (Rp)": 3200000, "Kategori": "Upah Kerja", "Penerima/Toko": "Mandor Pak Budi"}
    ])

if "galeri_foto" not in st.session_state:
    st.session_state.galeri_foto = [
        {"judul": "Pekerjaan Pondasi Awal", "tanggal": "2026-08-25", "keterangan": "Penggalian dan pengecoran fondasi masjid.", "file": None},
        {"judul": "Pengiriman Material Pasir", "tanggal": "2026-08-27", "keterangan": "Donasi material dari Pak Mat (Kulon Kali).", "file": None}
    ]

# Layout Header Baru Berbentuk Kotak Informasi Kompak
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
            st.sidebar.success("Login Berhasil!")
            st.rerun()
        else:
            st.sidebar.error("Password Salah!")
else:
    st.sidebar.success("🔓 Mode Pengurus Aktif")
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.authenticated = False
        st.sidebar.info("Anda telah log out.")
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

    total_masuk = st.session_state.df_donasi["Jumlah/Nilai (Rp)"].sum()
    total_keluar = st.session_state.df_keluar["Jumlah (Rp)"].sum()
    sisa_saldo = total_masuk - total_keluar

    # Layout Ringkasan 3 Angka Utama
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Dana Masuk", f"Rp {total_masuk:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
    col3.metric("Estimasi Saldo Kas", f"Rp {sisa_saldo:,.0f}")

    st.markdown("---")
    
    # Layout Layout Baru: Kolom Kiri Grafik, Kolom Kanan Penjelasan Ringkas
    col_chart1, col_chart2 = st.columns([1, 1])
    with col_chart1:
        st.markdown("#### 📈 Proporsi Bentuk Donasi")
        fig_donasi = px.pie(st.session_state.df_donasi, values='Jumlah/Nilai (Rp)', names='Kategori', color_discrete_sequence=px.colors.sequential.Darkmint)
        fig_donasi.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig_donasi, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### 📉 Alokasi Pengeluaran")
        fig_keluar = px.pie(st.session_state.df_keluar, values='Jumlah (Rp)', names='Kategori', color_discrete_sequence=px.colors.sequential.Oranges_r)
        fig_keluar.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig_keluar, use_container_width=True)

    st.markdown("---")
    
    # Layout Tabel Semua Riwayat (Terbaru Di Atas)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🌟 Semua Data Donatur")
        st.dataframe(st.session_state.df_donasi.iloc[::-1], use_container_width=True, height=350)
    with col_b:
        st.markdown("#### 🛠️ Semua Data Pengeluaran")
        st.dataframe(st.session_state.df_keluar.iloc[::-1], use_container_width=True, height=350)

# ================= 2. MENU CATAT PEMASUKAN =================
elif menu == "Catat Pemasukan (Donasi)":
    st.subheader("➕ Tambah Data Donatur / Pemasukan Dana")

    with st.form("form_donasi", clear_on_submit=True):
        tgl = st.date_input("Tanggal Donasi", datetime.today())
        nama = st.text_input("Nama Donatur")
        alamat = st.text_input("Alamat (Contoh: Nglarik RT 02/09 Kalongan)")
        kategori = st.selectbox("Bentuk Donasi", ["Uang Tunai/Transfer", "Material", "Uang & Material"])
        jumlah = st.number_input("Nominal / Estimasi Nilai (Rp)", min_value=0, step=50000)
        keterangan = st.text_input("Keterangan Tambahan (Contoh: 1 Rit Pasir / Transfer BCA)")

        submit_btn = st.form_submit_button("💾 Simpan Data Donatur", use_container_width=True)

        if submit_btn:
            if nama and jumlah > 0:
                new_data = {"Tanggal": str(tgl), "Nama Donatur": nama, "Jumlah/Nilai (Rp)": jumlah, "Kategori": kategori, "Alamat": alamat, "Keterangan": keterangan}
                st.session_state.df_donasi = pd.concat([st.session_state.df_donasi, pd.DataFrame([new_data])], ignore_index=True)
                st.success(f"Donasi dari **{nama}** berhasil disimpan!")
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
                new_keluar = {"Tanggal": str(tgl_K), "Keperluan": keperluan, "Jumlah (Rp)": jumlah_k, "Kategori": kategori_k, "Penerima/Toko": penerima}
                st.session_state.df_keluar = pd.concat([st.session_state.df_keluar, pd.DataFrame([new_keluar])], ignore_index=True)
                st.success(f"Pengeluaran untuk **{keperluan}** berhasil dicatat!")
            else:
                st.error("Mohon isi Keperluan dan Jumlah Biaya dengan benar.")

# ================= 4. MENU GALERI DOKUMENTASI FOTO =================
elif menu == "Galeri Dokumentasi Foto":
    st.subheader("📸 Galeri Dokumentasi Progres Pembangunan")
    
