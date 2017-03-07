from bs4 import BeautifulSoup
import json
try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen

url_list = []
with open('topic-url.txt', 'r') as file:
	data = json.loads(file.read())
	urls = data.values()
	# print(url_list, len(url_list))
	for i in urls:
		url_list.append(i['topic_url'])

# print(url_list, len(url_list))

def get_name_id(url):
	#get data
	html_doc = urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	individual_link = soup.find_all("a", {"class": "Author-name--profileLink"}) # find profile link
	# individual_link_post = soup.find_all("a", {"class": "Author-posts"}) #find post number
	#process data
	profile_dict = {} #initialize
	for item in individual_link:
		individual_profile_link = item['href']
		individual_name = individual_profile_link.split('/')[-2] #get the name
		individual_id = individual_profile_link.split('/')[-4] #get the id
		#check if the person already exisits
		if individual_name in profile_dict:
			continue
		else:
			profile_dict[individual_name] = individual_id
	return(profile_dict)

name_id_dict = {}
n = 0
with open('name-id.json', 'w') as f:
	for url in url_list:
		n += 1
		print("page#:", n)
		try:
			new_info = get_name_id(url)
			name_id_dict.update(new_info)
		except:
			pass
	json.dump(name_id_dict, f, indent=2)
f.close()