"""
'''
To ssh into flux:
ssh zlicheng@flux-hadoop-login.arc-ts.umich.edu

To load extra packages:
module load python-anaconda2/latest
module load python-anaconda3/latest

To run interactive shell:
pyspark --master yarn-client --queue si618w17

To run on Fladoop cluster:
spark-submit --master yarn-client --queue si618w17 --num-executors 30 --executor-memory 4g --executor-cores 4 project1-spark.py

To get results:
hadoop fs -getmerge name_id_output name_id_output.tsv

******* To upload a file to HDFS: *******
hdfs dfs -put topic-url.txt /user/zlicheng/

'''
"3123316760": {"topic_url": "https://us.battle.net//forums/en/sc2/topic/3123316760", "topic_title": "help"}
"2325682744": {"topic_url": "https://us.battle.net//forums/en/sc2/topic/2325682744", "topic_title": "chat channel auto join"}
"""

import urllib.request
import urllib.parse
import json
from collections import Counter
from get_request import find_matches
import csv


def project1_find_post_count():
	meta_data = json.loads(open('post_info.json', 'r').read())

	#finding post count
	poster_list = []
	for post in meta_data: #number control
		for k, v in post.items():
			poster_list.append(v['user_name'])

	post_count = Counter(poster_list)
	
	#writing
	output_file = open('post_count.csv', 'w')
	for k, v in post_count.items():
		output_file.write(str(k))
		output_file.write(",")
		output_file.write(str(v))
		output_file.write("\n")
	output_file.close()

def project1_get_match_data():
	with open('name-id.json', 'r') as file:
		namelist = json.loads(file.read())
		
		output_file = open('match_data.csv', 'w')
		
		n = 0
		for user_name, user_id in namelist.items():
			n += 1
			if n < 7349823749329839: #control flow
				try:
					match_number, win_rate = find_matches(user_id, user_name)
					output_file.write(str(user_name))
					output_file.write(',')
					output_file.write(str(match_number))
					output_file.write(',')
					output_file.write(str(win_rate))
					output_file.write('\n')
					print("player ", n)
				except:
					print("bad request")
					pass
			else:
				output_file.close()
				exit()

def project1_merge_visualize():
	#get match and post data
	reader = csv.reader(open('match_data.csv', 'r'))
	match_dict = {}
	for row in reader:
		user_name = row[0]
		win_rate = row[2]
		match_dict[user_name] = win_rate
	# print(match_dict)

	reader = csv.reader(open('post_count.csv', 'r'))
	post_count_dict = {}
	for row in reader:
		user_name = row[0]
		post_count = row[1]
		post_count_dict[user_name] = post_count
	# print(post_count_dict, type(post_count_dict), len(post_count_dict))

	#merge them by user_id
	merged_dict = {}
	for user_name, win_rate in match_dict.items():
		# print(user_name, win_rate)
		post_count = post_count_dict.get(user_name, None)
		# print(post_count)
		# print(user_name, post_count)
		if post_count:
			merged_dict[post_count] = win_rate
	# print(len(merged_dict))

	#export as a csv file for visualization
	with open('project1_visualization.csv', 'w') as f:
		for post_count, win_rate in merged_dict.items():
			f.write(post_count)
			f.write(',')
			f.write(win_rate)
			f.write('\n')
	f.close()

if __name__ == '__main__':
	# project1_find_post_count()
	# project1_get_match_data()
	project1_merge_visualize()
