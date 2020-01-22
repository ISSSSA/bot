from bs4 import BeautifulSoup
import requests
import telebot
import time
top_players = ['s1mple','device','ZywOo','ELIGE','Magisk','NAF','electronic','Brehze','Twistzz','ropz','NiKo','woxic','sergej','Xyp9x','jks','dupreeh','KRIMZ','CeRq','Brollan','Ethan','kennys','Jame','xsepower']
TOKEN = ''
bot = telebot.TeleBot(TOKEN,True,4)
@bot.message_handler(commands=['start','help'])
def command_start(message):
	bot.reply_to(message,'Дайте мне ссылку на hltv.org\n\nhttps://www.meme-arsenal.com/memes/4c0d4105d3e625f5773b32c14ef79192.jpg')
@bot.message_handler(regexp='((https?):((//)|(\\\\))+([hltv.org](#!)?)*)')
def command_url(message):
	# получаем страницу для парсинга
	url_list = message.text.split(' ')
	url = url_list[len(url_list)-1]
	picture_url = ' '
	print(message.text)
	try:
		score_st = 1
		score_nd = 1
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		soup.prettify()
		# получаем названия команд
		team1 = soup.find_all(class_='teamName')[2].get_text()
		team2 = soup.find_all(class_='teamName')[1].get_text()
		# получаем статистику в матчах 1 на 1
		try:
			t1_1v1_s = int(soup.find_all('div',class_='right-border')[0].select('div')[0].get_text())
			t2_1v1_s = int(soup.find_all('div',class_='left-border')[0].select('div')[0].get_text())
			score_st+=t1_1v1_s/10
			score_nd+=t2_1v1_s/10
		except IndexError:
			pass
		#получаем 2 последних матча 1 команды и их результаты 
		try:
			command1_st = soup.find_all('a',class_='text-ellipsis')[2].get_text()
			command1_res_st = soup.find_all('td',class_='result')[0].get_text()
			command1_st_w_l = soup.find_all('td',class_='result')[0].attrs["class"][2]
			if command1_st_w_l =='lost':
				score_st+=0
			else:
				score_st+=0.6
		except IndexError:
			command1_st = ' '
			command1_res_st = ' '
		try:
			command2_st = soup.find_all('a',class_='text-ellipsis')[3].get_text()
			command2_res_st = soup.find_all('td',class_='result')[1].get_text()
			command2_st_w_l = soup.find_all('td',class_='result')[1].attrs["class"][2]
			if command2_st_w_l == 'lost':
				score_st+=0
			else:
				score_st+=0.5
		except IndexError:
			command2_st = ' '
			command2_res_st = ' '
		# получаем 2 последних матча 2 команды и их результаты
		try:
			command1_nd = soup.find_all('a',class_='text-ellipsis')[7].get_text()
			command1_res_nd = soup.find_all('td',class_='result')[5].get_text()
			command1_nd_w_l = soup.find_all('td',class_='result')[5].attrs["class"][2]
			if command1_nd_w_l == 'lost':
				score_nd+=0
			else:
				score_nd+=0.6
		except IndexError:
			command1_nd = ' '
			command1_res_nd = ' '
		try:
			command2_nd = soup.find_all('a',class_='text-ellipsis')[8].get_text()
			command2_res_nd = soup.find_all('td',class_='result')[6].get_text()
			command2_nd_w_l = soup.find_all('td',class_='result')[6].attrs["class"][2]
			if command2_nd_w_l == 'lost':
				score_nd+=0
			else:
				score_nd+=0.5
		except IndexError:
			command2_nd = ' '
			command2_res_nd = ' '
		# получаем процентное соотношение вероятности на хлтв
		try:
			perc_1 = soup.find_all('div',class_='percentage')[0].get_text().split('%')[0]
			perc_2 = soup.find_all('div',class_='percentage')[1].get_text().split('%')[0]
		except IndexError:
			perc_1 = 50
			perc_2 = 50
		#получаем страницы команд и список игроков попутно проверяя на наличие в топе
		team1_url_p = soup.find_all('div',class_='team1-gradient')[0].select('a')[0].attrs["href"]
		team2_url_p = soup.find_all('div',class_='team2-gradient')[0].select('a')[0].attrs["href"]
		team1_url = 'https://www.hltv.org/' + team1_url_p
		team2_url = 'https://www.hltv.org/' + team2_url_p
		team1_page = requests.get(team1_url)
		team2_page = requests.get(team2_url)
		team1_soup = BeautifulSoup(team1_page.text,'html.parser')
		team2_soup = BeautifulSoup(team2_page.text,'html.parser')
		team1_soup.prettify()
		try:
			team1_num = int(team1_soup.find_all('div','profile-team-stat')[0].select('span')[0].select('a')[0].get_text().split('#')[1])
		except IndexError:
			team1_num = 300
		players_1 = ''
		players_2 = ''
		players_1_l = []
		players_2_l = []
		players_1_list = team1_soup.find_all('a',class_='col-custom')
		for i in players_1_list:
			players_1=players_1 + i.attrs["title"] + ' '
			if i in top_players:
				score_st+=0.5
			players_1_l.append(i.attrs["title"])
		team2_soup.prettify()
		#получаем место в рейтинге у команд
		try:
			team2_num = int(team2_soup.find_all('div','profile-team-stat')[0].select('span')[0].select('a')[0].get_text().split('#')[1])
		except IndexError:
			team2_num = 300
		players_2_list = team2_soup.find_all('a',class_='col-custom')
		for i in players_2_list:
			players_2=players_2 + i.attrs["title"] + ' '
			if i in top_players:
				score_nd+=0.5
			players_2_l.append(i.attrs["title"])
		#подводим подсчет очков у команды
		try:
			if team1_num < team2_num:
				score_st+=0.4
			elif team1_num > team2_num:
				score_nd+=0.4
			score_st += round(float(perc_1)/float(perc_2))
			score_nd += round(float(perc_2)/float(perc_1))
			total_score = score_nd + score_st
			p_score_st = str(round(score_st/total_score*100,1))+'%'
			p_score_nd = str(round(score_nd/total_score*100,1))+'%'
		except ArithmeticError:
			reply_to(message,'Что-то пошло не так попробуйте снова')
		#получаем картинку для вероятной команды победителя
		try:
			if score_st > score_nd:
				picture_url = 'https://www.hltv.org/galleries?team='+team1_url.split('/')[5]
			else:
				picture_url = 'https://www.hltv.org/galleries?team='+team2_url.split('/')[5]
			gallery_page = requests.get(picture_url)
			gallery_soup = BeautifulSoup(gallery_page.text,'html.parser')
			gallery_soup.prettify()
			picture = gallery_soup.find_all('div',class_='preview-holder')[0].select('img')[0].attrs['src']
		except IndexError:
			picture ='https://memepedia.ru/wp-content/uploads/2019/01/neskvik-s-pivom-mem.jpg'
		#собираем ответ для телеграма из частей
		players = team1 + ':\n'+players_1+'\n\n'+team2+':\n'+players_2
		team = team1+'(#'+str(team1_num)+')' + ' vs ' + team2 +'(#'+str(team2_num)+')'
		procent = team1 + ':\n'+ p_score_st + '\n'+team2+':\n'+p_score_nd
		ab1 = 'Последние игры ' + team1+ ' были с: \n' + command1_st + ' ' + command1_res_st + '\n' + command2_st + ' ' +command2_res_st
		ab2 ='Последние игры ' + team2+ ' были с: \n' + command1_nd + ' ' + command1_res_nd + '\n' + command2_nd + ' ' +command2_res_nd
		answer = team + '\n\n'+players + '\n\n' + ab1 + '\n\n'+ab2 +'\n\n' +procent+ '\n\n'+ picture
		score_nd = 1
		score_st = 1
		#отвечаем в телеграме
		bot.reply_to(message, answer)
	except IndexError:
		bot.reply_to(message,'Лебовски,мне нужна только ссылка на матч на hltv.org\n\nhttps://i.vimeocdn.com/video/751161691_1280x720.jpg')
	except OSError:
		bot.reply_to(message,'Лебовски,мне нужна только ссылка на матч на hltv.org\n\nhttps://i.vimeocdn.com/video/751161691_1280x720.jpg')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	bot.reply_to(message,'Дурак, ссылка нужна \n\n https://i1.sndcdn.com/artworks-000556944858-79zn1s-t500x500.jpg')
	print(message.text)
bot.polling()




