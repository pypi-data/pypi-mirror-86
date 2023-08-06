"""ts_middle_ground_server URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from apps.users.views import AuthView, RefreshTokenView, RegisterView, LogoutView
from data_middle.utils.view_upload import CargoExcelUploadView

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'login/$', AuthView.as_view()),
    url(r'^token-refresh/$', RefreshTokenView.as_view(), name='token_refresh'),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^cargo-excel-upload/$', CargoExcelUploadView.as_view()),

    path('data-center/', include('data_middle.data_middle_platform_serve.urls')),
    # path('utility/', include('data_middle.utility.urls')),

]
