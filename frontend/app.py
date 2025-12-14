import streamlit as st
import requests
import os
from PIL import Image

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Prediksi Harga Rumah Jaksel",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:5000")

# -----------------------------------------------------------------------------
# API HELPERS
# -----------------------------------------------------------------------------
def get_prediction(data):
    try:
        response = requests.post(f"{API_URL}/predict", json=data)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"Status {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_metrics():
    try:
        response = requests.get(f"{API_URL}/metrics", timeout=2)
        if response.status_code == 200:
             data = response.json()
             if data.get("status") == "success":
                 return data.get("data")
        return None
    except:
        return None

# -----------------------------------------------------------------------------
# STYLE & HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏠 Prediksi Harga Rumah Jakarta Selatan</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Estimasi harga rumah impian Anda berdasarkan data pasar terbaru (Rumah123).</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: MODEL METRICS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/25/25694.png", width=50) 
    st.header("📊 Model Performance")
    
    metrics = get_metrics()
    
    if metrics:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("R2 Score", f"{metrics['r2']:.2f}")
        with col_m2:
            st.metric("MAE (Error)", f"{int(metrics['mae']/1e6)} Jt")
        
        st.markdown(f"**Last Updated:**  \n{metrics['last_updated']}")
        st.success("Model Status: **Active**")
    else:
        st.warning("Model metrics unavailable (API offline?)")
    
    st.markdown("---")
    st.caption("Dikembangkan dengan otomatisasi CI/CD.")

# -----------------------------------------------------------------------------
# MAIN FORM
# -----------------------------------------------------------------------------
col_input, col_result = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("### 📝 Masukkan Spesifikasi Rumah")
    with st.form(key='house_form'):
        c1, c2 = st.columns(2)
        with c1:
            lb = st.number_input("Luas Bangunan (m²)", 30, 2000, 100, help="Luas area bangunan rumah")
        with c2:
            lt = st.number_input("Luas Tanah (m²)", 20, 2000, 120, help="Luas tanah sertifikat")
            
        c3, c4, c5 = st.columns(3)
        with c3:
            kt = st.number_input("Kamar Tidur", 1, 20, 3)
        with c4:
            km = st.number_input("Kamar Mandi", 1, 15, 2)
        with c5:
            grs = st.number_input("Garasi/Carport", 0, 10, 1)
            
        submit = st.form_submit_button("🚀 Hitung Estimasi Harga", use_container_width=True)

# -----------------------------------------------------------------------------
# RESULT DISPLAY
# -----------------------------------------------------------------------------
with col_result:
    if submit:
        st.markdown("### 💰 Hasil Estimasi")
        with st.spinner("Mengkalkulasi harga pasar..."):
            payload = {"LB": lb, "LT": lt, "KT": kt, "KM": km, "GRS": grs}
            result = get_prediction(payload)
            
            if result.get("status") == "success":
                price = result['prediction']
                
                # Big Price Display
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1E88E5;">
                    <h4 style="margin:0; color: #1565C0;">Estimasi Harga Pasar</h4>
                    <h1 style="color: #0D47A1; margin: 10px 0;">Rp {price:,.0f}</h1>
                    <p style="margin:0; color: #555;">*Harga ini adalah prediksi statistik berdasarkan {lb}m² LB dan {lt}m² LT di Jakarta Selatan.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detail Recap
                st.write("")
                st.info(f"Summary: Rumah dengan {kt} KT, {km} KM, dan {grs} Garasi.")
                
            else:
                st.error(f"Gagal memprediksi: {result.get('message')}")
    else:
        # Placeholder State
        st.info("👈 Isi formulir di kiri dan tekan tombol untuk melihat estimasi harga.")

