from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import time
import urllib.request

sentimentspath = 'sentimentstext'

def getSentiment(word):
	with open(sentimentspath, 'a') as f:
		print(word)
		url = 'https://www.sparknotes.com/search?q={}'.format(word)
		response = requests.get(url)

		soup = BeautifulSoup(response.text, 'html.parser')
		soup = soup.find('div', {'class': 'search-result-block'})
		href = soup.find('a').get('href')
		
		result_url = 'https://www.sparknotes.com{}'.format(href)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		found = soup.find('p')
		
		result = TextBlob(found.text).sentiment
		if result is None:
			print("{} failed".format(word))
		else:
			f.write('{} {}\n'.format(word, result))
		return result

	