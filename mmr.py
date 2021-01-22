#PROSES MENYIMPULKAN
import os
import re
import sys
import operator
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def load_stopWords():
	f = open('stopword.txt', 'r')
	return f.readlines()

stopwords = load_stopWords()	

def cleanData(sentence):
	ret = []
	sentence = stemmer.stem(sentence)	
	for word in sentence.split():
		if not word in stopwords:
			ret.append(word)
	return " ".join(ret)


def getVectorSpace(cleanSet):
	vocab = {}
	for data in cleanSet:
		for word in data.split():
			vocab[data] = 0
	return vocab.keys()
	
def calculateSimilarity(sentence, doc):
	if doc == []:
		return 0
	vocab = {}
	for word in sentence:
		vocab[word] = 0
	
	docInOneSentence = ''
	for t in doc:
		docInOneSentence += (t + ' ')
		for word in t.split():
			vocab[word]=0	

	cv = CountVectorizer(vocabulary=vocab.keys())

	docVector = cv.fit_transform([docInOneSentence])
	sentenceVector = cv.fit_transform([sentence])
	return cosine_similarity(docVector, sentenceVector)[0][0]

data = open(sys.argv[1], 'r')
texts = data.readlines()

sentences = []
clean = []
originalSentenceOf = {}

#Data cleansing
for line in texts:
	parts = line.split('.')
	for part in parts:
		cl = cleanData(part)
		sentences.append(part)
		clean.append(cl)
		originalSentenceOf[cl] = part		
setClean = set(clean)

#calculate Similarity score each sentence with whole documents		
scores = {}
for data in clean:
	temp_doc = setClean - set([data])
	score = calculateSimilarity(data, list(temp_doc))
	scores[data] = score
	#print score


#calculate MMR
n = 20 * len(sentences) / 100
alpha = 0.5
summarySet = []
while n > 0:
	mmr = {}
	#kurangkan dengan set summary
	for sentence in scores.keys():
		if not sentence in summarySet:
			mmr[sentence] = alpha * scores[sentence] - (1-alpha) * calculateSimilarity(sentence, summarySet)	
	selected = max(mmr.items(), key=operator.itemgetter(1))[0]	
	summarySet.append(selected)
	n -= 1

"""
print('\nKesimpulan:\n')
for sentence in summarySet:
	print(originalSentenceOf [sentence].lstrip(' ') + ". ") 
"""

#PROSES TAGGING
from nltk.tag import CRFTagger
from nltk.tokenize import WhitespaceTokenizer 
"""
import nltk
nltk.download('punkt')
"""
ct = CRFTagger()
ct.set_model_file('all_indo_man_tag_corpus_model.crf.tagger')

text = []
for sentence in summarySet:
	text.append(originalSentenceOf[sentence].lstrip(' ') + ". ")

text1 = "".join(text)
tk = WhitespaceTokenizer()
tokenizingResults = ct.tag_sents([tk.tokenize(text1)])
print(tokenizingResults)

#NEXT: hitung word occurences sesuai tag
#NEXT2: kata paling banyak di gabungin sama kata dari tag lain yang paling banyak juga