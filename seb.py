import requests
import bs4
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as bsp
from difflib import SequenceMatcher
import xlrd

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

base_url = 'http://search2.chiasenhac.vn/search.php?s='
page_url = '&page='

def get_url(song_name, artist_name):
	search_name = song_name
	search_name.replace(" ", "+")
	base_search = base_url + search_name + page_url
	current_page = '1'
		
	best_match = 0
	for pages in range(3):
		search_url = base_search + current_page
		int_page=int(current_page)
		int_page = int_page + 1
		current_page = str(int_page)
		search_req = requests.get(search_url)

		search_soup = bsp(search_req.text, 'lxml')
		for page_list in search_soup.find_all('div', {"class":"tenbh"}):
			song_detail = page_list.text
			print(song_detail)
			name_rat = similar(song_detail.lower(), song_name)
			art_rat = similar(song_detail.lower(), artist_name)
			current_match = (name_rat + art_rat)/2
			print(best_match)
			if current_match > best_match:
				hold_list = page_list
				best_match = current_match
			print(hold_list.text)	
		
	for song_url in hold_list.find_all('a', href=True):
		print(song_url['href'])
		play_url = song_url['href']


	play_req = requests.get(play_url)

	play_soup = bsp(play_req.text,'lxml')

	i = 0

	for d_tab in play_soup.find_all('a', {"target":"_blank"}):
		d_url = d_tab['href']
		break

	print(d_url)

	d_req = requests.get(d_url)

	d_soup = bsp(d_req.text, 'lxml')

	flac = 0
	m4a = 0
	d = 0
	for d_qual in d_soup.find_all('a', href=True):
		if d_qual['href'].endswith("[Lossless_FLAC].flac"):
			name = d_qual['href'].split('/')[-1]
			down = d_qual['href']
			print(down)
			print(name)
			flac = 1
			m4a = 1
			d =1
			return(down, name)
			break

	if flac == 0:
		for d_qual in d_soup.find_all('a', href=True):
			if d_qual['href'].endswith("[500kbps_M4A].m4a"):
				name = d_qual['href'].split('/')[-1]
				down = d_qual['href']
				print(down)
				print(name)
				m4a = 1
				d = 1
				return(down, name)
				break



	if m4a == 0:
		for d_qual in d_soup.find_all('a', href=True):
			if d_qual['href'].endswith("[320kbps_MP3].mp3"):
				name = d_qual['href'].split('/')[-1]
				down = d_qual['href']
				print(down)
				print(name)	
				m4a = 1
				d = 1
				return(down, name)
				break
	if d != 1:
		return("none", "none")	

def download(down, name):
	r = requests.get(down, stream = True)
	 
	with open(name,"wb") as song:
	    for chunk in r.iter_content(chunk_size=1024):
	 
	         # writing one chunk at a time to pdf file
	        if chunk:
	             song.write(chunk)

loc = ("list.xlsx")

ws = xlrd.open_workbook(loc)
sheet = ws.sheet_by_index(0)

l = 1
for z in range(263):
	download_url, na = get_url(sheet.cell_value(l, 0), sheet.cell_value(l, 1))
	print(sheet.cell_value(l,0))
	print(sheet.cell_value(l,1))
	if download_url != "none":
		download(download_url, na)
		text_file = open("Output.txt", "a+")
		text_file.write(sheet.cell_value(l, 0))
		text_file.write("\n")
		text_file.close()

	if download_url == "none":
		text_file = open("UnDone.txt", "a+")
		text_file.write(sheet.cell_value(l, 0))
		text_file.write("\n")
		text_file.close()
	l = l + 1
