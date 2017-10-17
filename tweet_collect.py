#Collects tweets from a particular topic given as terminal input while running the file:
#python3 tweet_collect.py "topic_name"

import json
import sys
from twython import Twython

#Add your Twitter app credentials
api_key = {
	'api_key': ' ',
	'api_secret': ' ',
	'access_token': ' ',
	'access_token_secret': ' '
}

# Initializing the Twython API object
twitter= Twython(api_key['api_key'],
				api_key['api_secret'],
				api_key['access_token'],
				api_key['access_token_secret']
				)

query=sys.argv[1].lower()
filename=sys.argv[1].lower()+".txt"

d={} #dictionary containing data
mini_id=sys.maxsize
check=0

try:
	new_statuses = twitter.search(q=query, count="100", include_entities= True, lang="en") #searches for the given query q, language set as 'english'
	while (len(d)<10000): #change the number here to collect as many tweets
		for tweet in new_statuses['statuses']:
			t = {} #new dictionary which will be contained in the original dictionary 'd' via tweet id
			t['zone'] = tweet['user']['time_zone']
			t['time'] = tweet['created_at']
			t['text'] = tweet['text']

			if 'media' in tweet['entities']: #checks if media contained in entities, sets true/false accordingly
				if len(tweet['entities']['media'])>=1:
					t['photo'] = True
				else:
					t['photo'] = False
			else:
				t['photo'] = False
			
			if 'urls' in tweet['entities']: #checks if url contained in entities, sets true/false accordingly
				if len(tweet['entities']['urls'])>=1:
					t['url'] = True
				else:
					t['url'] = False
			else:
				t['url'] = False
			
			if tweet['retweet_count']>0: #checks if the retweet count is greater than 0, implying it has been retweeted, thus setting true/false accordingly
				t['rt'] = True
			else:
				t['rt'] = False
			
			d[tweet['id']] = t #forms a structure like - d = {id1:{zone:,time:,text:,photo:,url:,rt:}, id2:{zone:,time:,text:,photo:,url:,rt:},.......}

			if tweet['id'] < mini_id:
				mini_id = tweet['id'] #getting the minimum id of all 100 tweets so that repetitions are not obtained in the next search
		new_statuses = twitter.search(q=query, count="100", include_entities= True, lang="en", max_id=mini_id-1)

except:
	check=1
	print("Rate Limit Error- Remaining Data added")# if rate limit is exceeded
	print("Total Tweets Collected",len(d))
	data = json.dumps(d) 
	f = open(filename,"w")
	f.write(data) #whatever data obtained written to file
	f.close()	

if check==0: #if no error occured, then data written to file
	data = json.dumps(d)
	print("Total Tweets Collected",len(d))
	f = open(filename,"w")
	f.write(data)
	f.close()
