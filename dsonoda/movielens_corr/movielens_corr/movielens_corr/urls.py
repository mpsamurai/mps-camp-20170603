"""movielens_corr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

import d3js_graph_movie_rating.urls
import test_sync.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^d3js_graph_movie_rating/', include(d3js_graph_movie_rating.urls, namespace='d3js_graph_movie_rating')),
    url(r'^test_sync/', include(test_sync.urls, namespace='test_sync')),
]
