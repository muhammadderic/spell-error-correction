import streamlit as st
from supabase import create_client, Client

def add_correct_sentence(kalimat_salah='default', kalimat_koreksi='default'):
    # Initialize Supabase client once
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    # Insert data into Supabase
    if st.button("Simpan"):
        supabase.table("spelling_correction").insert({
                            "kalimat_salah": kalimat_salah,
                            "kalimat_benar": kalimat_koreksi
                        }).execute()

        st.success("Data successfully inserted!")
