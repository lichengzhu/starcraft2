"""
'''
To ssh into flux:
ssh zlicheng@flux-hadoop-login.arc-ts.umich.edu

To ssh into AWS:
ssh -i "si618w17.pem" ubuntu@ec2-34-223-252-142.us-west-2.compute.amazonaws.com

To load extra packages:
module load python-anaconda3/latest
'''
"""


#######################################
# This is a "master" script that runs other python scripts. The flow is as follow:
# step 1: get_topic_url.py     -> capturing all topics under Blizzard Starcraft 2 General Discussion forum
# step 2: get_post.py      -> parse through forum topics and save posts into local database 'starcraft_project.db'
# step 3: get_game.py     -> using captured user names and user ids to fetch in-game data via Blizzard API
# step 4: get_profile.py     -> using captured user names and user ids to fetch players' game profile via Blizzard API
#######################################


import os 

os.system('python get_topic_url.py')
os.system('python get_post.py')
os.system('python get_game.py')
os.system('python get_profile.py')