from django.conf.urls import url
# from accounts.views import
from django.contrib.auth import views as auth_views

urlpatterns = [
   url(r'^login$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'), # ログイン機能はあるけどテンプレートがないので作る

]