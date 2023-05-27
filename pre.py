# import pymorphy2
# import nltk

# from nltk.tokenize import word_tokenize
# from nltk.stem.snowball import RussianStemmer

# from string import punctuation

# def text_preprocessing(some_text):
#   stopwords = nltk.corpus.stopwords.words('russian')
#   morph = pymorphy2.MorphAnalyzer()
#   stemmer = RussianStemmer(True)
#   punctuations = list(punctuation)
#   words_without_punct = [i for i in word_tokenize(some_text.lower()) if (i not in punctuations) and (i not in stopwords)]
#   lem_stem = [morph.parse(i)[0].normal_form for i in words_without_punct]
#   return lem_stem

# text_preprocessing('какой-то текст')
