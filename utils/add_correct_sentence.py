import streamlit as st
from supabase import create_client, Client

def add_correct_sentence(kalimat_salah, kalimat_koreksi):
  url = st.secrets["SUPABASE_URL"]
  key = st.secrets["SUPABASE_KEY"]

  supabase: Client = create_client(url, key)

  if st.button("Simpan"):
    supabase.table("spelling_correction").insert({"kalimat_salah": kalimat_salah, "kalimat_benar": kalimat_koreksi}).execute()