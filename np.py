import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Energy Forecast", page_icon="⚡")
st.title("⚡ Energy Consumption Forecasting")

class EnergyPredictor:
    def predict_energy(self, data):
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return 30000
        energy_data = data[numeric_cols[0]]
        if len(energy_data) < 7:
            return energy_data.mean() if len(energy_data) > 0 else 30000
        return energy_data.tail(7).mean()

def create_sample_data():
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    energies = [30000 + np.random.randint(-5000, 5000) for _ in range(30)]
    return pd.DataFrame({'date': dates, 'energy': energies})

predictor = EnergyPredictor()

uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if st.button("Generate Sample Data"):
    sample_data = create_sample_data()
    st.download_button("Download Sample", sample_data.to_csv(index=False), "sample.csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())
    if st.button("Predict"):
        prediction = predictor.predict_energy(data)
        st.success(f"Predicted: {prediction:,.0f} Wh")
