"""manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import concept.views as views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'concept'


urlpatterns = [
    path("top/", views.TopArtView.as_view(), name="top"),
    path('create-checkout-session', views.create_checkout_session, name='create-checkout-session'),
    path('artdetail/<int:pk>', views.ArtDetail.as_view(), name='artdetail'),
    path('artistdetail/<int:pk>', views.ArtistDetail.as_view(), name='artistdetail'),
    path('admin/', admin.site.urls),
    path('follow/<int:pk>/', views.followPlace, name='follow'),  
    path('mypage/<int:pk>', views.UserDetail.as_view(), name='userdetail'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.TopArtView.as_view(), name="top"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<str:username>/delete/', views.UserDeleteView.as_view(), name='delete'),
    path('change/', views.UserChangeView.as_view(), name="change"),
    path('followpeople/<int:pk>/', views.followPeople, name='followpeople'), 
    path('search/', views.search, name='search'),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('remove/<int:pk>', views.RemoveView, name="remove"),
    path('return/<int:pk>', views.Returndef, name='return'),
    
    path('checkout/success', views.checkout_success_view, name='kessai'),
    path('webhook', views.checkout_success_webhook, name='checkout-success-webhook'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
