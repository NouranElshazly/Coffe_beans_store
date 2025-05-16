from django.shortcuts import render

def about_us(request):
    return render(request, 'aboutus/aboutus.html')

# Create your views here.
