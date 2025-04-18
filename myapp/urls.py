from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Made login the root URL
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('trades/', views.trades, name='trades'),
    path('analytics/', views.analytics, name='analytics'),
    path('signal/', views.signal, name='signal'),
    path('pamm/', views.pamm, name='pamm'),
    path('history/', views.history, name='history'),
]






