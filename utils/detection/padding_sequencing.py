import tensorflow as tf

def padding_sequencing(input_seq):
    # Check if the input sequence is empty
    if not input_seq:
        raise ValueError("Input sequence is empty. Cannot apply padding to an empty sequence.")
    
    max_sequence_len = max([len(x) for x in input_seq])

    input_seq_pad = tf.keras.preprocessing.sequence.pad_sequences(
        input_seq,
        maxlen=max_sequence_len,
        padding='post'
    )

    return input_seq_pad

    