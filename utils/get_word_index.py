import tensorflow as tf

def get_word_index(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer(oov_token='oov')
    tokenizer.fit_on_texts(text)

    word_index = tokenizer.word_index

    return word_index
