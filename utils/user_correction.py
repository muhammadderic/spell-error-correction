import streamlit as st

@st.dialog("Koreksi")
def vote(item):
    reason = st.text_input("Masukkan kalimat yang benar")
    if st.button("Koreksi"):
        # Store the reason in session_state
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

def show_correction_dialog():
    if "vote" not in st.session_state:
        st.write("Apakah kalimat koreksi sudah benar?")
        if st.button("👍"):
            vote("right")
        if st.button("👎"):
            vote("wrong")
    else:
        st.write("Terima kasih telah mengkoreksi!")
        # Return the reason for further use
        return st.session_state.vote.get("reason")