from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def trades(request):
    return render(request, 'trades.html')

def analytics(request):
    return render(request, 'analytics.html')

def signal(request):
    return render(request, 'signal.html')

def pamm(request):
    return render(request, 'pamm.html')

def history(request):
    return render(request, 'history.html')
