"""import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
"""

#test the feedgen library
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
import urllib

def generate_rss(Article):
	fg = FeedGenerator()
	fg.id('http://lernfunk.de/media/654321')
	fg.title('Some Testfeed')
	fg.author( {'name':'John Doe','email':'john@example.de'} )
	fg.link( href='http://example.com', rel='alternate' )
	fg.logo('http://ex.com/logo.jpg')
	fg.subtitle('This is a cool feed!')
	fg.link( href='http://larskiesow.de/test.atom', rel='self' )
	fg.language('en')

	rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
	fg.rss_file('rss.xml') # Write the RSS feed to a file

def get_article(url):
	soup = BeautifulSoup(urllib.urlopen(url).read())
	title = soup.title.string
	preamble = soup.find_all(id="preamble")[0].text.encode("utf-8")
	main_text = soup.find_all(id="main-text")[0].text.encode("utf-8")
	
	article = Article(title, preamble, main_text)
	return article

get_article("http://plato.stanford.edu/cgi-bin/encyclopedia/random")

class Article():
	def __init__(self, title, preamble, content):
		self.title = title
		self.preamble = preamble
		self.content = content
