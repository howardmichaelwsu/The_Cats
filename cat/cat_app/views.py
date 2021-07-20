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
	pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
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
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	wallPost = WallPost.objects.all()
	context = {
	    'user': user,
	    'wallPost': wallPost,
	}
	return render(request, 'userhome.html', context)

# login from homepage
def login(request):
	#making a varibale by gabbing User model and filtering by email (can do username if you want)
	user = User.objects.filter(email=request.POST['email'])
	if user:
		#making variable logged_user into the user 
		logged_user = user[0]
		#grabbing hashed pw
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
			request.session['user_id'] = logged_user.id
			return redirect ('/userhome')
		#if login is messed up
		messages.error(request, 'Invaild Credentials')
		return redirect('/')
	messages.error(request, 'Email or password does not match our records')
	return redirect('/')

#logout function
def logout(request):
	request.session.flush()
	return redirect('/')

# Posting to wall from user to all feed
def wallPost(request):
	wallPost = request.POST['wallPost']
	errors = WallPost.objects.wallvalidate(wallPost)
	if len(errors) > 0:
		for key, val in errors.items():
			messages.error(request, val)
	user = User.objects.get(id=request.session['user_id'])
	WallPost.objects.create(postText = wallPost, user = user)
	return redirect('/userhome')

#comment under reviews
def comment(request):
	comment = request.POST['comment']
	wallPost_id = request.POST['wallPost_id']
	user = User.objects.get(id=request.session['user_id'])
	wallPost = Review.objects.get(id=wallPost_id)
	Comment.objects.create(comment = comment, user = user, postText = wallPost)
	return redirect('/userhome')

# Like button, many-to-many
def likes(request, id):
	liked_post = WallPost.objects.get(id=id)
	likes = User.objects.get(id=request.session['user_id'])
	liked_post.likes.add(likes)
	return redirect('/userhome')
	
