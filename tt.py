import requests
import xml.etree.cElementTree as cET
from datetime import datetime
from dateutil import parser

class Item:
	def __init__(self, title, link, pubDate):
		self.title = title
		self.link = link
		self.pubDate = pubDate
	def get_string(self):
		return "\n![" + self.title + "](" + self.link + ")\n"

def get_response(url):
	with requests.get(url, timeout = 30) as resp:
		if resp.status_code == 200:
			return resp.text
		else:
			return "fail"

def parsing_xml(xml):
	item_list = []
	try:
		xmlTree = cET.fromstring(xml)
		for obj in xmlTree.iter("item"):
			item_list.append(Item(obj.find("title").text, obj.find("link").text, obj.find("pubDate").text))
	except cET.ParseError:
		pass
	return item_list

def load_url():
	with open("url.txt", "r", encoding = "UTF-8") as file:
		url_list = file.read().splitlines()
		return url_list

def save_url(urlstring):
	with open("url.txt", "w", encoding = "UTF-8") as file:
		file.write(urlstring)

url_list = load_url()
result = ""
update_urltxt = ""

for list in url_list:
	urlstring = list.split("|")[0]
	timestring = list.split("|")[1]
	feed = get_response(urlstring)
	if feed != "fail":
		item_list = parsing_xml(feed)
		if len(item_list) > 0:
			for item_obj in item_list:
				pub_date = parser.parse(item_obj.pubDate)
				last_date = parser.parse(timestring)
				if pub_date.timestamp() > last_date.timestamp():
					result += item_obj.get_string()
					timestring = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
			update_urltxt = update_urltxt + urlstring + "|" + timestring + "\n"
		else:
			update_urltxt = update_urltxt + list + "\n"
	else:
		update_urltxt = update_urltxt + list + "\n"

save_url(update_urltxt)
print(result)
