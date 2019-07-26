from collections import Counter
import itertools
from nltk.corpus import wordnet
import random
import re
import spacy
from textblob import TextBlob

countpath = 'theresttext'
regex = r'\(\'([a-z]+)\', ([0-9]+)\)'

wordCounter = Counter()

with open(countpath, 'r') as f:
	line = f.readline()
	foundall = re.findall(regex, line)
	for match in foundall:
		wordCounter[match[0]] = int(match[1])

sentimentspath = 'sentimentstext'
regex = r'([a-z]+) Sentiment\(polarity=(-?[0-9]+\.[0-9]+), subjectivity=(-?[0-9]+\.[0-9]+)\)'

suit1 = [] # neg polarity # <0.5 subjectivity
suit2 = [] # neg polarity # >=0.5 subjectivity
suit3 = [] # pos polarity # <0.5 subjectivity
suit4 = [] # pos polarity # >=0.5 subjectivity

with open(sentimentspath, 'r') as f:
	line = f.readline()
	while line:
		m = re.match(regex, line)
		(word, polarity, subjectivity) = m.groups()
		p = float(polarity)
		s = float(subjectivity)
		
		if p < 0 and s < 0.5:
			suit1.append(word)
		elif p < 0 and s >= 0.5:
			suit2.append(word)
		elif p >= 0 and s >= 0.5:
			suit3.append(word)
		elif p >= 0 and s < 0.5:
			suit4.append(word)
		
		line = f.readline()
		
print(len(suit1))
print(suit1)

print(len(suit2))
print(suit2)

print(len(suit3))
print(suit3)

print(len(suit4))
print(suit4)

# TODO HERE
# perhaps segregate the suits by element instead of sentiment? 
# use sentiment to order things, perhaps????? 

earthsyns = wordnet.synsets('earth', pos = wordnet.NOUN)
watersyns = wordnet.synsets('water', pos = wordnet.NOUN)
airsyns = wordnet.synsets('air', pos = wordnet.NOUN)
firesyns = wordnet.synsets('fire', pos = wordnet.NOUN)

elesyns = [earthsyns, watersyns, airsyns, firesyns]
suits = [suit1, suit2, suit3, suit4]

for suit in suits:
	# afinities for earth, water, air, and fire, in order
	sumAfinities = [0, 0, 0, 0]

	for i, word in enumerate(suit):
		if i%10 == 0:
			print(i)
		for syn1 in wordnet.synsets(word, pos = wordnet.NOUN):
			for i, ele in enumerate(elesyns):
				maxMatch = 0
				for synE in ele:
					newMatch = syn1.path_similarity(synE) 
					if newMatch > maxMatch:
						maxMatch = newMatch
				sumAfinities[i] += maxMatch*wordCounter[word]

	sumAfinities = [x/len(suit) for x in sumAfinities]
	print(sumAfinities)
	