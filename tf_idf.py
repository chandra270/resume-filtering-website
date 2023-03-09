from sklearn.feature_extraction.text import TfidfVectorizer


def do_tfidf(token):
    tfidf = TfidfVectorizer(max_df=0.06, min_df=0.001)
    words = tfidf.fit_transform(token)
    sentence = " ".join(tfidf.get_feature_names())
    return sentence
