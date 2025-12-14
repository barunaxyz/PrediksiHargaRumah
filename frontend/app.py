import streamlit as st
import requests
from PIL import Image
import os

# Title
st.title("House Price Prediction")
st.subheader("Enter the house details below to get a price prediction.")

# Form
with st.form(key='house_data_form'):
    LB = st.number_input(
        label = "Building Area (m2) / Luas Bangunan",
        min_value = 30,
        max_value = 2000,
        value = 100
    )
    
    LT = st.number_input(
        label = "Land Area (m2) / Luas Tanah",
        min_value = 20,
        max_value = 2000,
        value = 120
    )

    KT = st.number_input(
        label = "Number of Bedrooms / Jumlah Kamar Tidur",
        min_value = 1,
        max_value = 15,
        value = 3
    )

    KM = st.number_input(
        label = "Number of Bathrooms / Jumlah Kamar Mandi",
        min_value = 1,
        max_value = 15,
        value = 2
    )

    GRS = st.number_input(
        label = "Garage Capacity (Cars) / Kapasitas Garasi",
        min_value = 0,
        max_value = 15,
        value = 1
    )

    submit_button = st.form_submit_button(label='Predict Price')

if submit_button:
    # Prepare data
    data = {
        "LB": LB,
        "LT": LT,
        "KT": KT,
        "KM": KM,
        "GRS": GRS
    }
    
    # Call API
    # Get the API URL from environment variables, defaulting to localhost for local testing
    api_url = os.getenv("API_URL", "http://localhost:5000/predict") 
    
    with st.spinner("Calculating..."):
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'success':
                    price = result['prediction']
                    st.success(f"Estimated Price: Rp {price:,.2f}")
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
            else:
                st.error(f"Failed to connect to API. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")
