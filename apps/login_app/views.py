from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages

import re
import bcrypt

from models import *   #import from models




EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    return render(request, 'login_app/index.html')
    
def register(request):
    # print request.POST #same as a dictionary
    error = False
    
    if len(request.POST['first_name']) < 2:
        messages.error(request, "First name must be 2 or more characters")
        error = True
    
    if len(request.POST['last_name']) < 2:
        messages.error(request,"Last name must be 2 or more characters")
        error = True
    
    if len(request.POST['password']) < 8:
        messages.error(request,"Password must be 8 or more characters")
        error = True
    
    if request.POST['password'] != request.POST['c_password']:
        messages.error(request, "Passwords don't match")
        error = True

    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,"email is invalid")
        error = True
   
    #check for unique email
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        messages.error(request, "Email taken")
        error = True


    
    if error:
        return redirect ('/')
    else:
        # create my user
        

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        
        the_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw)

        print the_user
        
        # store them in session
        request.session['user_id'] = the_user.id

        # redirect to some success or inner page
        return redirect('/success')

def login(request):
        # SELECT * FROM users WHERE email = my_email, password = my_password //can't check both, check one at a time
        
        # #alternative method
        the_user_list = User.objects.filter(email = request.POST['email'])
        if len(the_user_list) > 0:
            # [{}]
            the_user = the_user_list[0]
        else:
            messages.error(request, "Email or password invalid")
            return redirect ('/')
        # try:
        #     the_user = User.objects.get(email = request.POST['email'])
        # except:
        #     messages.error(request, "Email or password invalid")
        #     return redirect ('/')

        
        if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
            request.session['user_id'] = the_user.id
            return redirect ('/success')
        else: 
            messages.error(request, "Email or password invalid")
        return redirect ('/')
    


def success(request):
    
    if not 'user_id' in request.session:
        messages.error(request, "Must be logged in to view")
        return redirect ('/')
    
    context = {
        'user' : User.objects.get(id = request.session['user_id'])
    }
    
    return render(request, 'login_app/success.html', context)

def logout(request):
    request.session.clear()
    return redirect ('/')


        
        
        
        
        
        
        
        






    
    




