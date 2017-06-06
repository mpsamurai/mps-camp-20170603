from django.conf.urls import url
from ratings.views import RatingsView


urlpatterns = [
   url(r'^$', RatingsView.as_view(), name='list'),

]