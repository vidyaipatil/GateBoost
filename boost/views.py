from django.shortcuts import render

# Create your views here.
def homepage(request):
    user = request.user
    return render(request, 'boost/homepage.html', {'user':user})

def about(request):
    return render(request, 'boost/about.html', {})

def help(request):
    return render(request, 'boost/help.html', {})
