from utils.correction.word_corrector import correcting_word

# Generate corrected sentence
def generate_corrected_sentence(sastrawi_dictionary, my_dictionary, char_set, char2int, int2char, model_corr, sentence: str):
  corrected_word = None  # Inisialisasi corrected_word
  word_idx = -1  # Inisialisasi word_idx

  def spell_check(kata_list, kamus):
    kata_salah = [kata for kata in kata_list if kata.lower() not in kamus]
    return kata_salah

  for word_idx, word in enumerate(sentence.split()):
    if word not in sastrawi_dictionary or word not in my_dictionary:
      corrected_word = correcting_word(char_set, char2int, int2char, model_corr, [word])
      break

  if corrected_word is None:  # Jika tidak ada kata yang berbeda
    return sentence  # Mengembalikan kalimat asli tanpa perubahan

  corrected_sentence = sentence.split()
  corrected_sentence[word_idx] = corrected_word
  return " ".join(corrected_sentence)