import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Analitik Perpustakaan", page_icon="📊", layout="wide")

st.title("📊 Dashboard Analitik & Statistik Perpustakaan")

conn = sqlite3.connect("perpustakaan.db")
df_buku = pd.read_sql("SELECT * FROM buku", conn)
conn.close()

if df_buku.empty:
  st.warning("Belum ada data buku untuk dianalisis.")
else:
  st.subheader("📈 Grafik Distribusi Kategori Buku")
  fig_kat = px.pie(
      df_buku,
      names="kategori",
      values="stok",
      title="Perbandingan Jumlah Stok Berdasarkan Kategori",
      hole=0.4,
  )
  st.plotly_chart(fig_kat, use_container_width=True)

  st.subheader("📊 Grafik Stok Buku Berdasarkan Tahun Terbit")
  fig_tahun = px.bar(
      df_buku,
      x="tahun",
      y="stok",
      color="kategori",
      title="Stok Buku per Tahun",
      labels={"tahun": "Tahun Terbit", "stok": "Jumlah Stok"},
  )
  st.plotly_chart(fig_tahun, use_container_width=True)
