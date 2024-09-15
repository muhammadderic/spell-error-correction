import streamlit as st
import re
import keras

st.title('Spell Error Correction')

text = st.text_input('Input text')

submit = st.button('Correcting')

def text_preprocessing(text):
    # lowering text
    t = str(text).lower()
    # hapus HTML special entities, contoh: &amp; / &quot;
    # t = re.sub(r'\&\w*;', '', t)
    t = re.sub(r'&\w+;', '', t)
    # hapus titik (.) dalam angka ribuan, contoh: Rp5.000
    t = re.sub("\\.+(?=\d)", "", t)
    # hapus hyperlinks, contoh: google.com
    # t = re.sub('(\w*).(com|co.id)', '', t) 
    t = re.sub(r'\b\w+\.(com|co\.id)\b', '', t)
    # hapus hyperlinks, contoh: http://www.google.com
    t = re.sub(r'http\S+', '', t)
    # hapus karakter non-ascii
    t = re.sub('[^\x00-\x7F]+', ' ', t)
    # Replace ASCII control character \x02 with a hyphen
    t = re.sub('\x02', '-', t)
    # Remove multiple spaces
    t = re.sub(r'\s{2,}', ' ', t)
    # hapus spasi di kanan & kiri
    t = t.strip()
    return t

text = text_preprocessing(text)

model_path = "model_bilstm_epoch-100_batch-64_ALL.h5"

def load_model(model_path):
    try:
        model = keras.models.load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None
    
load_model(model_path)

st.success(text)