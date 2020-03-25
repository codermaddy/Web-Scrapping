from urllib.request import urlopen
from bs4 import BeautifulSoup
from newspaper import Article
import nltk
import csv

nltk.download('punkt')

main_news_file = open('main_news.csv', 'w')
sub_news_file = open('sub_news.csv', 'w')

field_names = ['Title', 'URL', 'Datetime', 'Summary', 'Key Sentences']

main_news_writer = csv.DictWriter(main_news_file, field_names)
sub_news_writer = csv.DictWriter(sub_news_file, field_names)

url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen'
leading_news_url = 'https://news.google.com'

keywords = ['surge', 'acquisitions', 'IPO']

connection = urlopen(url)

response = connection.read().decode('utf-8') 

soup = BeautifulSoup(response, 'html.parser')

section = soup.find('div', {'class' : 'lBwEZb BL5WZb GndZbb'})

main_news_writer.writeheader()
sub_news_writer.writeheader()

for news in list(section.children)[:10]:
	headings = news.find_all('a', {'class': 'DY5T1d'})
	
	main_news_heading = headings[0].string
	main_news_url = leading_news_url + headings[0]['href'][1:]
	
	try:
		article = Article(main_news_url)
		article.download()
		article.parse()
		article.nlp()
		key_sentences = ''
		for sentence in article.text.split('\n'):
			for word in keywords:
				if word in sentence:
					key_sentences = key_sentences + '\n' + sentence
					break
		main_news_writer.writerow({'Title': main_news_heading, 'URL': main_news_url, 'Datetime': article.publish_date, 'Summary': article.summary, 'Key Sentences': key_sentences})

	except:
		pass
	for sub_news in headings[1:]:
		sub_news_heading = sub_news.string
		sub_news_url = leading_news_url + sub_news['href'][1:]

		try:
			article = Article(sub_news_url)
			article.download()
			article.parse()
			article.nlp()
			key_sentences = ''
			for sentence in article.text.split('\n'):
				for word in keywords:
					if word in sentence:
						key_sentences = key_sentences + '\n' + sentence
						break
			sub_news_writer.writerow({'Title': sub_news_heading, 'URL': sub_news_url, 'Datetime': article.publish_date, 'Summary': article.summary, 'Key Sentences': key_sentences})
		
		except:
			pass

main_news_file.close()
sub_news_file.close()
connection.close() 
