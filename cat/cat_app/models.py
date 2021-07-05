from django.db import models
from datetime import datetime
import bcrypt, re

class UserManager(models.Manager):
	def basic_validation(self, post_data):
		#error message, starts as empty tuple adds if anything doesn't match credintials
		errors = {}
		#email format validation
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		#setting length minimum for password, first & last name and error message that pops up directing user of error
		if len(post_data['password']) < 8:
			errors['password'] = "Your password needs to be at least 8 characters"
		if len(post_data['password']) > 60:
			errors['password'] = "Password can not be over 45 characters"
		if len(post_data['first_name']) < 2:
			errors['first_name'] = "First name must be 2 characters or more"
		if len(post_data['last_name']) < 2:
			errors['last_name'] ="Last name must be 2 characters or more"
		#validating email
		if not EMAIL_REGEX.match(post_data['email']):
			errors['email'] = "Email must be valid"
		emailcheck = self.filter(email=post_data['email'])
		if emailcheck:
			errors['email'] = 'email already in use'
		#make sures passwords match in confirm password part of register
		if post_data['password'] != post_data['confirm_password']:
			errors['password'] = "Passwords must match"
		#returns any error in registration, if not will lead to success page
		return errors 

# Users info
class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	password = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# to call to UserManager to help validate info
	objects =UserManager()


	
		
