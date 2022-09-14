import sys

from tfidf import *

with open(sys.argv[1], "r") as file:
    xmltext = file.read()
text = gettext(xmltext)
word_count = Counter(tokenizer(text))
most_common = sorted(word_count, key=lambda x: word_count[x], reverse=True)
for key in most_common[:10]:
    print(key, word_count[key])
