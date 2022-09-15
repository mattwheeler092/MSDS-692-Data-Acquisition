import os
import string
import sys
import xml.etree.cElementTree as ET
import zipfile
from collections import Counter

import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer


def gettext(xmltext) -> str:
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    xmltext = xmltext.encode("ascii", "ignore")  # ensure there are no weird char
    tree = ET.ElementTree(ET.fromstring(xmltext))
    title = [elem.text for elem in tree.iterfind("title")]
    text = [elem.text for elem in tree.iterfind(".//text/*")]
    return " ".join(title + text)


def tokenize(text) -> list:
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3, strip digits.
    """
    text = text.lower()
    text = re.sub("[" + string.punctuation + "0-9\\r\\t\\n]", " ", text)
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if len(w) > 2]  # ignore a, an, to, at, be, ...
    return [w for w in tokens if w not in ENGLISH_STOP_WORDS]


def stemwords(words) -> list:
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in words]


def tokenizer(text) -> list:
    return stemwords(tokenize(text))


def compute_tfidf(corpus: dict) -> TfidfVectorizer:
    """
    Create and return a TfidfVectorizer object after training it on
    the list of articles pulled from the corpus dictionary. Meaning,
    call fit() on the list of document strings, which figures out
    all the inverse document frequencies (IDF) for use later by
    the transform() function. The corpus argument is a dictionary
    mapping file name to xml text.
    """
    tfidf = TfidfVectorizer(
        input="content",
        analyzer="word",
        preprocessor=gettext,
        tokenizer=tokenizer,
        stop_words="english",
        decode_error="ignore",
    )
    tfidf.fit(corpus.values())
    return tfidf


def summarize(tfidf: TfidfVectorizer, text: str, n: int):
    """
    Given a trained TfidfVectorizer object and some XML text, return
    up to n (word,score) pairs in a list. Discard any terms with
    scores < 0.09. Sort the (word,score) pairs by TFIDF score in reverse order.
    """
    results = []
    scores = tfidf.transform([text])
    feature_words = tfidf.get_feature_names()
    _, word_idxs = scores.nonzero()
    for idx in word_idxs:
        results.append((feature_words[idx], scores.toarray()[0][idx]))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return [res for res in results if res[1] >= 0.09][:n]


def load_corpus(zipfilename: str) -> dict:
    """
    Given a zip file containing root directory reuters-vol1-disk1-subset
    and a bunch of *.xml files, read them from the zip file into
    a dictionary of (filename,xmltext) associations. Use namelist() from
    ZipFile object to get list of xml files in that zip file.
    Convert filename reuters-vol1-disk1-subset/foo.xml to foo.xml
    as the keys in the dictionary. The values in the dictionary are the
    raw XML text from the various files.
    """
    corpus = {}
    with zipfile.ZipFile(zipfilename, "r") as zip:
        zip.extractall()
        for filepath in zip.namelist():
            if filepath.endswith(".xml"):
                folder, file = filepath.split("/")
                with open(filepath, "r") as xmlfile:
                    corpus[file] = xmlfile.read()
                os.remove(filepath)
        os.rmdir(folder)
    return corpus
