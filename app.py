import string
import streamlit as st

from utils.correction.main_correction import generate_corrected_sentence
from utils.text_preprocessing import text_preprocessing
from utils.load_model import load_model

# From detection folder
from utils.detection.tokenizer import tokenization
from utils.detection.get_word_index import get_word_index
from utils.detection.padding_sequencing import padding_sequencing
from utils.detection.embedding import embedding
from utils.detection.show_text_prediction import show_text_prediction

# From correction folder
from utils.correction.load_dictionary import load_dictionary

# Variables
model_corr_fn = './models/model_bilstm-mh_attm_epoch-100_batch-64_ALL.h5'

model_det_fn = './models/word_error_detection_all_subjects.h5'

# Header
header_left, header_right = st.columns([1,5], vertical_alignment="center")

with header_left:
    st.image("assets/peka.jpeg", width=120)

with header_right:
    st.subheader('Pendeteksi dan Koreksi Ejaan')

# Input
text = st.text_area('Masukkan kalimat')

submit = st.button('Koreksi')

# Text preprocessing
text = text_preprocessing(text)

# Create encode and decode dictionary
char_set = list(" abcdefghijklmnopqrstuvwxyz0123456789") + [x for x in string.punctuation]
char2int = { char_set[x]:x for x in range(len(char_set)) }
int2char = { char2int[x]:x for x in char_set }

# Add escape character to encode and decode characters
count = len(char_set)
codes = ["\t","\n"]
for i in range(len(codes)):
    code = codes[i]
    char2int[code] = count
    int2char[count] = code
    count+=1

# Load correction model   
model_corr = load_model(model_corr_fn)

# Load detection models
model_det = load_model(model_det_fn)

# Load dictionary
sastrawi_dictionary = load_dictionary("./sastrawi_dictionary.txt")

detection_result = 0

# Detection sentence
if submit:
    # Tokenization
    input_seq = tokenization(text)

    # Padding Sequencing
    input_seq_pad = padding_sequencing(input_seq)

    # Split words
    def split_word(sentence: str): return sentence.split(' ')

    words = split_word(text)

    # Get word index
    word_index = get_word_index(text)

    # Embedding
    embedding_matrix = embedding(words, word_index)

    # Detection
    y_pred = model_det.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    detection_result = show_text_prediction(y_pred)

# Correction sentence
if detection_result == 1:
    sentence = generate_corrected_sentence(sastrawi_dictionary, char_set, char2int, int2char, model_corr, text)

    st.text("Hasil koreksi:")
    st.info(sentence)

    # reason = ""

# Show the correction dialog and capture the reason
@st.dialog("Koreksi")
def vote():
    reason = st.text_input("Masukkan kalimat yang benar")
    if st.button("Koreksi"):
        st.session_state.vote = {"reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Apakah kalimat koreksi sudah benar?")
    if st.button("👍"):
        st.session_state.vote = {"reason": "Kalimat sudah benar"}
        st.rerun()
    if st.button("👎"):
        vote()
else:
    # Safely access the vote result from session_state
    vote_info = st.session_state.vote  # Retrieve the vote info
    st.write(f"Terima kasih telah mengkoreksi! Alasan: {vote_info['reason']}")