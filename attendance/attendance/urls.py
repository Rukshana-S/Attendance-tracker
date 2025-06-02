from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
path('admin/', admin.site.urls),
path('', include('myapp.urls')),
path('export-defaulters/', views.export_defaulter_pdf, name='export_defaulter_pdf'),
path('export-attendance/', views.export_attendance_pdf, name='export_pdf'),

]
