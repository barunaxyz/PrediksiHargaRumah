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
# SESSION STATE
# -----------------------------------------------------------------------------
if 'role' not in st.session_state:
    st.session_state.role = None

def login_user():
    st.session_state.role = 'user'
    st.rerun()

def login_admin(username, password):
    if username == "admin" and password == "admin123":
        st.session_state.role = 'admin'
        st.rerun()
    else:
        st.error("Username atau Password salah!")

def logout():
    st.session_state.role = None
    st.rerun()

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
# PAGES
# -----------------------------------------------------------------------------
def show_login_page():
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏠 House Price Prediction System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Silakan pilih akses login Anda</p>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["👤 User (Public)", "🔒 Admin (Metrik)"])
        
        with tab1:
            st.info("Akses fitur prediksi harga rumah secara gratis.")
            if st.button("🚀 Masuk sebagai User", use_container_width=True):
                login_user()
                
        with tab2:
            st.warning("Area terbatas khusus Administrator.")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("🔐 Login Admin", use_container_width=True):
                login_admin(username, password)

def show_user_page():
    # Header
    st.markdown('<div class="main-header">🏠 Prediksi Harga Rumah Jakarta Selatan</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Estimasi harga rumah impian Anda berdasarkan data pasar terbaru.</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/25/25694.png", width=50)
        st.write(f"Logged in as: **User**")
        if st.button("Logout", type="secondary"):
            logout()
    
    # Main Form
    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 📝 Masukkan Spesifikasi Rumah")
        with st.form(key='house_form'):
            c1, c2 = st.columns(2)
            with c1:
                lb = st.number_input("Luas Bangunan (m²)", 30, 2000, 100)
            with c2:
                lt = st.number_input("Luas Tanah (m²)", 20, 2000, 120)
                
            c3, c4, c5 = st.columns(3)
            with c3:
                kt = st.number_input("Kamar Tidur", 1, 20, 3)
            with c4:
                km = st.number_input("Kamar Mandi", 1, 15, 2)
            with c5:
                grs = st.number_input("Garasi/Carport", 0, 10, 1)
                
            submit = st.form_submit_button("🚀 Hitung Estimasi Harga", use_container_width=True)

    with col_result:
        if submit:
            st.markdown("### 💰 Hasil Estimasi")
            with st.spinner("Mengkalkulasi harga pasar..."):
                payload = {"LB": lb, "LT": lt, "KT": kt, "KM": km, "GRS": grs}
                result = get_prediction(payload)
                
                if result.get("status") == "success":
                    price = result['prediction']
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1E88E5;">
                        <h4 style="margin:0; color: #1565C0;">Estimasi Harga Pasar</h4>
                        <h1 style="color: #0D47A1; margin: 10px 0;">Rp {price:,.0f}</h1>
                        <p style="margin:0; color: #555;">*Prediksi berdasarkan spesifikasi fisik rumah.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Gagal memprediksi: {result.get('message')}")
        else:
             st.info("👈 Isi formulir di kiri untuk melihat estimasi.")

def show_admin_page():
    st.markdown('<div class="main-header">📊 Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Monitoring Performa Model Regresi.</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/97/97895.png", width=50)
        st.write(f"Logged in as: **Admin**")
        if st.button("Logout", type="secondary"):
            logout()
            
    metrics = get_metrics()
    
    if metrics:
        col1, col2, col3 = st.columns(3)
        with col1:
             st.metric("Model Status", "Active", "Online")
        with col2:
             st.metric("R2 Score (Akurasi)", f"{metrics['r2']:.4f}")
        with col3:
             st.metric("MAPE (Error Rate)", f"{metrics['mape']:.2%}", delta_color="inverse")
             
        st.markdown("---")
        st.markdown(f"### 🕒 Last Updated: {metrics['last_updated']}")
        
        st.markdown("### 📈 Detail Insights")
        st.info("Saat ini model menggunakan algoritma **Linear Regression**. Error rate 28% menunjukkan perlunya penambahan fitur lokasi untuk meningkatkan akurasi.")
        
    else:
        st.error("Gagal mengambil data metrik dari API. Pastikan API berjalan.")

# -----------------------------------------------------------------------------
# MAIN APP LOGIC
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E88E5; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #555; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

if st.session_state.role is None:
    show_login_page()
elif st.session_state.role == 'user':
    show_user_page()
elif st.session_state.role == 'admin':
    show_admin_page()
