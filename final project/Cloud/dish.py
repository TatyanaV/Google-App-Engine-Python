import os
import urllib
import base64
from google.appengine.api import users
from jinja2 import Environment, PackageLoader


from google.appengine.api import images
from google.appengine.ext import ndb
from PIL import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import jinja2
import webapp2
import util
import time

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
	
	
#user = users.get_current_user() 

#this will be the name and the picture of the dish 
class Dish(ndb.Model):
	#name of the dish
	name = ndb.StringProperty()
	#description of the dish
	dish_description = ndb.StringProperty()
	#price of the dish
	price = ndb.StringProperty()
	dish_user = ndb.UserProperty()
	
#this will be the review of the dish
class Dish_Review(ndb.Model):
  # this will be the date for now
  place_checkmark = ndb.StringProperty()
  #check ammount
  check_amount = ndb.FloatProperty()
  #child of the Dish
  dish_link = ndb.KeyProperty(kind = 'Dish')
  

			

class ViewDishesForSortedReviews(webapp2.RequestHandler):
	
	def get(self):
		user = users.get_current_user() 

		logout = users.create_logout_url('/')
		dish_query = Dish.query().order(Dish.name)
		view_dishes = dish_query.fetch(100)

		template_values = {
			'view_dishes': view_dishes,
			'logout' : util.create_logout_url(''),
		}

		template = JINJA_ENVIRONMENT.get_template('sorted_reviews.html')
		self.response.write(template.render(template_values))		

class AddDishes(webapp2.RequestHandler):
	
	def get(self):
		user = users.get_current_user() 

		template_values = {
			'logout' : util.create_logout_url(''),
		}
		template = JINJA_ENVIRONMENT.get_template('add2.html')
		self.response.write(template.render(template_values))
		

		
class EditDish(webapp2.RequestHandler):

	def post(self):
		logout = users.create_logout_url('/')
		user = users.get_current_user() 

		
		dish = Dish.get_by_id(int(self.request.get('id')))
		
		template_values = {
			'dish': dish,
			'logout' : util.create_logout_url(''),
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit2.html')
		self.response.write(template.render(template_values))
		
class ReviewPerFoodIteration(webapp2.RequestHandler):

	def post(self):
		#we are getting a key
		user = users.get_current_user() 

		logout = users.create_logout_url('/')
		dish = Dish.get_by_id(int(self.request.get('id')))
		dish_key = dish.key
		#if dish_key:
		review_query = Dish.query(Dish.key == dish_key).get()
			#if review_query:
		review_query2 = Dish_Review.query(Dish_Review.dish_link == review_query.key)
			#else:
			#	self.response.out.write("THIS DISH DOES NOT HAVE ANY REVIEWS.")
		dish_reviews = review_query2.fetch(100)	
		template_values = {
			'dish': dish,
			'dish_reviews': dish_reviews,
			'logout' : util.create_logout_url(''),
		}
		
		template = JINJA_ENVIRONMENT.get_template('17.html')
		self.response.write(template.render(template_values))


class ViewDishes(webapp2.RequestHandler):
	
	def get(self):
	
		#dish_query = Dish.query().order(Dish.name)
		#view_dishes = dish_query.fetch(100)
		user = users.get_current_user() 

		user_email = user.email()
		logout2 = users.create_logout_url('/')
		review_query2 = Dish.query(Dish.dish_user == user)
		view_dishes = review_query2.fetch(100)	
		template_values = {
			'view_dishes': view_dishes,
			'logout2': logout2,
			'user_email': user_email,
			'logout' : util.create_logout_url(''),
		}

		template = JINJA_ENVIRONMENT.get_template('view2.html')
		self.response.write(template.render(template_values))



		
class EditReview(webapp2.RequestHandler):

	def post(self):
		user = users.get_current_user() 

		logout = users.create_logout_url('/')
		dish_reviews = Dish_Review.get_by_id(int(self.request.get('id')))
		get_dish = Dish.query(dish_reviews.dish_link == Dish.key).get()
		
		template_values = {
			'dish_reviews': dish_reviews,
			'dish': get_dish,
			'logout' : util.create_logout_url(''),
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values)) 
		
					
class ViewReviewPerFood(webapp2.RequestHandler):
  
	def get(self):
		user = users.get_current_user() 

		dish = Dish.get_by_id(int(self.request.get('id')))
		
		#id = int(self.request.get('id'))
		#action = self.request.get('action')
		#also we need to delete all reviews associated with the dish_reviews
		#review_delete = Dish_Review.get_by_id(id)
		#dish_name = self.request.get('dish_for_review')
		#http://stackoverflow.com/questions/31852364/how-can-i-avoid-circular-imports-in-python-google-app-engine-ndb-pattern-to-avo
		#if action == "viewreviewperfood":
		dish_key = dish.key		
		#dish = Dish.get_by_id(id)
		for review_food in Dish_Review.query(dish_key == Dish_Review.dish_link).fetch():
		#If dish does not have any reviews, there is nothing to delete
		#we need to make sure that all reviews are deleted
			if review_food is None:
				self.response.out.write("THIS DISH DOES NOT HAVE ANY REVIEWS.")
			else:
				dish_review_query = Dish_Review.query()
				dish_reviews = dish_review_query.fetch(100)
		template_values = {
			'dish_reviews': dish_reviews,
			'view_dishes': view_dishes,
			'logout' : util.create_logout_url(''),
		}
		template = JINJA_ENVIRONMENT.get_template('review_per_dish.html')
		self.response.write(template.render(template_values))	

		
    
class AddReview(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user() 

		logout = users.create_logout_url('/')
		for dishes_list in Dish.query(Dish.dish_user == user).fetch():
		#If dish does not have any reviews, there is nothing to delete
		#we need to make sure that all reviews are deleted
			if dishes_list is None:
				self.response.out.write("THIS user does not have any employees added.")
			else:
				dish_query = Dish.query(Dish.dish_user == user)
				view_dishes = dish_query.fetch(100)
				#dish = Dish.get_by_id(int(self.request.get('id')))
				dish_review_query = Dish_Review.query()
				dish_reviews = dish_review_query.fetch(100)
		template_values = {
			'view_dishes': view_dishes,
			'dish_reviews': dish_reviews,
			'logout' : util.create_logout_url(''),
		}

		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.write(template.render(template_values))
	
class LogOut(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            template = env.get_template('logout.html')
            self.response.write(template.render())
        else: 
        	self.redirect(users.create_login_url(self.request.uri))

			
class Entry(webapp2.RequestHandler):

	def post(self):
		#user = users.get_current_user()
		#user1 = self.request.get('username')
		#password1 = self.request.get('password')
		#combination_query = User.query(User.username == user1 and User.password == password1).get()
		
		user = users.get_current_user() 

		action = self.request.get('action')
		action2 = self.request.get('action2')
		id = int(self.request.get('id'))
		#add dish  to the database
		if action == "add2":
			dish = Dish()
			#name of the dish
			dish.name = self.request.get('name')
			#description of the dish
			dish.dish_description = self.request.get('dish_description')
			dish.dish_user = user
			#price of the dish
			dish.price = self.request.get('price')
			#photo of the dish
 			dish.put()
			self.redirect('/view2')
		#add review to the database	
		elif action == "add":
		  dish_reviews = Dish_Review()
		  rest = Dish()
		  #rest2 = Dish.query()
		  #dish_link = rest2.order(Dish.id)
		  #first we need to look for the existing dish
		  dish_name = self.request.get('dish_for_review')
		  dish3 = Dish.query(Dish.name == dish_name).get()
		  if not dish3:
		   dish3 = Dish()
		   dish3.name = dish_name
		   dish3.put()
		  #logging.info("Added owner: %s", dish.key)
		  dish_reviews.dish_link = dish3.key
		  # 1 though 5
		  dish_reviews.check_amount = float(self.request.get('check_amount'))
		  #checkmark
		  dish_reviews.place_checkmark = self.request.get('place_checkmark')
		  #dish_reviews.dish_link = self.request.get('dish_link')
		  dish_reviews.put() 
		  self.redirect('/view2')
		#edit of the dish information	
		elif action == "edit2":
			dish = Dish.get_by_id(id)
			dish.name = self.request.get('name')
			dish.dish_description = self.request.get('dish_description')
			dish.price = self.request.get('price')
			dish.put()
			self.redirect('/view2')
		elif action == "delete2":
			#need to delete dish_reviews 
			dish5 = Dish.get_by_id(int(self.request.get('id')))
			#also we need to delete all reviews associated with the dish_reviews
			#review_delete = Dish_Review.get_by_id(id)
			#dish_name = self.request.get('dish_for_review')
			#http://stackoverflow.com/questions/31852364/how-can-i-avoid-circular-imports-in-python-google-app-engine-ndb-pattern-to-avo
			dish_key = dish5.key
			#http://stackoverflow.com/questions/22843919/google-app-engine-database-object-is-not-iterable
			for review_delete in Dish_Review.query(dish_key == Dish_Review.dish_link).fetch():
			#If dish does not have any reviews, there is nothing to delete
			#we need to make sure that all reviews are deleted
				if review_delete is None:
					self.response.out.write("THIS DISH DOES NOT HAVE ANY REVIEWS. NO REVIEWS WILL BE DELETED.")
				else:
					review_delete.key.delete()
			#for reviewquery in Dish_Review.query(Dish_Review.dish_link == dish_key).get():
			#reviewquery.key.delete()
			#ndb.delete_multi(ndb.Query(ancestor= dish.key).iter(keys_only = True))
			#reviewquery.key.delete()
			dish5.key.delete()
			self.redirect('/view2')
		elif action == "delete":
			dish_reviews = Dish_Review.get_by_id(id)
			dish_reviews.key.delete()
			self.redirect('/view2')
		#edit of the dish_reviews review	
		elif action == "edit":
			dish_reviews = Dish_Review.get_by_id(id)
			dish_reviews.check_amount = float(self.request.get('check_amount'))
			dish_reviews.place_checkmark = self.request.get('place_checkmark')
			dish_reviews.put()
			self.redirect('/view2')
			
class MainPage(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			user_email = user.email()
			#logout = util.create_logout_url('')
			#logout = users.create_logout_url('/')
			template_values = {
				'logout' : util.create_logout_url(''),
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))
			
	

		
def create_logout_url(url):
  return users.create_logout_url(url)		

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/index', MainPage),
	('/view2', ViewDishes),
	('/add', AddReview),
	('/add2', AddDishes),
	('/edit2', EditDish),
	('/enter', Entry),
	('/edit', EditReview),
	('/17', ReviewPerFoodIteration),
], debug=True)

