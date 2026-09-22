import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Pembangunan Masjid Almirra",
    page_icon="🕌",
    layout="wide"
)

# Kustomisasi CSS Tampilan Modern
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #198754;
    }
    .header-title {
        color: #198754;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# ================= INISIALISASI DATA SECURITY =================
# Pengaturan kata sandi untuk pengurus masjid
PASSWORD_PENGURUS = "masjid123"  # Silakan ubah password sesuai kebutuhan Anda

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ================= INISIALISASI DATA DEFAULT =================
if "df_donasi" not in st.session_state:
    st.session_state.df_donasi = pd.DataFrame([
        {"Tanggal": "2026-08-27", "Nama Donatur": "Pak Mat (Kulon Kali)", "Alamat": "Nglarik Kalongan", "Kategori": "Material", "Jumlah/Nilai (Rp)": 1400000, "Keterangan": "1 Rit Pasir"},
        {"Tanggal": "2026-09-11", "Nama Donatur": "Evrilian Mahendra", "Alamat": "Nglarik 03/09 Kalongan", "Kategori": "Uang Tunai/Transfer", "Jumlah/Nilai (Rp)": 750000, "Keterangan": "Transfer BCA"},
        {"Tanggal": "2026-09-18", "Nama Donatur": "Pak Mat (Kulon Kali)", "Alamat": "Nglarik Kalongan", "Kategori": "Material", "Jumlah/Nilai (Rp)": 1400000, "Keterangan": "1 Rit Pasir"},
        {"Tanggal": "2026-09-18", "Nama Donatur": "Mbah Suparti (RT 02)", "Alamat": "Nglarik 02/09 Kalongan", "Kategori": "Uang & Material", "Jumlah/Nilai (Rp)": 1500000, "Keterangan": "Uang Tunai & 10 Sak Semen"},
        {"Tanggal": "2026-09-18", "Nama Donatur": "AHMAD BAHRUDIN", "Alamat": "Nglarik 03/09 Kalongan", "Kategori": "Uang Tunai/Transfer", "Jumlah/Nilai (Rp)": 500000, "Keterangan": "Transfer BRI"},
        {"Tanggal": "2026-09-21", "Nama Donatur": "Slamet Riyadi", "Alamat": "Nglarik Kalongan", "Kategori": "Uang Tunai/Transfer", "Jumlah/Nilai (Rp)": 20000000, "Keterangan": "Donatur Utama"},
        {"Tanggal": "2026-09-21", "Nama Donatur": "Veny Diah Gustina", "Alamat": "Nglarik Kalongan", "Kategori": "Uang Tunai/Transfer", "Jumlah/Nilai (Rp)": 300000, "Keterangan": "Uang Tunai"}
    ])

if "df_keluar" not in st.session_state:
    st.session_state.df_keluar = pd.DataFrame([
        {"Tanggal": "2026-09-02", "Keperluan": "Pembelian Semen Tahap Awal", "Kategori": "Material", "Jumlah (Rp)": 4500000, "Penerima/Toko": "TB Maju Lancar"},
        {"Tanggal": "2026-09-12", "Keperluan": "Bayar Upah Tukang Minggu ke-1", "Kategori": "Upah Kerja", "Jumlah (Rp)": 3200000, "Penerima/Toko": "Mandor Pak Budi"}
    ])

if "galeri_foto" not in st.session_state:
    st.session_state.galeri_foto = [
        {"judul": "Pekerjaan Pondasi Awal", "tanggal": "2026-08-25", "keterangan": "Penggalian dan pengecoran fondasi masjid.", "file": None},
        {"judul": "Pengiriman Material Pasir", "tanggal": "2026-08-27", "keterangan": "Donasi material dari Pak Mat (Kulon Kali).", "file": None}
    ]

# Header Modern
col_logo, col_text = st.columns([1, 6])
with col_logo:
    st.markdown("# 🕌")
with col_text:
    st.markdown("<h2 class='header-title' style='margin-bottom:0;'>Pembangunan Masjid Almirra</h2>", unsafe_allow_html=True)
    st.markdown("**Lokasi:** Lingkungan Nglarik RW 09, Kel. Kalongan, Kec. Purwodadi, Kab. Grobogan")

st.markdown("---")

# ================= SIDEBAR & SISTEM LOGIN =================
st.sidebar.markdown("### 🔒 Akses Pengurus")

if not st.session_state.authenticated:
    input_password = st.sidebar.text_input("Masukkan Password Pengurus", type="password")
    if st.sidebar.button("Log In"):
        if input_password == PASSWORD_PENGURUS:
            st.session_state.authenticated = True
            st.sidebar.success("Login Berhasil!")
            st.rerun()
        else:
            st.sidebar.error("Password Salah!")
else:
    st.sidebar.success("🔓 Mode Pengurus Aktif")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.sidebar.info("Anda telah log out.")
        st.rerun()

st.sidebar.markdown("---")

# Pengaturan Menu Berdasarkan Status Login
st.sidebar.markdown("### 📌 Menu Navigasi")
if st.session_state.authenticated:
    # Menu Lengkap untuk Pengurus
    daftar_menu = [
        "Dashboard & Ringkasan", 
        "Catat Pemasukan (Donasi)", 
        "Catat Pengeluaran Dana", 
        "Galeri Dokumentasi Foto", 
        "Data & Laporan Lengkap"
    ]
else:
    # Menu Terbatas untuk Jemaah Umum
    daftar_menu = [
        "Dashboard & Ringkasan", 
        "Galeri Dokumentasi Foto", 
        "Data & Laporan Lengkap"
    ]

menu = st.sidebar.selectbox("Pilih Halaman", daftar_menu)

# ================= 1. MENU DASHBOARD =================
if menu == "Dashboard & Ringkasan":
    st.subheader("📊 Ringkasan Keuangan Pembangunan")

    total_masuk = st.session_state.df_donasi["Jumlah/Nilai (Rp)"].sum()
    total_keluar = st.session_state.df_keluar["Jumlah (Rp)"].sum()
    sisa_saldo = total_masuk - total_keluar

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan / Donasi", f"Rp {total_masuk:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
    col3.metric("Estimasi Saldo Bersih", f"Rp {sisa_saldo:,.0f}")

    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🌟 5 Donatur Terakhir")
        st.dataframe(st.session_state.df_donasi.tail(5), use_container_width=True)
    with col_b:
        st.markdown("#### 🛠️ Pengeluaran Terakhir")
        st.dataframe(st.session_state.df_keluar.tail(5), use_container_width=True)

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

        submit_btn = st.form_submit_button("💾 Simpan Data Donatur")

        if submit_btn:
            if nama and jumlah > 0:
                new_data = {
                    "Tanggal": str(tgl),
                    "Nama Donatur": nama,
                    "Alamat": alamat,
                    "Kategori": kategori,
                    "Jumlah/Nilai (Rp)": jumlah,
                    "Keterangan": keterangan
                }
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

        submit_keluar = st.form_submit_button("💾 Simpan Pengeluaran")

        if submit_keluar:
            if keperluan and jumlah_k > 0:
                new_keluar = {
                    "Tanggal": str(tgl_K),
                    "Keperluan": keperluan,
                    "Kategori": kategori_k,
                    "Jumlah (Rp)": jumlah_k,
                    "Penerima/Toko": penerima
                }
                st.session_state.df_keluar = pd.concat([st.session_state.df_keluar, pd.DataFrame([new_keluar])], ignore_index=True)
                st.success(f"Pengeluaran untuk **{keperluan}** berhasil dicatat!")
            else:
                st.error("Mohon isi Keperluan dan Jumlah Biaya dengan benar.")

# ================= 4. MENU GALERI DOKUMENTASI FOTO =================
elif menu == "Galeri Dokumentasi Foto":
    st.subheader("📸 Galeri Dokumentasi Progres Pembangunan")
    st.markdown("Berikut adalah dokumentasi foto progres fisik pembangunan Masjid Almirra.")

    # Form Upload Foto Baru (Hanya tampil jika pengurus sudah LOGIN)
    if st.session_state.authenticated:
        with st.expander("➕ Unggah Foto Dokumentasi Baru (Khusus Pengurus)"):
            with st.form("form_foto", clear_on_submit=True):
                judul_foto = st.text_input("Judul Kegiatan / Progres")
                tgl_foto = st.date_input("Tanggal Dokumentasi", datetime.today())
                ket_foto = st.text_area("Keterangan Singkat Foto")
                file_upload = st.file_uploader("Pilih Berkas Foto (JPG / PNG)", type=["jpg", "jpeg", "png"])

                submit_foto = st.form_submit_button("Upload Foto")

                if submit_foto:
                    if judul_foto and file_upload is not None:
                        img = Image.open(file_upload)
                        new_foto = {
                            "judul": judul_foto,
                            "tanggal": str(tgl_foto),
                            "keterangan": ket_foto,
                            "file": img
                        }

