import streamlit as st
import pandas as pd

st.set_page_config(page_title="AccuCheck", layout="wide")

st.title("AccuCheck")
st.caption("AI Accounting Policy & Compliance Checker")

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader(
    "Upload file keuangan (CSV / Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    # =====================
    # READ DATA
    # =====================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()  # bersihkan spasi

    # =====================
    # DATA PREVIEW
    # =====================
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # =====================
    # IDENTIFY
    # =====================
    st.subheader("🔍 Identify – Struktur Data")

    st.write(f"Jumlah baris: **{df.shape[0]}**")
    st.write(f"Jumlah kolom: **{df.shape[1]}**")
    st.write("Kolom terdeteksi:")
    st.write(list(df.columns))

    # Auto-detect kolom
    jenis_akun_col = None
    nilai_col = None

    for col in df.columns:
        if col.lower() in ["jenis akun", "jenis_akun", "account type"]:
            jenis_akun_col = col
        if col.lower() in ["nilai", "amount", "value"]:
            nilai_col = col

    if not jenis_akun_col or not nilai_col:
        st.error("Kolom 'Jenis Akun' atau 'Nilai' tidak ditemukan.")
        st.stop()

    st.success(f"Kolom Jenis Akun: {jenis_akun_col}")
    st.success(f"Kolom Nilai: {nilai_col}")

    # =====================
    # MEASURE
    # =====================
    st.subheader("📊 Measure – Ringkasan Nilai")

    summary = df.groupby(jenis_akun_col)[nilai_col].sum().reset_index()
    st.dataframe(summary)

    # =====================
    # ANALYZE (COMPLIANCE CHECK)
    # =====================
    st.subheader("⚠️ Analyze – Policy & Compliance Check")

    flags = []

    for i, row in df.iterrows():
        akun = str(row.get("Akun", "")).lower()
        jenis = str(row[jenis_akun_col]).lower()

        if "pendapatan" in akun and "pendapatan" not in jenis:
            flags.append(f"Baris {i+1}: Akun pendapatan diklasifikasikan sebagai {row[jenis_akun_col]}")

        if "beban" in akun and "beban" not in jenis:
            flags.append(f"Baris {i+1}: Akun beban diklasifikasikan sebagai {row[jenis_akun_col]}")

    if flags:
        for f in flags:
            st.warning(f)
    else:
        st.success("Tidak ditemukan ketidaksesuaian kebijakan akuntansi.")

    # =====================
    # COMMUNICATE
    # =====================
    st.subheader("🧠 Interpretasi AI")

    if flags:
        st.write("""
Berdasarkan hasil evaluasi, terdapat beberapa potensi ketidaksesuaian
dalam klasifikasi akun yang dapat memengaruhi kualitas laporan keuangan.
Disarankan untuk meninjau kembali kebijakan pencatatan yang digunakan.
""")
    else:
        st.write("""
Berdasarkan hasil evaluasi awal, pencatatan keuangan telah
menunjukkan konsistensi dengan kebijakan akuntansi yang digunakan.
""")

    # =====================
    # TAKE ACTION
    # =====================
    st.subheader("✅ Rekomendasi")

    st.write("""
- Lakukan peninjauan ulang pada akun yang terindikasi tidak sesuai
- Pastikan klasifikasi akun mengikuti kebijakan akuntansi
- Gunakan hasil evaluasi ini sebagai review awal sebelum laporan digunakan
""")
