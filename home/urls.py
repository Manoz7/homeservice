from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    
    path('login/', views.handleLogin, name='login'),
    path('user_register/', views.user_register, name='user_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('logout/', views.handleLogout, name='logout'),
    
    # Services
    path('services/', views.services, name='services'),
    path('services/<int:myid>/', views.serviceView, name='serviceView'),
    path('add_service/', views.addService, name='add_service'),
    
    path('book_service/', views.book_service, name='book_service'),
    path('tracker/', views.tracker, name='tracker'),

   
    # User Profile
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile/', views.profile, name='profile'),

    
    # Admin Panel
    path('admin_home/', views.admin_home, name= 'admin_home'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('all_services/', views.allServices, name= 'allservices'),
    path('all_users/', views.allUsers, name= 'allusers'),
    path('all_customers/', views.allCustomers, name= 'allcustomers'),
    path('feedback/', views.feedback, name='feedback'),
    
    path('admin_profile/', views.adminProfile, name= 'admin_profile'),
    path('edit_admin/<int:pid>', views.editAdmin, name= 'edit_admin'),
    path('changeadminpass/<int:pid>', views.changeAdminpass, name= 'changeadminpass'),

    # CRUD function
    path('editservices/<int:pid>', views.editServices, name= 'editservices'),
    path('deleteService/<int:myid>', views.deleteService, name='deleteService'),
    path('deleteCustomer/<int:myid>', views.deleteCustomer, name='deleteCustomer'),
    path('deleteUser/<int:myid>', views.deleteUser, name='deleteUser'),

]