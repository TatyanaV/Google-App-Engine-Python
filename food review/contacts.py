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

#this will be the name and the picture of the food    
class Restaurant(ndb.Model):
	#name of the food 
	name = ndb.StringProperty()
	#description of the food
	restaratunt_review = ndb.StringProperty()
	photo = ndb.BlobProperty()
	#price of the food
	rating = ndb.FloatProperty()
	
#this will be the review of the food	
class Food(ndb.Model):
  # description of the review
  food_review = ndb.StringProperty()
  place_checkmark = ndb.StringProperty()
  #rating from 1 to 5
  food_rating = ndb.StringProperty()
  #child of the Restaurant
  restraunt2 = ndb.KeyProperty(kind = 'Restaurant')
  

			
class ViewRestraunts(webapp2.RequestHandler):
	
	def get(self):
		restaratunts_query = Restaurant.query().order(Restaurant.name)
		restaratunts = restaratunts_query.fetch(100)

		template_values = {
			'contacts': restaratunts,
		}

		template = JINJA_ENVIRONMENT.get_template('view2.html')
		self.response.write(template.render(template_values))

class ViewRestrauntsForSortedReviews(webapp2.RequestHandler):
	
	def get(self):
		restaratunts_query = Restaurant.query().order(Restaurant.name)
		restaratunts = restaratunts_query.fetch(100)

		template_values = {
			'contacts': restaratunts,
		}

		template = JINJA_ENVIRONMENT.get_template('sorted_reviews.html')
		self.response.write(template.render(template_values))		

class AddRestraunts(webapp2.RequestHandler):
	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('add2.html')
		self.response.write(template.render())
		

class ViewFood(webapp2.RequestHandler):
  
	def get(self):
		#foods_query = Food.query().order(Food.id())
		#this is query for the review
		foods_query = Food.query()
		foods = foods_query.fetch(100)
		#also need to do the query for the food
		restaratunts_query = Restaurant.query().order(Restaurant.name)
		restaratunts = restaratunts_query.fetch(100)	

		template_values = {
			'foods': foods,
			'contacts': restaratunts,
		}

		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render(template_values))
		
	
		
class EditRestraunts(webapp2.RequestHandler):

	def post(self):
		
		restaurant = Restaurant.get_by_id(int(self.request.get('id')))
		
		template_values = {
			'restaurant': restaurant,
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit2.html')
		self.response.write(template.render(template_values))
		
class ReviewPerFoodIteration(webapp2.RequestHandler):

	def post(self):
		#we are getting a key
		restaurant = Restaurant.get_by_id(int(self.request.get('id')))
		restraoung_key = restaurant.key
		#if restraoung_key:
		review_query = Restaurant.query(Restaurant.key == restraoung_key).get()
			#if review_query:
		review_query2 = Food.query(Food.restraunt2 == review_query.key)
			#else:
			#	self.response.out.write("THIS DISH DOES NOT HAVE ANY REVIEWS.")
		foods = review_query2.fetch(100)	
		template_values = {
			'restaurant': restaurant,
			'foods': foods,
		}
		
		template = JINJA_ENVIRONMENT.get_template('17.html')
		self.response.write(template.render(template_values))	
		
class EditFood(webapp2.RequestHandler):

	def post(self):
		
		food = Food.get_by_id(int(self.request.get('id')))
		get_dish = Restaurant.query(food.restraunt2 == Restaurant.key).get()
		
		template_values = {
			'food': food,
			'restaurant': get_dish,
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values)) 
		
					
class ViewReviewPerFood(webapp2.RequestHandler):
  
	def get(self):
		restaurant = Restaurant.get_by_id(int(self.request.get('id')))
		
		#id = int(self.request.get('id'))
		#action = self.request.get('action')
		#also we need to delete all reviews associated with the food
		#review_delete = Food.get_by_id(id)
		#restraunt_name = self.request.get('restraunt4')
		#http://stackoverflow.com/questions/31852364/how-can-i-avoid-circular-imports-in-python-google-app-engine-ndb-pattern-to-avo
		#if action == "viewreviewperfood":
		restraoung_key = restaurant.key		
		#restaurant = Restaurant.get_by_id(id)
		for review_food in Food.query(restraoung_key == Food.restraunt2).fetch():
		#If dish does not have any reviews, there is nothing to delete
		#we need to make sure that all reviews are deleted
			if review_food is None:
				self.response.out.write("THIS DISH DOES NOT HAVE ANY REVIEWS.")
			else:
				foods_query = Food.query()
				foods = foods_query.fetch(100)
		template_values = {
			'foods': foods,
			'contacts': restaratunts,
		}
		template = JINJA_ENVIRONMENT.get_template('review_per_dish.html')
		self.response.write(template.render(template_values))	

		
    
class AddFood(webapp2.RequestHandler):
	def get(self):
		#Restaurant_id = int(Restaurant_id)
		#rest3 = Restaurant.get_by_id(int(Restaurant_id))
		#you need to do the query both for the food and for the review
		restaratunts_query = Restaurant.query().order(Restaurant.name)
		restaratunts = restaratunts_query.fetch(100)
		#rest3 = restaratunts[0]
		foods_query = Food.query()
		foods = foods_query.fetch(100)
		#feed.key = ndb.Key('Restaurant', int(feed.Restaurant_id), parent=Restaurant.key)

		template_values = {
			'contacts': restaratunts,
			'foods': foods,
		}

		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.write(template.render(template_values))
	
		

		
class Entry(webapp2.RequestHandler):

	def post(self):
	
		action = self.request.get('action')
		id = int(self.request.get('id'))
		#add food to the database
		if action == "add2":
			restaurant = Restaurant()
			#name of the food
			restaurant.name = self.request.get('name')
			#description of the food
			restaurant.restaratunt_review = self.request.get('restaratunt_review')
			#price of the food
			restaurant.rating = float(self.request.get('rating'))
			#photo of the food
			if self.request.get('photo') == "":
				restaurant.photo = base64.b64encode("")
			else:
				restaurant.photo = base64.b64encode(str(images.resize(self.request.get('photo'),140,140)))
 			restaurant.put()
			self.redirect('/view2')
		#add review to the database	
		elif action == "add":
		  food = Food()
		  rest = Restaurant()
		  #rest2 = Restaurant.query()
		  #restraunt2 = rest2.order(Restaurant.id)
		  #first we need to look for the existing restaurant
		  restraunt_name = self.request.get('restraunt4')
		  restaurant3 = Restaurant.query(Restaurant.name == restraunt_name).get()
		  if not restaurant3:
		   restaurant3 = Restaurant()
		   restaurant3.name = restraunt_name
		   restaurant3.put()
		  #logging.info("Added owner: %s", restraunt.key)
		  food.restraunt2 = restaurant3.key
		  #description of the food
		  food.food_review = self.request.get('food_review')
		  # 1 though 5
		  food.food_rating = self.request.get('food_rating')
		  #checkmark
		  food.place_checkmark = self.request.get('place_checkmark')
		  #food.restraunt2 = self.request.get('restraunt2')
		  food.put() 
		  self.redirect('/view')
		#edit of the food information	
		elif action == "edit2":
			restaurant = Restaurant.get_by_id(id)
			restaurant.name = self.request.get('name')
			restaurant.restaratunt_review = self.request.get('restaratunt_review')
			restaurant.rating = float(self.request.get('rating'))
			if self.request.get('photo_choice') == "change":
				if self.request.get('photo') == "":
					restaurant.photo = base64.b64encode("")
				else:
					restaurant.photo = base64.b64encode(str(images.resize(self.request.get('photo'), 140, 140)))
			restaurant.put()
			self.redirect('/view2')
		elif action == "delete2":
			#need to delete food 
			restaurant = Restaurant.get_by_id(id)
			#also we need to delete all reviews associated with the food
			#review_delete = Food.get_by_id(id)
			#restraunt_name = self.request.get('restraunt4')
			#http://stackoverflow.com/questions/31852364/how-can-i-avoid-circular-imports-in-python-google-app-engine-ndb-pattern-to-avo
			restraoung_key = restaurant.key
			#http://stackoverflow.com/questions/22843919/google-app-engine-database-object-is-not-iterable
			for review_delete in Food.query(restraoung_key == Food.restraunt2).fetch():
			#If dish does not have any reviews, there is nothing to delete
			#we need to make sure that all reviews are deleted
				if review_delete is None:
					self.response.out.write("THIS DISH DOES NOT HAVE ANY REVIEWS. NO REVIEWS WILL BE DELETED.")
				else:
					review_delete.key.delete()
			#for reviewquery in Food.query(Food.restraunt2 == restraoung_key).get():
			#reviewquery.key.delete()
			#ndb.delete_multi(ndb.Query(ancestor= restaurant.key).iter(keys_only = True))
			#reviewquery.key.delete()
			restaurant.key.delete()
			self.redirect('/view2')
		elif action == "delete":
			food = Food.get_by_id(id)
			food.key.delete()
			self.redirect('/view')
		#edit of the food review	
		elif action == "edit":
			food = Food.get_by_id(id)
			food.food_review = self.request.get('food_review')
			food.food_rating = self.request.get('food_rating')
			food.place_checkmark = self.request.get('place_checkmark')
			food.put()
			self.redirect('/view')
	
      

application = webapp2.WSGIApplication([
	('/', ViewRestraunts),
	('/view2', ViewRestraunts),
  ('/view', ViewFood),
  ('/add', AddFood),
	('/add2', AddRestraunts),
	('/edit2', EditRestraunts),
	('/enter', Entry),
	('/edit', EditFood),
	('/sorted_reviews', ViewRestrauntsForSortedReviews),
	('/17', ReviewPerFoodIteration),
], debug=True)
util.run_wsgi_app (application)
