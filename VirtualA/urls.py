from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='signup.html'),  
    path('login/', views.login, name='login.html'),  
    path('home/', views.home, name='index.html'),  
    path('about/', views.about, name='about.html'),  
    path('service/', views.service, name='service.html'),  
    path('patient_search/', views.patient_search, name='patient_search.html'),  
    path('form/', views.form, name='form.html'),  
    path('results/', views.results, name='results.html'),  
    path('logout/', views.logout_view, name='logout'),  
    path('reset_link/', views.reset_link, name='reset.html'),
    path('new_pass/', views.new_pass, name="new_pass.html")  
]




