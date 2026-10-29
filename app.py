import sqlite3
import pandas as pd
import streamlit as st

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Perpustakaan Digital Josjis",
    page_icon="📚",
    layout="wide",
)


# Inisialisasi Database SQLite
def init_db():
  conn = sqlite3.connect("perpustakaan.db")
  cursor = conn.cursor()
  # Tabel Buku
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            kategori TEXT NOT NULL,
            stok INTEGER NOT NULL,
            tahun INTEGER NOT NULL
        )
    """)
  # Tabel Riwayat Peminjaman
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_peminjam TEXT NOT NULL,
            judul_buku TEXT NOT NULL,
            tanggal_pinjam TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()


init_db()

# Session State untuk Login Admin
if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False

# Sidebar Navigasi & Login
st.sidebar.title("🔐 Panel Admin & Navigasi")
menu = st.sidebar.selectbox(
    "Pilih Menu", ["Beranda (Home)", "Katalog Buku", "Login Admin"]
)

if menu == "Beranda (Home)":
  st.title("📚 Selamat Datang di Perpustakaan Digital")
  st.markdown(
      "Aplikasi web dashboard perpustakaan interaktif berbasis Python, Streamlit,"
      " dan SQLite."
  )
  st.info(
      "Gunakan menu di sidebar untuk melihat katalog buku atau login sebagai"
      " admin guna mengelola data."
  )

  # Ringkasan Data Cepat di Beranda
  conn = sqlite3.connect("perpustakaan.db")
  df_buku = pd.read_sql("SELECT * FROM buku", conn)
  df_pinjam = pd.read_sql("SELECT * FROM peminjaman", conn)
  conn.close()

  col1, col2, col3 = st.columns(3)
  col1.metric("Total Judul Buku", len(df_buku))
  col2.metric("Total Kategori", df_buku["kategori"].nunique() if not df_buku.empty else 0)
  col3.metric("Buku Sedang Dipinjam", len(df_pinjam[df_pinjam["status"] == "Dipinjam"]))

elif menu == "Katalog Buku":
  st.title("📖 Katalog Buku Perpustakaan")
  conn = sqlite3.connect("perpustakaan.db")
  df_buku = pd.read_sql("SELECT * FROM buku", conn)
  conn.close()

  if df_buku.empty:
    st.warning(
        "Belum ada data buku. Silakan minta Admin memasukkan data melalui menu"
        " Manajemen Data."
    )
  else:
    search = st.text_input("🔍 Cari judul buku atau penulis...")
    if search:
      df_buku = df_buku[
          df_buku["judul"].str.contains(search, case=False, na=False)
          | df_buku["penulis"].str.contains(search, case=False, na=False)
      ]
    st.dataframe(df_buku, use_container_width=True)

elif menu == "Login Admin":
  st.title("🔑 Login Administrator")
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")

  if st.button("Login"):
    if username == "admin" and password == "josjis123":
      st.session_state["logged_in"] = True
      st.success("Login Berhasil! Silakan buka menu Analitik atau Manajemen Data.")
    else:
      st.error("Username atau Password salah!")
