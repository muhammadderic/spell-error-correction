import numpy as np
import tensorflow as tf

from utils.correction.encode_word import encode_word

max_dec_len = 15

# Correcting word
def correcting_word(char_set, char2int, int2char, model_corr, word):
  # encoding kata masukan (word to vector)
  encoder_inputs = encode_word(char_set, char2int, word)

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