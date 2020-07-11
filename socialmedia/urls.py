"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from connect.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Front,name='front'),
    path('login/',Login,name="login"),
    path('logout/',Logout,name="logout"),
    path('Register/',Register,name="register"),
    path('in/<str:Username>/',UserProfile,name="UserProfile"),
    path('in/Edit/<str:Username>/', Update_User_Details, name = "UpdateUserProfile"),


    path('all_professionals/<str:what>/',All_Profession,name="professional"),
    path('connection/<str:action>/<int:u_id>/',Manage_your_connections, name="connections"),
    path('add_company/', Add_Company, name = "addCompany"),
    path('your_company_details/', CompanyDetails, name = "CompanyDetails"),
    path('post_new_blog/', NewPost, name = "post"),
    path('likes/<int:b_id>/<str:Username>/', Like_By_Me, name = "likes")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
