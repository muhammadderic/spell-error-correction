import string
import numpy as np
import streamlit as st
import re
import tensorflow as tf

st.title('Spell Error Correction')

text = st.text_area('Input your text here')

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

model_path = "./model_bilstm-mh_attm_epoch-100_batch-64_ALL.h5"
max_enc_len = 14
max_dec_len = 15

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

def load_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None
    
model = load_model(model_path)


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