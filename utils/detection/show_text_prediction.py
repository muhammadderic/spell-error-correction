import streamlit as st

def show_text_prediction(y_pred):
    if 1 in y_pred:
        text = f"This sentence contains error word/words."
        st.warning(text)
        return 1
    else:
        text = f"This sentence contains no errors."
        st.success(text)
        return 0