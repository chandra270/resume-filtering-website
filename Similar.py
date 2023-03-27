# pyright: reportUnusedVariable=false
import textdistance as td
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# import jellyfish

def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    # s = td.sorensen_dice.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    # o = td.overlap.normalized_similarity(resume, job_des)
    # total = (j+s+o+c)/4
    total = (j+c)/2
    return total*100

#cosine only
# def match(resume, job_des):
#     vectorizer = TfidfVectorizer()
#     tfidf = vectorizer.fit_transform([resume, job_des])
#     return cosine_similarity(tfidf)[0,1] * 100


# def match(resume, job_des):
#     similarity_scores = []
#     for job_skill in job_des:
#         max_score = 0
#         for resume_skill in resume:
#             score = jellyfish.jaro_winkler(job_skill, resume_skill)
#             if score > max_score:
#                 max_score = score
#         similarity_scores.append(max_score)
#     # Calculate the average similarity score across all job skills
#     average_similarity_score = sum(similarity_scores) / len(similarity_scores)

    # Calculate cosine similarity between resume and job description
    # vectorizer = TfidfVectorizer()
    # tfidf = vectorizer.fit_transform([resume, " ".join(job_des)])
    # a = cosine_similarity(tfidf)[0, 1]

    # # Calculate total similarity score as the average of the two scores
    # total = (average_similarity_score + a) / 2
    # return total * 100
