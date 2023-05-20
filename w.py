# import numpy as np

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# import pymorphy2

# import statistics

# from nltk.tokenize import word_tokenize
# from nltk.stem.snowball import RussianStemmer

# from string import punctuation

# import matplotlib.pyplot as plt

# def preprocessed_text(texts):
#     stopwords = nltk.corpus.stopwords.words('russian')
#     morph = pymorphy2.MorphAnalyzer()
#     stemmer = RussianStemmer(True)
#     punctuations = list(punctuation)
#     preprocessed_texts = []

#     for i in range(0, len(texts)):
#         words_without_punct = [j for j in word_tokenize(texts[i].lower()) if (j not in punctuations) and (j not in stopwords)]
#         lem_stem = [morph.parse(j)[0].normal_form for j in words_without_punct]
#         preprocessed_texts.append(' '.join(lem_stem))

#     return preprocessed_texts

# preprocessed_text('привет! это текст')