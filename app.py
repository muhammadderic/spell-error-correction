import string
import numpy as np
import streamlit as st
import tensorflow as tf

from utils.text_preprocessing import text_preprocessing
from utils.load_model import load_model
from utils.tokenizer import tokenization
from utils.get_word_index import get_word_index
from utils.padding_sequencing import padding_sequencing
from utils.embedding import embedding
from utils.show_text_prediction import show_text_prediction

# Variables
model_path = "./model_bilstm-mh_attm_epoch-100_batch-64_ALL.h5"

model_trans_fn = f"./models/model_text_clf_v3_transposition_6.h5"
model_punc_fn = f"./models/model_text_clf_v3_punctuation_6.h5"
model_subs_fn = f"./models/model_text_clf_v3_substitution_6.h5"
model_rw_fn = f"./models/model_text_clf_v3_real-word_6.h5"
model_del_fn = f"./models/model_text_clf_v3_deletion_6.h5"
model_ins_fn = f"./models/model_text_clf_v3_insertion_6.h5"

max_enc_len = 14
max_dec_len = 15

# Header
st.markdown(
    """
    <style>
    .header-img {
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3); /* Shadow under the image */
    }
    h1 {
        text-align: center; /* Center the title */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.title('Spell Error Correction')

# Apply the CSS to the image
st.markdown('<img class="header-img" src="assets/peka.jpeg" style="width: 200px;">', unsafe_allow_html=True)

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
model = load_model(model_path)

# Load detection models
model_trans = load_model(model_trans_fn)
model_punc = load_model(model_punc_fn)
model_subs = load_model(model_subs_fn)
model_rw = load_model(model_rw_fn)
model_del = load_model(model_del_fn)
model_ins = load_model(model_ins_fn)


# Load dictionary Reads a text file and converts its contents into a list of words.
def file_to_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into words
    word_list = text.split()

    return word_list

# Load dictionary
sastrawi_dictionary = file_to_word_list("./sastrawi_dictionary.txt")

# Convert word to vector
def encode_word(word: list):
  encoded_word = np.zeros((1, max_enc_len, len(char_set)), dtype='float32')

  for _,inp in enumerate(word):
    for row, char in enumerate(inp):
      encoded_word[0, row, char2int[char]] = 1

  return encoded_word


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
    pred_arr = model.predict([
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

  def spell_check(kata_list, kamus):
    kata_salah = [kata for kata in kata_list if kata.lower() not in kamus]
    return kata_salah

  for word_idx, word in enumerate(sentence.split()):
    if word not in sastrawi_dictionary:
      corrected_word = correcting_word([word])
      break

  if corrected_word is None:  # Jika tidak ada kata yang berbeda
    return sentence  # Mengembalikan kalimat asli tanpa perubahan

  corrected_sentence = sentence.split()
  corrected_sentence[word_idx] = corrected_word
  return " ".join(corrected_sentence)

sentence = generate_corrected_sentence(text)

st.success(sentence)

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

    # Transposition
    y_trans_pred = model_trans.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    show_text_prediction(y_trans_pred, "transposition")

    # Punctuation
    y_punc_pred = model_trans.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    show_text_prediction(y_punc_pred, "punctuation")

    # Substitution
    y_subs_pred = model_trans.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    show_text_prediction(y_subs_pred, "substitution")

    # Real-word
    y_rw_pred = model_trans.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    show_text_prediction(y_rw_pred, "real-word")

    # Deletion
    y_del_pred = model_trans.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    show_text_prediction(y_del_pred, "deletion")

    # Insertion
    y_ins_pred = model_trans.predict(embedding_matrix, verbose=0).argmax(axis=-1)
    show_text_prediction(y_ins_pred, "insertion")