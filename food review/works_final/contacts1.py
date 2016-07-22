import os
import urllib
import base64

from google.appengine.api import images
from google.appengine.ext import ndb
from PIL import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class Restaurant(ndb.Model):

	name = ndb.StringProperty()
	restaratunt_review = ndb.StringProperty()
	rating = ndb.StringProperty()

	
class ViewRestraunts(webapp2.RequestHandler):
	
	def get(self):
		restaratunts_query = Restaurant.query().order(Restaurant.name)
		restaratunts = restaratunts_query.fetch(100)

		template_values = {
			'contacts': restaratunts,
		}

		template = JINJA_ENVIRONMENT.get_template('view2.html')
		self.response.write(template.render(template_values))

class AddRestraunts(webapp2.RequestHandler):
	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('add2.html')
		self.response.write(template.render())
		
class EditRestraunts(webapp2.RequestHandler):

	def post(self):
		
		restaurant = Restaurant.get_by_id(int(self.request.get('id')))
		
		template_values = {
			'restaurant': restaurant,
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit2.html')
		self.response.write(template.render(template_values))
	
class Entry(webapp2.RequestHandler):

	def post(self):
		
		action = self.request.get('action')
		id = int(self.request.get('id'))
		
		if action == "add2":
			restaurant = Restaurant()
			restaurant.name = self.request.get('name')
			restaurant.restaratunt_review = self.request.get('restaratunt_review')
			restaurant.rating = self.request.get('rating')
			restaurant.put()
			self.redirect('/view2')
		elif action == "edit2":
			restaurant = Restaurant.get_by_id(id)
			restaurant.name = self.request.get('name')
			restaurant.restaratunt_review = self.request.get('restaratunt_review')
			restaurant.rating = self.request.get('rating')
			restaurant.put()
			self.redirect('/view2')
		elif action == "delete2":
			restaurant = Restaurant.get_by_id(id)
			restaurant.key.delete()
			self.redirect('/view2')    
      

application = webapp2.WSGIApplication([
	('/', ViewRestraunts),
	('/view2', ViewRestraunts),
	('/add2', AddRestraunts),
	('/edit2', EditRestraunts),
	('/enter', Entry),
], debug=True)
util.run_wsgi_app (application)
