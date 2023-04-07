import textdistance as td
from nltk.metrics.distance import jaccard_distance

def matchJ(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    return j * 100


def matchS(resume, job_des):
    s = td.sorensen_dice.similarity(resume, job_des)
    return s*100

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def matchC(resume, job_des):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume, job_des])
    cos_sim = cosine_similarity(tfidf[0], tfidf[1])
    return np.round(cos_sim[0][0] * 100, 2)

def matchO(resume, job_des):
    o = td.overlap.normalized_similarity(resume, job_des)
    return o*100

def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    o = td.overlap.normalized_similarity(resume, job_des)
    total = (j+s+o+c)/4
    # total = (s+o)/2
    return total*100

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

def matchLSA(resume, job_des):
    # preprocess the documents
    documents = [resume, job_des]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(documents)
    vocab = vectorizer.get_feature_names_out()

    # apply LSA
    lsa_model = TruncatedSVD(n_components=2)
    lsa_vectors = lsa_model.fit_transform(tfidf)

    # calculate cosine similarity between the documents
    similarity = cosine_similarity(lsa_vectors)[0][1]

    # return the similarity score as a percentage
    return similarity * 100

