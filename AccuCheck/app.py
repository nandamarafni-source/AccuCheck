import streamlit as st
import pandas as pd

st.set_page_config(page_title="AccuCheck", layout="wide")

st.title("AccuCheck")
st.caption("AI Accounting Policy & Compliance Checker")

# =====================
# UPLOAD DATA
# =====================
uploaded_file = st.file_uploader(
    "Upload file keuangan (CSV atau Excel)",
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

    akun_list = []
    jenis_akun_list = []

    if "Akun" in df.columns:
        akun_list = df["Akun"].dropna().unique()
        st.write(f"Jumlah akun unik: **{len(akun_list)}**")
        st.write(akun_list)

    if "Jenis Akun" in df.columns:
        jenis_akun_list = df["Jenis Akun"].dropna().unique()
        st.write("Jenis akun terdeteksi:")
        st.write(jenis_akun_list)

    st.success("Tahap Identify selesai")

    # =====================
    # MEASURE
    # =====================
    st.subheader("📊 Measure – Ringkasan Nilai")

    if "Jenis Akun" in df.columns and "Nilai" in df.columns:
        summary_measure = (
            df.groupby("Jenis Akun")["Nilai"]
            .sum()
            .reset_index()
        )
        st.dataframe(summary_measure)
    else:
        st.warning("Kolom 'Jenis Akun' atau 'Nilai' tidak ditemukan.")

    # =====================
    # ANALYZE (COMPLIANCE CHECK)
    # =====================
    st.subheader("⚠️ Analyze – Policy & Compliance Check")

    findings = []

    if "Akun" in df.columns and "Jenis Akun" in df.columns:
        for i, row in df.iterrows():
            akun = str(row["Akun"])
            jenis = str(row["Jenis Akun"])

            if "Pendapatan" in akun and jenis != "Pendapatan":
                findings.append(
                    f"Akun '{akun}' dicatat sebagai '{jenis}' (potensi salah klasifikasi)."
                )

            if "Beban" in akun and jenis != "Beban":
                findings.append(
                    f"Akun '{akun}' dicatat sebagai '{jenis}' (perlu ditinjau kembali)."
                )

    if findings:
        for f in findings:
            st.error(f)
    else:
        st.success("Tidak ditemukan ketidaksesuaian kebijakan yang signifikan.")

    # =====================
    # COMMUNICATE
    # =====================
    st.subheader("🧠 Interpretasi AI")

    interpretation = (
        "Berdasarkan hasil evaluasi, sistem mengidentifikasi struktur data "
        "dan melakukan pemeriksaan awal terhadap konsistensi pencatatan akun. "
        "Temuan yang muncul bersifat indikatif dan ditujukan sebagai bahan "
        "review awal sebelum dilakukan evaluasi lanjutan."
    )

    st.write(interpretation)

    # =====================
    # TAKE ACTION
    # =====================
    st.subheader("✅ Rekomendasi Tindak Lanjut")

    st.write(
        "- Periksa kembali klasifikasi akun yang tidak sesuai\n"
        "- Sesuaikan pencatatan dengan kebijakan akuntansi yang berlaku\n"
        "- Lakukan review manual sebelum laporan digunakan"
    )
