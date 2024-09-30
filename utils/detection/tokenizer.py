import tensorflow as tf

def tokenization(text):
    # Check if input is empty
    if not text:
        print("Input is empty.")
        return []
    
    tokenizer = tf.keras.preprocessing.text.Tokenizer(oov_token='oov')
    tokenizer.fit_on_texts(text)

    input_seq = tokenizer.texts_to_sequences(text)

    # Debugging prints
    print("Word Index:", tokenizer.word_index)
    print("Input Sequences:", input_seq)

    return input_seq