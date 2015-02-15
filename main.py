import webapp2
import urllib

#append path to resolve the third party issue at google app engine
import sys
sys.path.insert(0, 'libs')

from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(generate_rss)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)


class Article:
	def __init__(self, title, link, preamble, content):
		self.title = title
		self.link = link
		self.preamble = preamble
		self.content = content

def generate_rss(article):
	fg = FeedGenerator()
	#todo: change this to a real id later
	fg.id('http://lernfunk.de/media/%s' % article.title)

	fg.title(article.title)
	fg.link(href=article.link)
	fg.description("%s \n %s" % (article.preamble, article.content))

	fg.language('en')
	rssfeed = fg.rss_str(pretty=True) # Get the RSS feed as string
	return rssfeed
	#fg.rss_file('%s_rss.xml' % article.title) # Write the RSS feed to a file

def get_article(url):
	#create an url object
	url_obj = urllib.urlopen(url)
	soup = BeautifulSoup(url_obj.read())
	title = soup.title.string
	link = url_obj.geturl()
	preamble = soup.find_all(id="preamble")[0].text
	main_text = soup.find_all(id="main-text")[0].text
	#contruct an article object
	article = Article(title, link, preamble, main_text)

	return article

#article = get_article("http://plato.stanford.edu/cgi-bin/encyclopedia/random")
#generate_rss(article)

