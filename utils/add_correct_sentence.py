import streamlit as st
from supabase import create_client, Client

def add_correct_sentence(kalimat_salah, correct_sentence):
    # Initialize Supabase client once
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    supabase.table("spelling_correction").insert({
                "kalimat_salah": kalimat_salah,
                "kalimat_benar": correct_sentence
            }).execute()

    # if st.button("Simpan"):
    #     if correct_sentence.strip():  # Ensure valid input
    #         supabase.table("spelling_correction").insert({
    #             "kalimat_salah": kalimat_salah,
    #             "kalimat_benar": correct_sentence
    #         }).execute()
    #         st.success("Data successfully inserted!")
    #     else:
    #         st.warning("Kalimat koreksi tidak boleh kosong.")
