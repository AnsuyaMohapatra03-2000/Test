import streamlit as st

st.title("🚀 My First Streamlit App")
st.write("Hello, welcome to my web app!")

# Example input
name = st.text_input("Enter your name")
if name:
    st.success(f"Hello, {name} 👋")

# Example chart
import pandas as pd
import numpy as np
data = pd.DataFrame({
    'x': np.arange(10),
    'y': np.random.randn(10)
})
st.line_chart(data.set_index('x'))
