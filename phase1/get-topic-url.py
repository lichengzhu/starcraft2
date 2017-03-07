from bs4 import BeautifulSoup
import json
try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen


#getting pages set up 
page_list = []
page_list.append("https://us.battle.net/forums/en/sc2/40568/")
for page in range(2, 4000):
	page_url = "https://us.battle.net/forums/en/sc2/40568/?" + "page=%s" % page
	page_list.append(page_url)
# print(type(page_list), len(page_list))


#find all topics for a specific page
def get_topic(url):
	#get data
	html_doc = urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	#getting rid of official announcement contents
	try: #only first page has official announcement section
		soup.find("div", {"data-topics-container": "sticky"}).decompose()
	except:
		pass 

	#process data
	topics = soup.find_all("a", {"class": "ForumTopic"})
	return_dic = {}
	for item in topics:
		topic_url = "https://us.battle.net" + str(item['href'])
		topic_id = topic_url.split('/')[-1]
		try:
			topic_title = item.find("span",class_="ForumTopic-title").string.strip()
		except:
			topic_title = "None title"
		return_dic[topic_id] = {'topic_url':topic_url, 'topic_title':topic_title}
	return(return_dic)

topic_dict = {}
with open('topic-url.txt', 'w') as f:
	for page in page_list:
		print(page)
		try:
			topics = get_topic(page)
			topic_dict.update(topics)
		except:
			pass
	json.dump(topic_dict, f, indent=2, ensure_ascii=False)
f.close()