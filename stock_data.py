from urllib.request import urlopen
from bs4 import BeautifulSoup
from sched import scheduler
from time import time, sleep
from csv import DictWriter

url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9'

sc = scheduler(time, sleep)

field_names = ['Company Name', 'Industry', 'Last Price', 'Change', '%Chg', 'Mkt Cap']

PERC_CHNG_IDX = 4
COMP_NAME_IDX = 0
CHNG_MAGNITUDE = 0.5
CHECK_INTERVAL = 4  	#4*30sec = 2 mins

data = []

counter = 0

def check_change(data_recent):
	if len(data):
		print("CHECKING FOR CHANGE!")
		for i in range(len(data)):
			if abs(float(data_recent[i][PERC_CHNG_IDX]) - float(data[i][PERC_CHNG_IDX])) >= CHNG_MAGNITUDE:
				print("ATTENTION!", end = ' ')
				print("Change of %f in %s" %(float(data_recent[i][PERC_CHNG_IDX]) - float(data[i][PERC_CHNG_IDX]), data_recent[i][COMP_NAME_IDX]))
		print("-."*20) 

def read_data():

	global counter
	global data

	connection = urlopen(url)

	response = connection.read()
	response = response.decode('utf-8')

	soup = BeautifulSoup(response, 'html.parser')

	section = soup.find('table', {'class': 'tbldata14 bdrtpg'})

	#print(time())

	data_recent = []

	for row in section.find_all('tr')[1:]:

		row_content = []

		for idx, column in enumerate(row.find_all('td', {'class': 'brdrgtgry'})):

			if idx < 2:
				tmp = column.find('a').string
			else:
				tmp = column.string

			row_content.append(tmp)

		data_recent.append(row_content)

	connection.close()

	#print(counter)

	if not len(data):
		for row in data_recent:
			print(row)

	if counter == 0:
		check_change(data_recent)
		data = data_recent
	
	counter = (counter+1)%CHECK_INTERVAL
	
	sc.enter(30, 1, read_data)

sc.enter(0, 1, read_data)
sc.run()