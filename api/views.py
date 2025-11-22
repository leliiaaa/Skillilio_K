from django.shortcuts import render

# Головна сторінка 
def index(request):
    return render(request, 'index.html')

# Сторінка авторизації 
def auth_page(request):
    return render(request, 'auth.html')