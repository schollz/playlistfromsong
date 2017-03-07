from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.last.fm/search?q=the+beatles+let+it+be')
soup = BeautifulSoup(r.content, 'html.parser')
chartlist = soup.find_all('table',class_='chartlist')[0]
for link in chartlist.find_all('a',class_='link-block-target'):
	print(link)