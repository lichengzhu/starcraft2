import urllib.request
import urllib.parse
import json
from collections import Counter

def find_matches(user_id, user_name):
	"""This is a function using Blizzard's API to find game match information for specific user"""
	apikey = "b4h5k62f9377d9dns3pmn9b2nraevhb6"
	user_name = str(user_name)
	user_id = str(user_id)
	base_url = "https://us.api.battle.net/sc2/profile/{}/1/{}/matches?locale=en_US&apikey={}".format(user_id, user_name, apikey)

	req = urllib.request.Request(base_url)
	try:
		matches = urllib.request.urlopen(req).read().decode()
		matches = list(json.loads(matches).values())[0] #converting into a list of matches
		
		match_number = len(matches) #finding number of matches
		match_results = Counter([match['decision'] for match in matches]) #finding all match results
		try:
			loss_count = match_results['LOSS']
			win_count = match_results['WIN']
			# win_rate = str((win_count / loss_count) * 100)[:5]+"%"
			win_rate = win_count / (loss_count + win_count)
		except:
			win_rate = 0
		return(match_number, win_rate)
	except:
		pass


# if __name__ == '__main__':
	# find_matches("7023839345", "zappy")