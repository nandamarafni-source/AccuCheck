import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import os
from dotenv import load_dotenv

# =========================
# PAGE SETUP
# =========================
st.set_page_config(
    page_title="AccuCheck",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AccuCheck")
st.caption("AI Accounting Policy & Compliance Checker | Rule-based + AI Commentary")

# =========================
# LOAD API KEY (OPTIONAL)
# =========================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# =========================
# AI COMMENTARY FUNCTION
# =========================
def generate_ai_commentary(summary_df: pd.DataFrame) -> str:
    """
    AI commentary bersifat konseptual & edukatif.
    Tidak melakukan prediksi atau perhitungan lanjutan.
    """
    if not client:
        return "⚠️ AI Commentary tidak aktif (API Key belum diatur)."

    text_data = summary_df.to_string(index=False)

    prompt = f"""
    Anda adalah AI Accounting Reviewer.

    Berikut ringkasan data keuangan:
    {text_data}

    Tugas Anda:
    1. Jelaskan temuan utama secara konseptual
    2. Identifikasi potensi ketidakkonsistenan pencatatan
    3. Berikan rekomendasi perbaikan bersifat edukatif
    4. Gunakan bahasa non-teknis dan mudah dipahami
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error AI Commentary: {e}"

# =========================
# DATA UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📂 Upload file Excel / CSV",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # =========================
    # DATA PREVIEW
    # =========================
    st.subheader("📜 Data Preview")
    st.dataframe(df.head())

    # =========================
    # BASIC VALIDATION
    # =========================
    if df.shape[1] < 2:
        st.warning("⚠️ Data minimal harus memiliki lebih dari satu kolom.")
        st.stop()

    # =========================
    # IDENTIFY & MEASURE (AGGREGATION)
    # =========================
    st.subheader("📊 Ringkasan Data (Identify & Measure)")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    category_cols = df.select_dtypes(exclude="number").columns.tolist()

    if not numeric_cols or not category_cols:
        st.warning("⚠️ Data harus memiliki kolom kategori dan numerik.")
        st.stop()

    cat_col = category_cols[0]
