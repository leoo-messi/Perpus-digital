import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Manajemen Data", page_icon="📝", layout="wide")

# Cek Status Login Admin
if not st.session_state.get("logged_in", False):
  st.error("⚠️ Akses Ditolak! Silakan Login terlebih dahulu melalui halaman utama.")
  st.stop()

st.title("📝 Panel Manajemen Data Perpustakaan (Admin)")

tab1, tab2 = st.tabs(["Kelola Buku", "Kelola Peminjaman"])

with tab1:
  st.subheader("➕ Tambah Buku Baru")
  with st.form("form_tambah_buku"):
    judul = st.text_input("Judul Buku")
    penulis = st.text_input("Penulis")
    kategori = st.selectbox(
        "Kategori", ["Fiksi", "Sains", "Teknologi", "Sejarah", "Ekonomi"]
    )
    stok = st.number_input("Jumlah Stok", min_value=1, value=5)
    tahun = st.number_input("Tahun Terbit", min_value=1900, max_value=2026, value=2023)
    submitted = st.form_submit_button("Simpan Buku")

    if submitted:
      conn = sqlite3.connect("perpustakaan.db")
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO buku (judul, penulis, kategori, stok, tahun) VALUES"
          " (?, ?, ?, ?, ?)",
          (judul, penulis, kategori, stok, tahun),
      )
      conn.commit()
      conn.close()
      st.success(f"Buku '{judul}' berhasil ditambahkan!")
      st.rerun()

  st.subheader("📋 Daftar & Hapus Buku")
  conn = sqlite3.connect("perpustakaan.db")
  df_buku = pd.read_sql("SELECT * FROM buku", conn)
  conn.close()
  st.dataframe(df_buku, use_container_width=True)

  if not df_buku.empty:
    id_hapus = st.selectbox("Pilih ID Buku yang ingin dihapus", df_buku["id"])
    if st.button("Hapus Buku"):
      conn = sqlite3.connect("perpustakaan.db")
      cursor = conn.cursor()
      cursor.execute("DELETE FROM buku WHERE id = ?", (id_hapus,))
      conn.commit()
      conn.close()
      st.success("Buku berhasil dihapus!")
      st.rerun()

with tab2:
  st.subheader("📌 Catat Peminjaman Buku")
  with st.form("form_pinjam"):
    nama = st.text_input("Nama Peminjam")
    buku_pinjam = st.text_input("Judul Buku yang Dipinjam")
    tgl = st.date_input("Tanggal Pinjam")
    status = st.selectbox("Status", ["Dipinjam", "Dikembalikan"])
    submit_pinjam = st.form_submit_button("Simpan Data Peminjaman")

    if submit_pinjam:
      conn = sqlite3.connect("perpustakaan.db")
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO peminjaman (nama_peminjam, judul_buku, tanggal_pinjam,"
          " status) VALUES (?, ?, ?, ?)",
          (nama, buku_pinjam, str(tgl), status),
      )
      conn.commit()
      conn.close()
      st.success("Data peminjaman berhasil disimpan!")
      st.rerun()

  st.subheader("📋 Riwayat Peminjaman")
  conn = sqlite3.connect("perpustakaan.db")
  df_pinjam = pd.read_sql("SELECT * FROM peminjaman", conn)
  conn.close()
  st.dataframe(df_pinjam, use_container_width=True)
