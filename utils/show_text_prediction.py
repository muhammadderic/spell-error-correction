import streamlit as st

def show_text_prediction(y_pred, error_text):
    if 1 in y_pred:
        text = f"This sentence contains {error_text} error word/words."
        st.warning(text)
    else:
        text = f"This sentence contains no {error_text} errors."
        st.success(text)