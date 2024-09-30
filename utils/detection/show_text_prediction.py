import streamlit as st

def show_text_prediction(y_pred):
    if 1 in y_pred:
        text = f"⚠️ Kalimat ini mengandung kata/kata-kata yang salah"
        st.toast(text)
        return 1
    else:
        text = f"✅ Kalimat ini tidak mengandung kata yang salah"
        st.toast(text)
        return 0