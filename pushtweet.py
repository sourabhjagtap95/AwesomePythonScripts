from tweepy import OAuthHandler
import tweepy
#consumer key, consumer secret, access token, access secret.
#create a twitter app to get all the authentication credentials
ckey=" "
csecret=" "
atoken=" "
asecret=" "

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api=tweepy.API(auth)

#write the tweet messege to update on twitter
api.update_status('Hola Twitter 2, (checking twitter python api)')
