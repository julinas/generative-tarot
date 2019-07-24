from collections import Counter
import itertools
from nltk.corpus import wordnet
import random
import spacy
from textblob import TextBlob
import time

import warnings
warnings.filterwarnings('ignore')

from retrieve_sentiment import getSentiment

nlp = spacy.load("en_core_web_lg")

themepath = 'themestext'

wordCounter = Counter()

with open (themepath, "r") as f:
	data = f.readlines()
	for line in data:
		words = line.split()
		wordCounter.update(words)
		
lemmaCounter = Counter()

tobe = nlp('is')[0].lemma

# testText = getSentiment('football')

# test = TextBlob(testText).sentiment
# print(test)
# print(type(test.polarity))
# print(test[1])
		
n = len(list(wordCounter))		
for word in wordCounter.most_common(n):
	text = word[0].lower()
	text = text.replace('”', '')
	text = text.replace('“', '')
	text = text.replace('\'s', '')
	token = nlp(text)[0]
	
	if (not token.is_alpha) or \
		(token.pos_ is not 'NOUN' and token.pos_ is not 'VERB') or \
		(token.lemma == tobe):
		del wordCounter[word[0]]
	else:
		lemmaCounter.update({token.lemma_: word[1]})		

n = len(list(lemmaCounter))
print(n)
print(lemmaCounter.most_common(22))
for ele in lemmaCounter.most_common(22):
	op = TextBlob(ele[0]).sentiment
	print(ele[0], op)

list_of = list(lemmaCounter.most_common(n))
iter_of = iter(list_of)

for lemma in iter_of:
	syns1 = wordnet.synsets(lemma[0], pos = wordnet.NOUN)
	for lemma2 in lemmaCounter.most_common(n):
		if lemma[0] == lemma2[0]:
			continue
		syns2 = wordnet.synsets(lemma2[0], pos = wordnet.NOUN)
		
		for syn1, syn2 in itertools.product(syns1, syns2):
			if syn1.lch_similarity(syn2) >= 2.7:
				lemmaCounter[lemma[0]] += lemma2[1]
				list_of.remove(lemma2)
				del lemmaCounter[lemma2[0]]
				print("merged {} and {}".format(lemma[0], lemma2[0]))
			break

n = len(list(lemmaCounter))
trumps = lemmaCounter.most_common(22)
# suits = list(lemmaCounter.most_common(78))[22:]
therest = list(lemmaCounter.most_common(n))[22:]

print(n)

print(trumps)
# print(suits)
# print(therest)

suit1 = [] # neg polarity # <0.5 subjectivity
suit2 = [] # neg polarity # >=0.5 subjectivity
suit3 = [] # pos polarity # <0.5 subjectivity
suit4 = [] # pos polarity # >=0.5 subjectivity

for ele in therest[746:]:

	# (polarity[-1.0, 1.0], subjectivity[0.0, 0.1])
	sentiment = getSentiment(ele[0])
	if sentiment is None:
		continue
	p = sentiment.polarity
	s = sentiment.subjectivity
	if p < 0 and s < 0.5:
		suit1.append(ele)
	elif p < 0 and s >= 0.5:
		suit2.append(ele)
	elif p >= 0 and s < 0.5:
		suit3.append(ele)
	elif p >= 0 and s >= 0.5:
		suit4.append(ele)
	# time.sleep(random.randint(20, 30))

print(len(suit1))
print(suit1)

print(len(suit2))
print(suit2)

print(len(suit3))
print(suit3)

print(len(suit4))
print(suit4)
	