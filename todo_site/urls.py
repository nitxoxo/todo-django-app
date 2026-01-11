"""
URL configuration for todo_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from todo import views

# Optional: namespacing for future-proofing
app_name = "todo"

urlpatterns = [
    path('', views.index, name="index"),  # main todo list
    path('toggle/<int:id>/', views.toggle_complete, name="toggle"),  # mark complete
    path('del/<int:item_id>/', views.remove, name="del"),  # remove task
    path('register/', views.register_view, name="register"),  # register
    path('login/', views.Login_view, name="login"), 
    path('edit/<int:id>/', views.edit_task, name="edit"),
    path('logout/', views.Logout_view, name="logout"),  # logout
    path('admin/', admin.site.urls),  # admin
]


