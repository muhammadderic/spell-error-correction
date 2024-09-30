import numpy as np

max_enc_len = 14

# Convert word to vector
def encode_word(char_set, char2int, word: list):
  encoded_word = np.zeros((1, max_enc_len, len(char_set)), dtype='float32')

  for _,inp in enumerate(word):
    for row, char in enumerate(inp):
      encoded_word[0, row, char2int[char]] = 1

  return encoded_word