import re

def text_preprocessing(text):
    # lowering text
    t = str(text).lower()
    # hapus HTML special entities, contoh: &amp; / &quot;
    # t = re.sub(r'\&\w*;', '', t)
    t = re.sub(r'&\w+;', '', t)
    # hapus titik (.) dalam angka ribuan, contoh: Rp5.000
    t = re.sub("\\.+(?=\d)", "", t)
    # hapus hyperlinks, contoh: google.com
    # t = re.sub('(\w*).(com|co.id)', '', t) 
    t = re.sub(r'\b\w+\.(com|co\.id)\b', '', t)
    # hapus hyperlinks, contoh: http://www.google.com
    t = re.sub(r'http\S+', '', t)
    # hapus karakter non-ascii
    t = re.sub('[^\x00-\x7F]+', ' ', t)
    # Replace ASCII control character \x02 with a hyphen
    t = re.sub('\x02', '-', t)
    # Remove multiple spaces
    t = re.sub(r'\s{2,}', ' ', t)
    # hapus spasi di kanan & kiri
    t = t.strip()
    return t