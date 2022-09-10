# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    index = htable(4011)
    for idx, file in enumerate(files):
        for word in words(get_text(file)):
            word_files = htable_get(index, word)
            if word_files is None:
                htable_put(index, word, {idx})
            else:
                word_files.add(idx)
    return index


def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    qualified_files = htable_get(index, terms[0])
    if qualified_files is None:
        qualified_files = set()
    for term in terms[1:]:
        other_files = htable_get(index, term)
        if other_files is None:
            other_files = set()
        qualified_files = qualified_files.intersection(other_files)
    return [file for idx, file in enumerate(files) if idx in qualified_files]
