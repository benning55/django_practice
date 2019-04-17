from django.urls import path

from . import views

urlpatterns = [
  path('index/', views.index, name='index'),
  path('detail/<int:poll_id>/', views.detail, name='detail'),
  path('create/', views.create, name='create_poll'),
  path('comment/', views.comment, name='create_comment'),
  path('login/', views.my_login, name='login'),
  path('logout/', views.my_logout, name='logout')
]
