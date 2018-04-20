from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages

from datetime import datetime

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
    
    if len(request.POST['name']) < 3:
        messages.error(request, "Name must be 3 or more characters")
        error = True
    
    if len(request.POST['email']) < 3:
        messages.error(request, "Username must be 3 or more characters")
        error = True
    
   
    
    if len(request.POST['password']) < 8:
        messages.error(request,"Password must be 8 or more characters")
        error = True
    
    if request.POST['password'] != request.POST['c_password']:
        messages.error(request, "Passwords don't match")
        error = True

    if len(request.POST['dob']) == 0:
        messages.error(request, "Date hired required")
        error = True
    # else:
        # today = datetime.today()
        # my_bday = datetime.strftime[request.POST['dob'], "%Y-%m-%d"]

        # print my_bday < today

    # if not EMAIL_REGEX.match(request.POST['email']):
    #     messages.error(request,"email is invalid")
    #     error = True
   
    #check for unique email
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        messages.error(request, "Username taken")
        error = True


    
    if error:
        return redirect ('/')
    else:
        # create my user
        

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        
        the_user = User.objects.create(name = request.POST['name'], email = request.POST['email'],
         password = hashed_pw)
        # dob=datetime.strptime(request.POST['dob'],"%Y-%m-%d")

        print the_user
        
        # store them in session
        request.session['user_id'] = the_user.id

        # redirect to some success or inner page
        return redirect('/main')

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
            return redirect ('/main')
        else: 
            messages.error(request, "Email or password invalid")
        return redirect ('/')
    


def main(request):
    
    if not 'user_id' in request.session:
        messages.error(request, "Must be logged in to view")
        return redirect ('/')
    
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        # 'items': Item.objects.exclude(haters = User.objects.get(id= request.session['user_id'])),
        'items': Item.objects.all(),
        'my_items': Item.objects.filter(uploader = User.objects.get(id= request.session['user_id']),

        
        )
        
    }
    
    return render(request, 'login_app/main.html', context)

def logout(request):
    request.session.clear()
    return redirect ('/')

def add(request):
    if not 'user_id' in request.session:
        return redirect ('/')
    if request.method != 'POST':
        return redirect ('/main')
    
    #validations AREA

    Item.objects.create(label = request.POST['label'], uploader = User.objects.get(id = request.session['user_id'])) #manytomany is done differently

   

    return redirect ('/main')

def addnow(request):
    if not 'user_id' in request.session:
        return redirect ('/')
    if request.method != 'POST':
        return redirect ('/main')
    
    #validations AREA

    Item.objects.create(label = request.POST['label'], uploader = User.objects.get(id = request.session['user_id'])) #manytomany is done differently

   

    return render (request, '/main')


def edit(request, rec_id):
    context = {
        'items' : Item.objects.get(id = rec_id)
    }

    return render(request, 'login_app/edit.html', context)

def modify(request, rec_id):
    if request.method != 'POST':
        return redirect ('/main')
    
    # if not 'user_id' in request.session:
    #     return redirect ('/')
    
    items = Item.objects.get(id = rec_id)

    
    items.label = request.POST['label']
    items.save()

    return redirect ('/main')

def delete(request, rec_id):
    if not 'user_id' in request.session:
        return redirect ('/')
    
    Item.objects.get(id = rec_id).delete()
    return redirect ('/main')

def addwish(request, rec_id):
    if not 'user_id' in request.session:
        return redirect ('/')

    Item.objects.get(id = rec_id).items.add(User.objects.get(id = request.session['user_id']))
    return redirect ('/main')

def wishcreate(request):

    
    # Item.objects.create(artist = request.POST['artist'], album = request.POST['album'],
    # label = request.POST['label'], uploader = User.objects.get(id = request.session['user_id'])) #manytomany is done differently

    

    if not 'user_id' in request.session:
        messages.error(request, "Must be logged in to view")
        return redirect ('/')
    
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        # 'items': Item.objects.exclude(haters = User.objects.get(id= request.session['user_id'])),
        'items': Item.objects.all(),
        'my_items': Item.objects.filter(uploader = User.objects.get(id= request.session['user_id']),
        
        )
        
    }
    
    return render(request, 'login_app/add_item.html', context)


def wishview(request, rec_id):

    if not 'user_id' in request.session:
        messages.error(request, "Must be logged in to view")
        return redirect ('/')
    
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        # 'items': Item.objects.filter(haters = User.objects.get(id= request.session['user_id'])),
        'items': Item.objects.all(),
        'my_items': Item.objects.filter(uploader = User.objects.get(id= request.session['user_id']),
        
        )
        
    }
    
    return render(request, 'login_app/wish_items.html', context)

def addwish(request, rec_id):
   
    
    
    if not 'user_id' in request.session:
        messages.error(request, "Must be logged in to view")
        return redirect ('/')
    Item.objects.get(id = rec_id).items.add(User.objects.get(id = request.session['user_id']))

    

   
        
        
        
    
    
    return redirect ('/main')
    
    
    




        
        
        
        
        
        
        
        






    
    




