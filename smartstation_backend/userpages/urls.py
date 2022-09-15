from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.UserLogin.as_view(), name="login"),
    # path('<slug:slug>/', views.UserView.as_view(), name='userdetail'),
    path('userview/', views.userview, name='userdetail')

]