# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from words import get_text, words


def linear_search(files, terms):
    """
    Given a list of fully-qualified filenames, return a list of them
    whose file contents has all words in terms as normalized by your words() function.
    Parameter terms is a list of strings.
    Perform a linear search, looking at each file one after the other.
    """
    qualified_files = []
    for file in files:
        words_in_file = words(get_text(file))
        for term in terms:
            if term not in words_in_file:
                break
        else:
            qualified_files.append(file)
    return qualified_files
