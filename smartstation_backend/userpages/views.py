from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView    
from django.views import generic
# from .models import UserModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required





def index(request):
    return HttpResponse("Hello, world. ")




class UserLogin(LoginView):
    template_name = 'userpages/LoginView_form.html'
    # next_page = 'userdetail'


# class UserView(generic.DetailView):
#     # model = UserModel

#     template_name = 'userpages/userpage.html'
#     def get_queryset(self):
#         pass


def userview(request):
    username = request.POST.get('username', )
    password = request.POST.get('password', )
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
        # return render(request, 'userpages/userpage.html', {
        #     'user':user
            
        # })
        return render(request, 'index.html', {
            'user':user
            
        })

    else:
        return HttpResponse("You need to login!")


