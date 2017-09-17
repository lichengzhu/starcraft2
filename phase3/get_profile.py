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
setting up the database for profile_info table
"""
db.execute('DROP TABLE IF EXISTS profile_info')
db.execute('CREATE TABLE profile_info (user_name TEXT, user_id INT, prime_race TEXT, highest_rank TEXT, campaign_difficulty TEXT)')





"""
this function pulls profile data from Blizzard API if given user id and user name
"""
def get_profile(user_id, user_name):
	apikey = "b4h5k62f9377d9dns3pmn9b2nraevhb6"
	user_name = str(user_name)
	user_id = str(user_id)
	base_url = "https://us.api.battle.net/sc2/profile/{}/1/{}/?locale=en_US&apikey={}".format(user_id, user_name, apikey)

	req = urllib.request.Request(base_url)
	try:
		# requesting data
		profile_meta = urllib.request.urlopen(req).read().decode()
		profile = json.loads(profile_meta) #converting into a dictionary
		
		# parsing data
		prime_race = profile['career']['primaryRace']
		highest_rank = profile['career']['highest1v1Rank']
		if profile['campaign'] == {}:
			campaign_difficulty = "NA"
		else:
			campaign_difficulty = profile['campaign']

		# writting to the database
		insertion = [user_name, int(user_id), str(prime_race), str(highest_rank), str(campaign_difficulty)]
		db.execute('INSERT INTO profile_info VALUES(?, ?, ?, ?, ?)', insertion)
	except:
		pass




"""
this function iterate through all users found via web parsing and get their profile data
"""
def main():
	user_count = len(name_list)
	n = 0
	for i in name_list:
		n += 1
		user_name = i[0]
		user_id = i[1]
		print("profile-user:", user_name, user_id, "progress:", (n/user_count))
		try:
			get_profile(user_id, user_name)
			# time.sleep(0.101)
		except:
			pass

	conn.commit()
	conn.close()

if __name__ == '__main__':
	# get_profile("5753050", "Iskeletor")
	main()