from tfidf import *

zipfilename = sys.argv[1]
summarizefile = sys.argv[2]

# Create tfidf model
corpus = load_corpus(zipfilename)
tfidf = compute_tfidf(corpus)

# Extract text for summarisation
with zipfile.ZipFile(zipfilename, "r") as zip:
    zipfolder = zipfilename.split("/")[-1].split(".")[0]
    xmltext = zip.read(os.path.join(zipfolder, summarizefile))

# Summarise file and print results
for word, score in summarize(tfidf, xmltext, n=20):
    print(word, format(round(score, 3), ".3f"))
