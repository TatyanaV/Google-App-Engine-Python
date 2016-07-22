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
  