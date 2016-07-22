import os
import urllib
import base64

from google.appengine.api import images
from google.appengine.ext import ndb
from PIL import Image

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class Contact(ndb.Model):

	name = ndb.StringProperty()
	your_review = ndb.StringProperty()
	rating = ndb.StringProperty()
	place_checkmark = ndb.StringProperty()
	photo = ndb.BlobProperty()
	
class ViewContacts(webapp2.RequestHandler):
	
	def get(self):
		foods_query = Contact.query().order(Contact.name)
		foods = foods_query.fetch(100)

		template_values = {
			'foods': foods,
		}

		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render(template_values))

class AddContacts(webapp2.RequestHandler):
	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.write(template.render())
		
class EditContacts(webapp2.RequestHandler):

	def post(self):
		
		food = Contact.get_by_id(int(self.request.get('id')))
		
		template_values = {
			'food': food,
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))
	
class Entry(webapp2.RequestHandler):

	def post(self):
		
		action = self.request.get('action')
		id = int(self.request.get('id'))
		
		if action == "add":
			food = Contact()
			food.name = self.request.get('name')
			food.your_review = self.request.get('your_review')
			food.rating = self.request.get('rating')
			food.place_checkmark = self.request.get('place_checkmark')
			if self.request.get('photo') == "":
				food.photo = base64.b64encode("")
			else:
				food.photo = base64.b64encode(str(images.resize(self.request.get('photo'), 140, 140)))
			food.put()
			self.redirect('/view')
		elif action == "edit":
			food = Contact.get_by_id(id)
			food.name = self.request.get('name')
			food.your_review = self.request.get('your_review')
			food.rating = self.request.get('rating')
			food.place_checkmark = self.request.get('place_checkmark')
			if self.request.get('photo_choice') == "change":
				if self.request.get('photo') == "":
					food.photo = base64.b64encode("")
				else:
					food.photo = base64.b64encode(str(images.resize(self.request.get('photo'), 140, 140)))
			food.put()
			self.redirect('/view')
		elif action == "delete":
			food = Contact.get_by_id(id)
			food.key.delete()
			self.redirect('/view')

application = webapp2.WSGIApplication([
	('/', ViewContacts),
	('/view', ViewContacts),
	('/add', AddContacts),
	('/edit', EditContacts),
	('/enter', Entry),
], debug=False)
