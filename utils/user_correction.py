import streamlit as st

@st.dialog("Koreksi")
def vote():
    reason = st.text_input("Masukkan kalimat yang benar")
    if st.button("Koreksi"):
        # Store the reason in session_state
        st.session_state.vote = {"reason": reason}
        return st.session_state.vote.get("reason")

def show_correction_dialog():
    if "vote" not in st.session_state:
        st.write("Apakah kalimat koreksi sudah benar?")
        if st.button("👍"):
            st.session_state.vote = {"reason": "Kalimat sudah benar"}
            return st.session_state.vote.get("reason")
        if st.button("👎"):
            vote()