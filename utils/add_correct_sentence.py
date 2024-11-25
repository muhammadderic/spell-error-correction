import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client once
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def add_correct_sentence(kalimat_salah='default', kalimat_koreksi='default'):
    # Validate input
    if not kalimat_salah.strip() or not kalimat_koreksi.strip():
        st.error("Both 'kalimat_salah' and 'kalimat_koreksi' must be provided.")
        return

    try:
        # Insert data into Supabase
        result = supabase.table("spelling_correction").insert({
                            "kalimat_salah": kalimat_salah,
                            "kalimat_benar": kalimat_koreksi
                        }).execute()

        st.success("Data successfully inserted!")
        st.write("Result:", result)
    except Exception as e:
        st.error(f"Failed to insert data: {e}")
