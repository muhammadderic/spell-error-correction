import tensorflow as tf

def tokenization(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer(oov_token='oov')
    tokenizer.fit_on_texts(text)

    # num_words = len(tokenizer.word_index)+1

    word_index = tokenizer.word_index

    input_seq = tokenizer.texts_to_sequences(text)

    return input_seq, word_index