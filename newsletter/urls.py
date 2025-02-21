from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('recipient/', views.home_page, name='home_page'),
    path('', views.recipient_list, name='recipient_list'),
    path('add/', views.recipient_add, name='recipient_add'),
    path('<int:pk>/edit/', views.recipient_edit, name='recipient_edit'),
    path('<int:pk>/delete/', views.recipient_delete, name='recipient_delete'),
]
