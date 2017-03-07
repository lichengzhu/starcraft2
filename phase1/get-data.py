from bs4 import BeautifulSoup
import json
try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen

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

		if individual_name in profile_dict: #check if the person already exisits
			continue
		else:
			profile_dict[individual_name] = individual_id

	return(profile_dict)

def get_next_page(url):
	#get data
	html_doc = urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')

	#process data
	#if this is a page under specific topic
	if "topic" in url:
		next_page = soup.find("a", {"class": "Pagination-button--next"}) #find "next" page button under a specific topic
		
		#filter url so that there will be no "https://us.battle.net//forums/en/sc2/topic/20753099025?page=2?page=3"
		rooturl = url.split("?")[0]

		try:
			next_page_link = str(rooturl) + str(next_page['href'])
			return(next_page_link)
		except:
			return("End of topic page")
	#if the page is under the general dicussion sectio of the forum
	else:
		next_page = soup.find("a", {"class": "Pagination-button--next"}) #open applies to page2 and beyond under the general discussion thread
		
		#filter url so that there will be no "https://us.battle.net/forums/en/sc2/40568/?page=2?page=3"
		rooturl = url.split("?")[0]

		try:
			next_page_link = str(rooturl) + str(next_page['href'])
			return(next_page_link)
		except:
			print("End of general discussion page")
			exit()

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

def main():
	""" first page """
	first_page_url = "https://us.battle.net/forums/en/sc2/40568/" #first page of "General Discussion" of SC2
	name_id_dict = {} #initializing the dict that will be returned

	print(first_page_url)
	topic_list = get_topic(first_page_url)

	for k, v in topic_list.items():
		topic_url = v['topic_url']
		
		while topic_url != "End of topic page":
			print(topic_url)
			name_id_dict.update(get_name_id(topic_url))
			topic_url = get_next_page(topic_url) # get next page of topic

	#getting to the 2nd page of the general discussion
	page_url = first_page_url + "?page=2"

	

	""" second page and beyond """
	#finding names/id from specific topics
	while page_url != "End of general discussion page":
		print(page_url)
		topic_list = get_topic(page_url)


		#for topics
		for k, v in topic_list.items():
			topic_url = v['topic_url']

			while topic_url != "End of topic page":
				print(topic_url)
				name_id_dict.update(get_name_id(topic_url))
				topic_url = get_next_page(topic_url) # get next page of topic

		print(name_id_dict)

		#getting to next page of the general discussion
		page_url = get_next_page(page_url)

	return(name_id_dict)




if __name__ == '__main__':
	# get_name_id("https://us.battle.net/forums/en/sc2/topic/20753318331?page=2")
	# get_next_page("https://us.battle.net/forums/en/sc2/40568/")
	# get_next_page("https://us.battle.net/forums/en/sc2/topic/20753318331?")
	# get_next_page("https://us.battle.net/forums/en/sc2/topic/20753318331?page=2")
	# get_topic("https://us.battle.net/forums/en/sc2/40568/")
	main()
