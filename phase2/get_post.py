from bs4 import BeautifulSoup
import json
import re
import sqlite3 as sqlite
try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen


"""
setting up the database
"""
conn = sqlite.connect('starcraft_project.db')
db = conn.cursor()
db.execute('DROP TABLE IF EXISTS post_info')
db.execute('CREATE TABLE post_info (post_id INT, user_name TEXT, user_id INT, upvote INT, downvote INT, total_vote INT, reply_by TEXT, post_time TEXT, post_text TEXT)')



"""
getting the links for pages on the Forum
"""
url_list = []
with open('topic-url.json', 'r') as file:
	data = json.loads(file.read())
	urls = data.values()
	# print(url_list, len(url_list))
	for i in urls:
		url_list.append(i['topic_url'])



"""
this function will fetch data for each post and write them into a local database
"""
def get_post_info(url):
	html_doc = urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	individual_link = soup.find_all("div", {"class": "TopicPost"}) # find profile link
	
	for item in individual_link:
		post_information = json.loads(item['data-topic-post'])
		post_id = post_information['id']
		user_name = post_information['author']['name']
		#finding the CORRECT user id
		user_id_target = item.find("a", {"class":"Author-name--profileLink"})
		user_id = user_id_target['href'].split("/")[-4]
		upvote = post_information['rank']['voteUp']
		downvote = post_information['rank']['voteDown']
		totalvote = int(upvote) - int(downvote)
		
		#reply by which user
		# reply_list = []
		try:
			quote_info = item.find("blockquote")
			reply_by = quote_info.find("a").text
		except:
			reply_by = 'NA'
		# reply_list.append(reply_by)

		#post content
		post = item.find("div", {"class": "TopicPost-bodyContent"})
		post_text = post.text

		#post time
		post_time_meta = item.find("a", {"class": "TopicPost-timestamp"})
		post_time = str(post_time_meta['data-tooltip-content'])
		post_time = post_time.split()[0] #only keeping mm/dd/yyyy, getting rid of hh/mm AMPM
		# print(post_time)
		
		#writting data to database
		insertion = [int(post_id), user_name, int(user_id), int(upvote), int(downvote), int(totalvote), reply_by, post_time, post_text]
		db.execute('INSERT INTO post_info VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', insertion)


"""
Iterate through all pages ("topics" pages by Blizzard) and fetch data into local database
"""
def main():
	topic_count = len(url_list)
	n = 0
	for url in url_list:
		n += 1
		print("topic-page#:", n, url, "progress:", (n/topic_count))
		try:
			get_post_info(url)
		except:
			pass

	conn.commit()
	conn.close()


if __name__ == '__main__':
	# get_post_info("https://us.battle.net/forums/en/sc2/topic/20753229703")
	# get_post_info("https://us.battle.net/forums/en/sc2/topic/20753656683")
	main()