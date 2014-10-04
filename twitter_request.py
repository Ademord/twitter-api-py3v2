import requests
import base64
import json
import sys

def log(msg):
	sys.stderr.write(msg)
	sys.stderr.write('\n')
def search_hashtag(hashtag, count):
	#############################################################
	#          Step 1: Encode consumer key and secret           #
	#############################################################
	client_key= 'KlERfpepfwGbr6mFXnJmOlGjB'
	client_secret = '1eWnSzH4u4uwGghVVDFjkbPnr81pY28dggbHdW2vlNuBByymxU'
	#############################################################
	#                Step 2: Obtain a bearer token              #
	#############################################################
	bearer_token = '%s:%s' % (client_key, client_secret)

	encoded_bearer_token = base64.b64encode(bearer_token.encode('ascii')).decode('ascii')

	request_token_url = 'https://api.twitter.com/oauth2/token'

	request_token_headers = {
		'Authorization': 'Basic %s' % encoded_bearer_token,
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	}

	request_token_body = {
		'grant_type': 'client_credentials'
	}

	log('Requesting access tokens...')

	try:
		r = requests.post(request_token_url, data = request_token_body, headers = request_token_headers)
	except ValueError:
		print("Couldn't connect to twitter api to obtain a bearer token.")
	#############################################################
	#                   Step 2.5 Build Request                  # 
	#############################################################
	oauth_tokens = json.loads(r.text)

	protected_url = 'https://api.twitter.com/1.1/search/tweets.json'

	search_query = {
		'q': hashtag,
		'result_type': 'recent',
		'count': count
	}
	#############################################################
	#  Step 3: Authenticate API requests with the bearer token  #
	#############################################################
	request_headers = {
		'Authorization': 'Bearer %s' % oauth_tokens['access_token']
	}

	log('Fetching tweets...')

	r = requests.get(protected_url, params = search_query, headers = request_headers)
	#############################################################
	#                 Step 3.5: Parse Information               #
	#############################################################
	response = json.loads(r.text)
	return response
        #print( json.dumps(response, indent = 2))
	return json.dumps(response, indent = 2)

if __name__ == "__main__":
	print( search_hashtag("#python",1))