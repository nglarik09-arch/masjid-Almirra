import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Sistem Keuangan Masjid Almirra",
    page_icon="🕌",
    layout="wide"
)

# Inisialisasi Data Default
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
        {"Tanggal": "2026-09-02", "Keperluan": "Pembelian Semen Tahap Awal", "Kategori": "Material", "Jumlah (Rp)": 0, "Penerima/Toko": "TB Maju Lancar"},
        {"Tanggal": "2026-09-12", "Keperluan": "Bayar Upah Tukang Minggu ke-1", "Kategori": "Upah Kerja", "Jumlah (Rp)": 0, "Penerima/Toko": "Mandor Pak Budi"}
    ])

# Header Aplikasi
st.title("🕌 Sistem Informasi Pembangunan Masjid Almirra")
st.markdown("**Lokasi:** Lingkungan Nglarik RW 09, Kelurahan Kalongan, Kecamatan Purwodadi, Kabupaten Grobogan")
st.markdown("---")

# Sidebar Navigasi Menu
menu = st.sidebar.selectbox("Pilih Menu", ["Dashboard & Ringkasan", "Catat Pemasukan (Donasi)", "Catat Pengeluaran Dana", "Data & Laporan Lengkap"])

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
        st.markdown("#### 5 Donatur Terakhir")
        st.dataframe(st.session_state.df_donasi.tail(5), use_container_width=True)
    with col_b:
        st.markdown("#### Pengeluaran Terakhir")
        st.dataframe(st.session_state.df_keluar.tail(5), use_container_width=True)

# ================= 2. MENU CATAT PEMASUKAN =================
elif menu == "Catat Pemasukan (Donasi)":
    st.subheader("➕ Tambah Data Donatur / Pemasukan Dana")

    with st.form("form_donasi"):
        tgl = st.date_input("Tanggal Donasi", datetime.today())
        nama = st.text_input("Nama Donatur")
        alamat = st.text_input("Alamat (Contoh: Nglarik RT 02/09 Kalongan)")
        kategori = st.selectbox("Bentuk Donasi", ["Uang Tunai/Transfer", "Material", "Uang & Material"])
        jumlah = st.number_input("Nominal / Estimasi Nilai (Rp)", min_value=0, step=50000)
        keterangan = st.text_input("Keterangan Tambahan (Contoh: 1 Rit Pasir / Transfer BCA)")

        submit_btn = st.form_submit_button("Simpan Data Donatur")

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

    with st.form("form_keluar"):
        tgl_K = st.date_input("Tanggal Pengeluaran", datetime.today())
        keperluan = st.text_input("Keperluan / Nama Barang")
        kategori_k = st.selectbox("Kategori Pengeluaran", ["Material", "Upah Kerja", "Konsumsi", "Lain-lain"])
        jumlah_k = st.number_input("Jumlah Biaya (Rp)", min_value=0, step=50000)
        penerima = st.text_input("Dibayarkan Kepada / Toko")

        submit_keluar = st.form_submit_button("Simpan Pengeluaran")

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

# ================= 4. MENU LAPORAN LENGKAP =================
elif menu == "Data & Laporan Lengkap":
    st.subheader("📋 Laporan Keuangan & Daftar Donatur Masjid Almirra")

    tab1, tab2 = st.tabs(["Daftar Pemasukan (Donatur)", "Daftar Pengeluaran"])

    with tab1:
        st.markdown("### Rekapitulasi Donatur")
        st.dataframe(st.session_state.df_donasi, use_container_width=True)
        
        csv_donasi = st.session_state.df_donasi.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Unduh Laporan Donatur (CSV)", csv_donasi, "laporan_donatur_almirra.csv", "text/csv")

    with tab2:
        st.markdown("### Rekapitulasi Pengeluaran")
        st.dataframe(st.session_state.df_keluar, use_container_width=True)

        csv_keluar = st.session_state.df_keluar.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Unduh Laporan Pengeluaran (CSV)", csv_keluar, "laporan_pengeluaran_almirra.csv", "text/csv")
