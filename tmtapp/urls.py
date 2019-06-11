"""tutorial URL Configuration

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
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from . import views, views_file, views_app_update

urlpatterns = [
    # 提BUG页面操作
    path('product/', views.ProductObject.as_view()),
    path('product/<int:product_id>/project/', views.ProjectObject.as_view()),
    path('user/', views.UserObject.as_view()),
    path('bug/', views.BugObject.as_view()),

    # 文件上传、下载
    path('files/', views_file.FileUploadObject.as_view()),
    path('bugfiles/', views_file.FileUploadBugObject.as_view()),

    # app更新
    path('appupdate/', views_app_update.AppUploadObject.as_view()),
    path('apphistory/', views_app_update.AppHistoryObject.as_view()),

]
