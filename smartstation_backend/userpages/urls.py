from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/<int:devID>', views.UserLogin.as_view(), name="login"),
    # path('<slug:slug>/', views.UserView.as_view(), name='userdetail'),
    path('userview/', views.UserView, name='userdetail'),
    path('signup/',views.signup,name='signup')

]