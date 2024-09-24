import numpy as np
from gensim.models import Word2Vec

def embedding(words, word_index):
    word_vectors = Word2Vec(
          sentences=words,
          vector_size=100, #dimensi vektor kata
          window=5, #Jarak maksimum antara kata target dan kata-kata di sekitarnya.
          min_count=1, #Kata-kata harus muncul setidaknya sekali untuk dianggap.
          workers=4 #Menggunakan 4 worker threads untuk pelatihan.
      )

    embedding_dim = 100
    embedding_matrix = np.zeros((len(word_index)+1, embedding_dim))

    for word, i in word_index.items():
        if word in word_vectors.wv.index_to_key:
            embedding_matrix[i] = word_vectors.wv[word]

    return embedding_matrix