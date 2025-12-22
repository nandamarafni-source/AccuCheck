import streamlit as st
import pandas as pd

st.set_page_config(page_title="AccuCheck", layout="wide")
st.title("AccuCheck – AI Accounting Policy & Compliance Checker")

uploaded_file = st.file_uploader(
    "Upload file keuangan (CSV / Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    # =====================
    # READ FILE
    # =====================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # =====================
    # IDENTIFY
    # =====================
    st.subheader("🔍 Identify – Struktur Data")

    columns_lower = {c.lower(): c for c in df.columns}

    def find_column(possible_names):
        for name in possible_names:
            if name in columns_lower:
                return columns_lower[name]
        return None

    akun_col = find_column(["akun", "account"])
    jenis_col = find_column(["jenis akun", "jenis_akun", "account type", "type"])
    nilai_col = find_column(["nilai", "amount", "value", "nominal"])

    st.write("Kolom terdeteksi:")
    st.write({
        "Akun": akun_col,
        "Jenis Akun": jenis_col,
        "Nilai": nilai_col
    })

    if not nilai_col:
        st.error("Kolom nilai/amount tidak ditemukan. Measure tidak dapat dijalankan.")
        st.stop()

    # =====================
    # MEASURE
    # =====================
    st.subheader("📊 Measure – Ringkasan Data")

    if jenis_col:
        summary = df.groupby(jenis_col)[nilai_col].sum().reset_index()
        st.write("Ringkasan nilai per jenis akun:")
        st.dataframe(summary)
    else:
        st.warning("Kolom jenis akun tidak ditemukan. Measure dilakukan secara total.")
        st.write(f"Total nilai: {df[nilai_col].sum():,.0f}")

    # =====================
    # ANALYZE (COMPLIANCE)
    # =====================
    st.subheader("⚠️ Analyze – Policy & Compliance Check")

    flags = []

    if akun_col and jenis_col:
        for _, row in df.iterrows():
            akun = str(row[akun_col]).lower()
            jenis = str(row[jenis_col]).lower()

            if "pendapatan" in akun and jenis != "pendapatan":
                flags.append("Akun pendapatan dicatat bukan sebagai pendapatan")

            if "beban" in akun and jenis != "beban":
                flags.append("Akun beban dicatat bukan sebagai beban")

    if flags:
        st.error("Ditemukan potensi ketidaksesuaian kebijakan akuntansi:")
        for f in set(flags):
            st.write(f"- {f}")
    else:
        st.success("Tidak ditemukan ketidaksesuaian kebijakan yang signifikan.")

    # =====================
    # COMMUNICATE
    # =====================
    st.subheader("🧾 Interpretasi AI")

    st.write("""
AccuCheck melakukan evaluasi awal terhadap struktur dan konsistensi
pencatatan keuangan berdasarkan kebijakan akuntansi dasar.
Hasil ini bersifat pendukung dan tidak menggantikan penilaian profesional.
""")

    # =====================
    # TAKE ACTION
    # =====================
    st.subheader("✅ Rekomendasi")

    st.write("""
1. Lakukan peninjauan ulang terhadap klasifikasi akun.
2. Pastikan konsistensi jenis akun dengan kebijakan akuntansi.
3. Gunakan hasil evaluasi ini sebagai dasar review lanjutan.
""")
