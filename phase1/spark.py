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

import json
from pyspark import SparkContext
import re
from urllib2 import urlopen
"""try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen"""
sc = SparkContext(appName="project1-name_id")

input_file = sc.textFile("topic-url.txt")

def get_name_id(data):
	#pre-processing
	for (k, v) in data.items():
		url = v['topic_url']
	#get data
	html_doc = urlopen(url).read()
	elements = re.findall(r'class="Author-name--profileLink" href=".*"', html_doc)
	individual_link = [element.split()[1] for element in elements]
	#process data
	name_id_list = [] #initialize
	for item in individual_link:
		individual_profile_link = item.split("=")[1]
		individual_name = individual_profile_link.split('/')[-2] #get the name
		individual_id = individual_profile_link.split('/')[-4] #get the id
		name_id_list.append((individual_name, individual_id))
	print(name_id_list)

output = input_file.map(lambda line: json.loads(line)) \
		.flatMap(get_name_id) \
		.reduceByKey(lambda x, y: x[1]) \
		.map(lambda x: x[0] + '\t' + x[1])

output.collect()
output.saveAsTextFile("name_id_output")