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
therest = list(lemmaCounter.most_common(n))[22:]

print(n)
print(trumps)

trumpspath = 'trumpstext'

# with open(trumpspath, 'w') as f:
	# f.write('{}'.format(trumps))
	
therestpath = 'theresttext'
with open(therestpath, 'a') as f:
	for lemma in therest:
		f.write('{}'.format(lemma))
	
	
