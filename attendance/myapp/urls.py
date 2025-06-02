from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('records/', views.view_attendance, name='view_attendance'),
    path('summary/', views.attendance_summary, name='summary'),
    path('export/', views.export_pdf, name='export_pdf'),

]

