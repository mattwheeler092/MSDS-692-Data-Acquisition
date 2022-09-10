import os
import re
import string


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    filepaths = []
    for obj in os.listdir(root):
        obj_path = os.path.abspath(os.path.join(root, obj))
        if os.path.isfile(obj_path):
            filepaths.append(obj_path)
        elif os.path.isdir(obj_path):
            filepaths += filelist(obj_path)
    return filepaths


def get_text(fileName):
    f = open(fileName, encoding="latin-1")
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile("[" + re.escape(string.punctuation) + "0-9\\r\\t\\n]")
    nopunct = regex.sub(
        " ", text
    )  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def html_format_string(search_result_words, terms):
    """ Function to convert search result words into HTML. """
    html_formated_words = []
    for word in search_result_words:
        if any(term in word for term in terms):
            html_formated_words.append(f"<b>{word}</b>")
        else:
            html_formated_words.append(word)
    return " ".join(html_formated_words)


def get_search_result_string(file, terms, num_words):
    """ Function to get the HTML formated search result string
        for a given file and search terms. Returns a specified
        number of words. The substring that is choosen contains
        the larger number of search terms. 
    """
    # Find the position indicies of the search terms within the text
    text_words = get_text(file).lower()
    word_pos_dict = {text_words.index(term): term for term in terms}
    word_pos_idxs = sorted(word_pos_dict.keys())
    # Find the text substring that contains the most search terms
    current_idx_group = [word_pos_idxs[0]]
    max_idx_group = []
    for idx in word_pos_idxs[1:]:
        if abs(current_idx_group[0] - idx) < num_words * 4.5:
            current_idx_group.append(idx)
        elif len(current_idx_group) > len(max_idx_group):
            current_idx_group, max_idx_group = [idx], current_idx_group
    midpoint_idx = max(max_idx_group, current_idx_group, key=len)[0]
    midpoint_term = word_pos_dict[midpoint_idx]
    # Contruct HTML search result string
    prefix, _, suffix = text_words.partition(midpoint_term)
    prefix_words = [w for w in prefix.replace("\n", " ").split(" ") if w != ""]
    suffix_words = [w for w in suffix.replace("\n", " ").split(" ") if w != ""]
    search_result_words = (
        prefix_words[-1 * num_words // 2 :]
        + [midpoint_term]
        + suffix_words[: num_words // 2]
    )
    return html_format_string(search_result_words, terms)


def get_file_HTML(file, terms, num_words=20):
    """ Function to get formatted HTML string for a valid search file. """
    html = f'<a href="file://{file}">{file}</a><br>'
    html += get_search_result_string(file, terms, num_words) + "<br><br>"
    return html


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    html = "<html>\n\t<body>\n\t<h2>Search results for <b>"
    html += f"{' '.join(terms)}</b> in {len(docs)} files </h2>"
    for doc in docs:
        html += f"\n\t\t{get_file_HTML(doc, terms, num_words=20)}"
    html += "\n</body>\n</html>"
    return html


def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
