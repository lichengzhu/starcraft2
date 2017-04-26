import datetime
import json
import sqlite3 as sqlite
import urllib.request
import time
# try:
# 	# For Python 3.0 and later
# 	from urllib.request import urlopen
# except ImportError:
# 	# Fall back to Python 2's urllib2
# 	from urllib2 import urlopen


"""
fetching user_name and user_id from post_info table
"""
conn = sqlite.connect('starcraft_project.db')
db = conn.cursor()
db.execute('SELECT DISTINCT user_name, user_id FROM post_info')
name_list = db.fetchall()



"""
setting up the database for match_info table
"""
db.execute('DROP TABLE IF EXISTS match_info')
db.execute('CREATE TABLE match_info (user_name TEXT, user_id INT, win INT, loss INT, bail INT, match_date TEXT)')





"""
this function pulls match data from Blizzard API if given user id and user name
"""
def get_matches(user_id, user_name):
	apikey = "b4h5k62f9377d9dns3pmn9b2nraevhb6"
	user_name = str(user_name)
	user_id = str(user_id)
	base_url = "https://us.api.battle.net/sc2/profile/{}/1/{}/matches?locale=en_US&apikey={}".format(user_id, user_name, apikey)

	req = urllib.request.Request(base_url)
	try:
		matches = urllib.request.urlopen(req).read().decode()
		matches = list(json.loads(matches).values())[0] #converting into a list of matches
		
		for match in matches:
			# fetching the result of the match
			if match['decision'] == 'WIN':
				win = 1
				loss = 0
				bail = 0
			if match['decision'] == 'LOSS':
				win = 0
				loss = 1
				bail = 0
			if match['decision'] == 'BAILER':
				win = 0
				loss = 0
				bail = 1
			# converting time from Linux time stamp to Python string
			time_stamp = match['date']
			match_date = datetime.datetime.fromtimestamp(int(time_stamp)).strftime('%m/%d/%Y')

			# writting to the database
			insertion = [user_name, int(user_id), win, loss, bail, str(match_date)]
			db.execute('INSERT INTO match_info VALUES(?, ?, ?, ?, ?, ?)', insertion)
	except:
		pass




"""
this function iterate through all users found via web parsing and get their match data
"""
def main():
	user_count = len(name_list)
	n = 0
	for i in name_list:
		n += 1
		user_name = i[0]
		user_id = i[1]
		print("match-user:", user_name, user_id, "progress:", (n/user_count))
		try:
			get_matches(user_id, user_name)
			# time.sleep(0.101)
		except:
			pass

	conn.commit()
	conn.close()

if __name__ == '__main__':
	# get_matches("5753050", "Iskeletor")
	main()