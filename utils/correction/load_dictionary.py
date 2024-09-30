# Load dictionary Reads a text file and converts its contents into a list of words.
def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into words
    word_list = text.split()

    return word_list