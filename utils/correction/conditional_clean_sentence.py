import re

def conditional_clean_sentence(clean_sentence, raw_sentence):
    # Split both sentences into words
    clean_words = clean_sentence.split()
    raw_words = re.findall(r'\w+|\S', raw_sentence)  # Words and punctuation
    
    # Initialize the transformed sentence
    transformed_sentence = []
    
    clean_idx = 0  # Index for tracking words in clean sentence
    
    for raw_token in raw_words:
        if re.match(r'\w+', raw_token):  # If it's a word
            if clean_idx < len(clean_words) and clean_words[clean_idx] == raw_token.lower():
                # Match clean word with raw word structure (case)
                transformed_sentence.append(raw_token)
            else:
                # If word doesn't match, use the word from the clean sentence
                transformed_sentence.append(clean_words[clean_idx])
            clean_idx += 1
        else:
            # Append punctuation as it is
            transformed_sentence.append(raw_token)
    
    # Join the transformed tokens into a final sentence
    return ''.join([' ' + token if token.isalnum() else token for token in transformed_sentence]).strip()