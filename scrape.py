import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.sparknotes.com/lit/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
soup = soup.findAll('h3', {'class': 'letter-list__filter-title'})

urllist = []

for s in soup:
	found = s.findAll('a')
	for ele in found:
		urllist.append(ele.get('href'))
		
themepath = 'themestext'

with open(themepath, 'w') as f:
	for url in urllist:		
		url = 'https://www.sparknotes.com{}themes/'.format(url)
		soup = BeautifulSoup(requests.get(url).text, 'html.parser')
		soup = soup.findAll('div', {'class': 'studyGuideText'})
		for s in soup:
			found = s.findAll('h3')
			for ele in found:
				f.write('{}\n'.format(ele.text))

	