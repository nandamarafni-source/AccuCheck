import streamlit as st
import pandas as pd

st.set_page_config(page_title="AccuCheck", layout="wide")

st.title("AccuCheck")
st.caption("AI Accounting Policy & Compliance Checker")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload file keuangan (CSV / Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    # =========================
    # READ DATA
    # =========================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # =========================
    # DATA PREVIEW
    # =========================
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # =========================
    # IDENTIFY
    # =========================
    st.subheader("🔍 Identify – Struktur & Akun")

    total_rows = df.shape[0]
    total_cols = df.shape[1]

    st.write(f"Jumlah baris data: **{total_rows}**")
    st.write(f"Jumlah kolom data: **{total_cols}**")
    st.write("Nama kolom:")
    st.write(list(df.columns))

    if "Akun" in df.columns:
        akun_unik = df["Akun"].dropna().unique()
        st.write(f"Jumlah akun terdeteksi: **{len(akun_unik)}**")
        st.write(akun_unik)

    if "Jenis Akun" in df.columns:
        jenis_akun = df["Jenis Akun"].dropna().unique()
        st.write("Jenis akun terdeteksi:")
        st.write(jenis_akun)

    st.success("Tahap Identify selesai")

    # =========================
    # MEASURE
    # =========================
    st.subheader("📊 Measure – Ringkasan Nilai")

    if "Jenis Akun" in df.columns and "Nilai" in df.columns:
        summary = (
            df.groupby("Jenis Akun")["Nilai"]
            .sum()
            .reset_index()
        )

        st.write("Total nilai per jenis akun:")
        st.dataframe(summary)

    else:
        st.warning("Kolom 'Jenis Akun' atau 'Nilai' tidak ditemukan")

    # =========================
    # ANALYZE (POLICY & COMPLIANCE)
    # =========================
    st.subheader("⚠️ Analyze – Policy & Compliance Check")

    flags = []

    if {"Akun", "Jenis Akun"}.issubset(df.columns):
        for i, row in df.iterrows():
            akun = str(row["Akun"]).lower()
            jenis = str(row["Jenis Akun"]).lower()

            if "pendapatan" in akun and jenis != "pendapatan":
                flags.append(
                    f"Baris {i+1}: Akun pendapatan dicatat sebagai {row['Jenis Akun']}"
                )

            if "beban" in akun and jenis != "beban":
                flags.append(
                    f"Baris {i+1}: Akun beban dicatat sebagai {row['Jenis Akun']}"
                )

            if "kas" in akun and jenis not in ["aset", "asset"]:
                flags.append(
                    f"Baris {i+1}: Akun kas seharusnya termasuk Aset"
                )

    if flags:
        st.error("Ditemukan potensi ketidaksesuaian kebijakan akuntansi:")
        for f in flags:
            st.write("•", f)
    else:
        st.success("Tidak ditemukan pelanggaran kebijakan pencatatan yang signifikan")

    # =========================
    # COMMUNICATE
    # =========================
    st.subheader("🗣️ Communicate – Ringkasan Evaluasi")

    if flags:
        st.write(
            "Berdasarkan hasil evaluasi, terdapat beberapa pe
