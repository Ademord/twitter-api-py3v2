import tornado.ioloop
import tornado.web
import tornado.template
import tornado.httpserver
import os
import os.path
import re
#from twitter_test import search_hashtag
from twitter_request import search_hashtag
from replacer import tweet_replace_links
import json
loader = tornado.template.Loader(os.path.join(os.getcwd(), "templates"))

class Templates(object):
	tweet_list = loader.load("prueba_tweet_list.html")
	


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		count_str = self.get_argument("count", default=10)
		count = int(count_str)
		#count = 10

		hashtag = self.get_argument("hashtag", default="steam")
		if not hashtag.startswith("#"):
			hashtag = "#" + hashtag
		# GET TWEETS FEED BY HASHTAG
		tweets = search_hashtag(hashtag,count)
		tweets = tweets['statuses']
		for t in tweets:
			#t['text'] = re.sub(r'(http+[^ ]+[a-zA-Z0-9])+.+[a-zA-Z0-9]',r'<a href="\1">\1</a>', t['text'])
			if 'After playing' in t['text']:
				print (json.dumps(t, indent = 2))
			t['text'] = tweet_replace_links(t)
	
		css_path = os.path.join("css")
		html = Templates.tweet_list.generate(tweets = tweets, count=count, 
			hashtag = hashtag[1:])
		
		self.write(html)


def main():
	css_path = os.path.join(os.getcwd(), "templates","css")
	handlers = [ (r"/", MainHandler),
				(r'/css/(.*)', tornado.web.StaticFileHandler, {'path': css_path}) ]
	#settings = { "static_url": os.path.join(os.getcwd(), "templates", "css") }

	application = tornado.web.Application(handlers)
	http_server = tornado.httpserver.HTTPServer(application)
	port = int(os.environ.get("PORT", 5000))
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
	main()
