from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.cache import cache_control
from . models import UserAuth, AdminSuper, DeletedUser, UpdatedUser
import secrets


# Log in function
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def log_in_page(request):

  # setting a flag to authenticate user input(username and password) matches or not
  pass_valid = {'mismatch': False}
  
  # checking user or Admin already logged in or not using session.
  # UserAuth is a DB relation stores user data.
  if UserAuth.objects.filter(username=request.session.get('username')).exists():
    return redirect(home_page)
  
  # AdminSuper is a DB relation stores admin data.
  if AdminSuper.objects.filter(username=request.session.get('username')).exists():
    return redirect(admin_page)
  
  if request.method=='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    # checking user input with user data in DB for Authentication.
    if UserAuth.objects.filter(username=username ,password=password).exists():
      request.session['username'] = username  # Entering user info to Session.
      return redirect(home_page)
    
    elif AdminSuper.objects.filter(username=username ,password=password).exists():
      request.session['username'] = username  # Entering Admin info to Session.
      return redirect(admin_page)
    
    # change flag to inticate username or password mis matches
    else:
      pass_valid['mismatch'] = True

  return render(request, 'login.html', pass_valid)



# function to create a user. Used in Sign Up and admin's Add option
def create_new_user(request):

  # setting some flags
  status = {
    'empty': False,
    'space': False,
    'exists': False,
    'limit': False,
    'mismatch': False,
    'success' : False,
    'update': False
    }
  
  # user submited data
  uname= request.POST.get('username')
  email= request.POST.get('email')
  pass1= request.POST.get('password')
  pass2= request.POST.get('repassword')
  country= request.POST.get('country')

  # If anything went wrong, changes flag value and returns it.
  if uname == None or email == None or pass1 == None or uname == '' or email == '' or pass1 == '':
    status['empty'] = True
    return status
  
  elif ' ' in uname or ' ' in email:
    status['space'] = True
    return status

  elif AdminSuper.objects.filter(username=uname).exists() or AdminSuper.objects.filter(email=email).exists() or UserAuth.objects.filter(username=uname).exists() or UserAuth.objects.filter(email=email).exists():
    status['exists'] = True
    return status
  
  elif len(pass1)<8:
    status['limit']= True
    return status

  elif pass1 != pass2:
    status['mismatch'] = True
    return status
  
  # If nothing goes wrong. Create new user and return success.
  else:
    new_user = UserAuth(username=uname, email=email, password=pass1, country=country)
    new_user.save()
    status['success'] = True
    return status



# Sign Up page
def sign_up_page(request):

  # checking user or Admin already logged in or not using session.
  if UserAuth.objects.filter(username=request.session.get('username')).exists():
    return redirect(home_page)
  
  if AdminSuper.objects.filter(username=request.session.get('username')).exists():
    return redirect(admin_page)

  if request.method=='POST':
    # calling function Create New User.
    response= create_new_user(request)

    # checking user creation is success or not.
    if response['success']:
      return redirect(log_in_page)
    
    else:
      return render(request, 'signup.html', response) 
     
  return render(request, 'signup.html')


# Users Home page
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def home_page(request, page = 'home'):

  # Checking user logged in or not, using Session. Authentication.
  if UserAuth.objects.filter(username=request.session.get('username')).exists():

    # fetching logged user's data from DB.
    user_info = UserAuth.objects.get(username= request.session.get('username'))
    # if user's country info is not added, to add country.
    if request.method == 'POST':
      user_info.country = request.POST.get('country')
      user_info.save()

    home = {
      'user_info': user_info,
      'page': page,
      }
    
    return render(request, 'home.html', home)

  return redirect(log_in_page)


# Admin's Home page
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_page(request, check= 'available_list'):

  # Checking Admin logged in or not, using Session. Authentication.
  if AdminSuper.objects.filter(username=request.session.get('username')).exists():

    # fetching datas from DB tables.
    available_info = UserAuth.objects.all()
    update_info = UpdatedUser.objects.all()  # UpdatedUser is a DB relation stores Updated users info
    delete_info = DeletedUser.objects.all()  # DeletedUser is a DB relation stores Deleted users info

    # checking user wants list of 'available users' or 'deleted users' or 'updated users'
    if check == 'available_list':
      # search
      if request.POST:
        searcher = request.POST.get('search')
        user_info = UserAuth.objects.filter(username__icontains=searcher).values()
      # all data
      else:
        user_info = available_info

    elif check == 'deleted_list':
      # search
      if request.POST:
        searcher = request.POST.get('search')
        user_info = DeletedUser.objects.filter(username__icontains=searcher).values()
      # all data
      else:
        user_info = delete_info

    else:
      # search
      if request.POST:
        searcher = request.POST.get('search')
        user_info = UpdatedUser.objects.filter(username__icontains=searcher).values()
      # all data
      else:
        user_info = update_info
    
    # country wise data for dougnut graph
    values = {}
    color ={}
    for i in available_info:
      values[i.country] = values.get(i.country,0) + 1
      # different colors for dougnut graph
      color[i.country] = f'#{secrets.token_hex(3)}'

    all_info = {
      'check': check,
      'user_info': user_info,
      'available_count': len(available_info),
      'delete_count': len(delete_info),
      'update_count': len(update_info),
      'doughnut_values': values,
      'doughnut_color': color
      }
    
    return render(request, 'admin.html', all_info)
  
  return redirect(log_in_page)


# Log Out function for both User's and Admin's Home.
def log_out(request):
  # checking user logged in or not. Authentication.
  if 'username' in request.session:
    request.session.flush()  # clearing user info from Session

  return redirect(log_in_page)


# Add User Feature only for Admin
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_user(request):

  # checking user logged in or not. Authentication.
  if 'username' in request.session:

    if request.method == 'POST':
      # calling function Create New User.
      response= create_new_user(request)

      # checking user creation is success or not.
      if response['success']:
        return redirect(admin_page)
      
      else:
        return render(request, 'admin_add.html', response)
      
    return render(request, 'admin_add.html')

  return redirect(log_in_page)


# Delete User Feature only for Admin
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_user(request, id):

  # checking user logged in or not. Authentication.
  if 'username' in request.session:

    # fetching user data to be deleted.
    obj = UserAuth.objects.get(pk = id)
    # Inserting the deleting user's data to another table.
    to_delete_obj = DeletedUser(username=obj.username, email=obj.email, password=obj.password, country=obj.country)
    to_delete_obj.save()
    # deleting the user's data
    obj.delete()
    return redirect(admin_page)

  return redirect(log_in_page)


# Update User Feature only for Admin
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_user(request, id):

  # checking user logged in or not. Authentication.
  if 'username' in request.session:

    # fetching user data to be updated.
    obj = UserAuth.objects.get(id = id)

    response = {
      'update': True,
      'details': obj
      }
    
    if request.POST:
      # Inserting the updating user's data to another table.
      to_update_obj = UpdatedUser(username=obj.username, email=obj.email, password=obj.password, country=obj.country)
      to_update_obj.save()
      updated_user_name = request.POST.get('username')
      updated_email = request.POST.get('email')
      updated_country = request.POST.get('country')
      # updating the user's data
      obj.username, obj.email, obj.country = updated_user_name, updated_email, updated_country
      obj.save()
      return redirect(admin_page)
      
    return render(request, 'admin_add.html', response)
  
  return redirect(log_in_page)
