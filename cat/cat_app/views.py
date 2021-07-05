from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.db.models import Sum
import requests

def index(request):
	return render(request, "index.html")

def register(request):
	# setting up errors from models.py to actually display on webpage
	if request.method == 'GET':
		return redirect('/')
	errors = User.objects.basic_validation(request.POST)
	#making sure there isn't an empty field and will print error on homepage(index.html)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	#hashing/encrypting the password with bcrypt
	password = request.POST['password']
	pw_hash = bcrypt.hashpw(password.encode, bcrypt.gensalt()).decode()
	newuser = User.objects.create(
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		email = request.POST['email'],
		password = pw_hash,
		)
	request.session['user_id'] = newuser.id
	return redirect ('/userhome')

#this is users feed. Will have feed, options to edit profile, post, and etc. 
def userhome(request):
	#if 'user_id' not in request.session:
	#	return redirect('/')
	#user = User.objects.get(id=request.session['user_id'])
	#context = {
	#    'user': user
	#}
	return render(request, 'userhome.html')#, context)
