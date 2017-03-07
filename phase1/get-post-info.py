from bs4 import BeautifulSoup
import json
import re
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

def get_post_info(url):
	#get data
	html_doc = urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	individual_link = soup.find_all("div", {"class": "TopicPost"}) # find profile link
	
	#process data
	return_dict = {}
	for item in individual_link:
		post_information = json.loads(item['data-topic-post'])
		post_id = post_information['id']
		user_name = post_information['author']['name']
		#finding the CORRECT user id
		user_id_target = soup.find("a", {"class":"Author-name--profileLink"})
		user_id = user_id_target['href'].split("/")[-4]
		upvote = post_information['rank']['voteUp']
		downvote = post_information['rank']['voteDown']
		totalvote = int(upvote) - int(downvote)
		post_count = 1
		
		#reply by which user
		# reply_list = []
		try:
			quote_info = item.find("blockquote")
			reply_by = quote_info['data-quote']
		except:
			reply_by = 'None'
		# reply_list.append(reply_by)

		#post content
		post = item.find("div", {"class": "TopicPost-bodyContent"})
		post_text = post.text
		
		#summarize return
		return_dict[post_id] = {'user_name': user_name, 'user_id': user_id, 'upvote': upvote, 'downvote': downvote, 'totalvote': totalvote, 'post_count': post_count, 'reply_by': reply_by, 'post_text': post_text}
	return(return_dict)

def main():
	return_list = []
	n = 0
	with open('post_info.json', 'w') as f:
		for url in url_list:
			n += 1
			print("page#:", n)
			try:
				new_info = get_post_info(url)
				return_list.append(new_info)
			except:
				pass
		json.dump(return_list, f, indent=2, ensure_ascii=False)
	f.close()

if __name__ == '__main__':
	# get_post_info("https://us.battle.net/forums/en/sc2/topic/20753229703")
	main()


