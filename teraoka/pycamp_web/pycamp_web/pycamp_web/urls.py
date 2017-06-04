"""pycamp_web URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
# from events.views import EventListView
from django.conf.urls.static import static
from django.conf import settings
import events.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),  # 正規表現 ^admin/ 文頭admin/ならOK ^admin/$ は文頭admin/aa はNG 文末/で終わり
    url(r'^events/', include(events.urls, namespace='events')),  # 他のurls.pyを読込ます処理を流します
    # include(events.urls)を 'events'という名前で読込みます
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)