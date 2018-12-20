from django.shortcuts import render
def home(request):
    return render(request, 'frontend/home.html')

def signup(request):
    return render(request, 'frontend/signup.html')