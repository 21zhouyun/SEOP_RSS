import webapp2
import urllib
import datetime
from google.appengine.api import memcache
from google.appengine.ext import db

#append path to resolve the third party issue at google app engine
import sys
sys.path.insert(0, 'libs')

from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from pytz import timezone


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("http://plato.stanford.edu/cgi-bin/encyclopedia/random")

class Feed(webapp2.RequestHandler):
	def get(self):
		article = get_article("http://plato.stanford.edu/cgi-bin/encyclopedia/random")
		self.response.headers['Cache-Control'] = 'public,max-age=%s' % 86400
		self.response.headers['Content-Type'] = 'text/xml'
		self.response.out.write(generate_rss(article))

application = webapp2.WSGIApplication([
	('/', MainPage), ('/feed', Feed)
], debug=True)


class Article(db.Model):
		title = db.TextProperty(required=True)
		link = db.StringProperty(required=True)
		preamble = db.TextProperty(required=True)
		content = db.TextProperty(required=True)

def generate_rss(article):
	fg = FeedGenerator()
	#todo: change this to a real id later
	fg.id('http://www.example.com')
	fg.title("RESEP")
	fg.link(href="http://plato.stanford.edu/", rel='self')
	fg.description("This feed grabs a random entry from the Stanford Encyclopedia of Philosophy everyday")

	fe = fg.add_entry()
	fe.title(article.title)
	fe.link(href=article.link, rel='alternate')
	fe.id(article.link)
	fe.author(name="Stanford University")
	fe.published(published=get_last_update_date())
	fe.description("%s \n %s" % (article.preamble, article.content))
	fe.content(content="%s \n %s" % (article.preamble, article.content), type='CDATA')

	fg.language('en')
	rssfeed = fg.rss_str(pretty=True) # Get the RSS feed as string
	return rssfeed
	#fg.rss_file('%s_rss.xml' % article.title) # Write the RSS feed to a file

def get_article(url):
	last_update = get_last_update_date()
	cached_article_id = memcache.get('cached_article_id')
	eastern = timezone('US/Eastern')
	#get new entry
	if (eastern.localize(datetime.datetime.now()) - last_update).days >= 1 or cached_article_id is None:

		#create an url object
		url_obj = urllib.urlopen(url)
		soup = BeautifulSoup(url_obj.read())
		title = soup.title.string
		link = url_obj.geturl()
		preamble = soup.find_all(id="preamble")[0].encode('utf-8')
		content = soup.find_all(id="main-text")[0].encode('utf-8')
		#contruct an article object
		article = Article(title=title, link=link, preamble=preamble.decode('utf-8'), content=content.decode('utf-8'))
		article.put()

		memcache.add('cached_article_id', article.key().id())
		#update last update date
		eastern = timezone('US/Eastern')
		date = eastern.localize(datetime.datetime.now())
		memcache.add('last_update', date)

		return article

	else:
		return Article.get_by_id(cached_article_id)

#deal with memcache
def get_last_update_date():
    date = memcache.get('last_update')
    if date is not None:
        return date
    else:
    	eastern = timezone('US/Eastern')
        date = eastern.localize(datetime.datetime.now())
        memcache.add('last_update', date)
        return date


#generate_rss(article)

