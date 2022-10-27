from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView    
from django.views import generic
# from .models import UserModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect






def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = form.save()
            login(request, user)
    
            return render(request, 'UserPage.html', {
                'user':user
                
            })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewUserForm()

    return render(request, 'Register.html', {'form': form})



# def index(request):
#     return HttpResponse("Hello, world. ")


class UserLogin(LoginView):
    # template_name = 'userpages/LoginView_form.html'
    

    template_name = 'LoginView_form.html'
 
    def get(self, request, *args, **kwargs):
        self.devId= kwargs['devID']
        return render(request, self.template_name, 
        {'form': LoginForm({'DevId':self.devId}),
        'devId':self.devId}
        )
    
   


    # next_page = 'userdetail'




def UserView(request):
    username = request.POST.get('username', )
    password = request.POST.get('password', )
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
        return render(request, 'UserPage.html', {
            'user':user
            
        })
        # return render(request, 'index.html', {
        #     'user':user
            
        # })

    else:
        return HttpResponse("You need to login!")


