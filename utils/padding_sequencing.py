import tensorflow as tf

def padding_sequencing(input_seq, text):
    max_sequence_len = max([len(x) for x in input_seq])

    input_seq_pad = tf.keras.preprocessing.sequence.pad_sequences(
        input_seq,
        maxlen=max_sequence_len,
        padding='post'
    )

    return input_seq_pad

    