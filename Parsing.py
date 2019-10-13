# Данный скрипт осуществляет парсинг Avito.
# Получает заголовок объявления, цену, дату/время, ссылку.

# Необходимо добавить:
# проверку с заданными промежутками времени;
# запись результата в файл Excel/SQL;
# добавление в результаты при появлении новых объявлений;
# оповещение на Email о новых объявлениях.

import requests
from bs4 import BeautifulSoup
import re																				# регулярные выражения
import openpyxl																			# библиотека для Excel

def get_html(url):
	r = requests.get(url)
	return r.text
	
def get_total_pages(html):
	index_pages = 0																		# начальный индекс
	soup = BeautifulSoup(html, 'lxml')
																						# получаем список
	pages = soup.find_all ('div', attrs = {'class': 'description item_table-description'})
	
	pages_len = len(pages)																# кол-во элементов в списке
	print(str(pages_len) + '\n')
	
	try:
		# читаем excel-файл
		wb = openpyxl.load_workbook('base.xlsx')
	except IOError:
		# создаем новый excel-файл
		wb = openpyxl.Workbook()
		wb.create_sheet(title = 'Объявления', index = 0)
	
	# получаем лист, с которым будем работать
	sheet = wb['Объявления']
	
	while (index_pages != pages_len):													# цикл обхода списка
		pages1 = pages[index_pages]														# получаем элемент списка

		title =  pages1.find ('span', attrs = {'itemprop': 'name'})						# достаем тег "name"
		price =  pages1.find ('span', attrs = {'class': 'price'})						# достаем тег "price"
		date =  pages1.find ('div', attrs = {'class': 'item-date'})						# достаем тег "item-date"
		href = pages1.find('a', class_ = 'item-description-title-link').get('href')		# достаем ссылку
	
		title = str(title.get_text())													# достаем заголовок
		price = str(price.get_text())													# достаем цену
		date = str(date.get_text())														# достаем дату
		href = "http:/" + str(href)
		
		title = re.sub("^\s+|\n|\r|\s+$", '', title)									# удаляем лишние символы
		price = re.sub("^\s+|\n|\r|₽|\s+$", '', price)									# удаляем лишние символы
		date = re.sub("^\s+|\n|\r|\s+$", '', date)										# удаляем лишние символы

		print(title)
		print(price)
		print(date)
		print(href + '\n')
		
		# запись в файл
		sheet.append([title, price, date, href])
		
		index_pages += 1																# индекс следующего элемента
	
	# сохраняем файл
	wb.save('base.xlsx')	
	
def main():
	url = "https://www.avito.ru/ekaterinburg/avtomobili/s_probegom/inomarki/mehanika/benzin/levyy_rul/ne_bolee_dvuh/ne_bityy?cd=1&pmax=350000&pmin=150000&radius=200&user=1&f=188_901b20303"
	
	html = get_html(url)
	get_total_pages(html)

if __name__ == '__main__':
	main()
