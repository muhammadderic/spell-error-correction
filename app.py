import string
import streamlit as st
import numpy as np
import tensorflow as tf

from utils.text_preprocessing import text_preprocessing
from utils.load_model import load_model
from utils.add_correct_sentence import add_correct_sentence

# From detection folder
from utils.detection.tokenizer import tokenization
from utils.detection.get_word_index import get_word_index
from utils.detection.padding_sequencing import padding_sequencing
from utils.detection.embedding import embedding
from utils.detection.show_text_prediction import show_text_prediction

# From correction folder
from utils.correction.load_dictionary import load_dictionary
from utils.correction.conditional_clean_sentence import conditional_clean_sentence

# Variables
model_corr_fn = './models/model_bilstm-mh_attm_epoch-100_batch-64_BI.h5'

model_det_fn = './models/word_error_detection_all_subjects.h5'

# Header
header_left, header_right = st.columns([1,5], vertical_alignment="center")

with header_left:
    st.image("assets/peka.jpeg", width=120)

with header_right:
    st.subheader('Pendeteksi dan Koreksi Ejaan')

# Input
input_text = st.text_area('Masukkan kalimat')

# Create a placeholder for the button
submit = st.button('Koreksi', key='tombol_koreksi')

# Text preprocessing
text = text_preprocessing(input_text)

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
my_dictionary = load_dictionary("./my_dictionary.txt")
sastrawi_dictionary = load_dictionary("./sastrawi_dictionary.txt")

# ===================
# Correction Function
# ===================
max_enc_len = 14

# Convert word to vector
def encode_word(word: list):
  encoded_word = np.zeros((1, max_enc_len, len(char_set)), dtype='float32')

  for _,inp in enumerate(word):
    for row, char in enumerate(inp):
      encoded_word[0, row, char2int[char]] = 1

  return encoded_word

max_dec_len = 15

# Correcting word
def correcting_word(word):
  # encoding kata masukan (word to vector)
  encoder_inputs = encode_word(word)

  # decoding kata masukan
  decoder_inputs = np.zeros((1, max_dec_len, len(char_set)+2), dtype='float32')
  decoder_inputs[:, 0, char2int['\t']] = 1

  input_word = ''
  pred_word = ''

  # melakukan koreksi per-huruf dari kata masukan
  for idx in range(decoder_inputs.shape[1]-1):
    pred_arr = model_corr.predict([
        tf.constant(encoder_inputs),
        tf.constant(decoder_inputs)
    ], verbose=0)

    input2_idx = np.argmax(pred_arr[:, idx, :], axis=1)[0]
    decoder_inputs[:, idx+1, input2_idx] = 1

    input1_idx = np.argmax(encoder_inputs[:, idx, :], axis=1)[0]

    pred_word += int2char[input2_idx]
    input_word += int2char[input1_idx]

    if (pred_word[-1] == '\n'):
      break

  # menghapus next line character
  pred_word = pred_word[:-1]

  return pred_word

# Generate corrected sentence
def generate_corrected_sentence(sentence: str):
  corrected_word = None  # Inisialisasi corrected_word
  word_idx = -1  # Inisialisasi word_idx

  for word_idx, word in enumerate(sentence.split()):
    if word not in my_dictionary:
      corrected_word = correcting_word([word])
      break

  if corrected_word is None:  # Jika tidak ada kata yang berbeda
    return sentence  # Mengembalikan kalimat asli tanpa perubahan

  corrected_sentence = sentence.split()
  corrected_sentence[word_idx] = corrected_word
  return " ".join(corrected_sentence)

# Detection sentence
if submit:
    detection_result = 0
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

    # Detect the wrong word
    for word_idx, word in enumerate(text.split()):
      if word not in my_dictionary:
        show_text_prediction(1)
        detection_result = 1
        break

    # Correction sentence
    if detection_result == 1:
        
        sentence = generate_corrected_sentence(text)
        transformed_sentence = conditional_clean_sentence(sentence, input_text)

        with st.spinner('Sedang mengkoreksi...'):
            st.subheader("Hasil koreksi:")
            st.info(transformed_sentence)

            with st.popover("Koreksi kalimat, jika kalimat salah", use_container_width=True):
                correct_sentence = st.text_area("Kalimat yang benar menurut anda adalah:")

                # Add a submit button
                add_correct_sentence(transformed_sentence, correct_sentence)
    else:
        show_text_prediction(0)