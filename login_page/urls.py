from django.urls import path
from . import views

# <check>, <page>, <id> for sending some arguments to related functions
urlpatterns = [
    path('',views.log_in_page, name='login'),
    path('login/',views.log_in_page, name='login'),
    path('signup/',views.sign_up_page, name='signup'),
    path('Superadmin/', views.admin_page, name='super_admin'),
    path('Superadmin/<check>', views.admin_page, name='super_admin'),
    path('home/',views.home_page, name='home'),
    path('home/<page>',views.home_page, name='home'),
    path('logout/', views.log_out, name='logout'),
    path('add/',views.add_user, name= 'addUser'),
    path('delete/<id>',views.delete_user, name= 'deleteUser'),
    path('update/<id>',views.update_user, name= 'updateUser'),
]