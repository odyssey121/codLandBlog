from django.conf.urls import url
from django.urls import include

from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^add_article/', views.add_article, name="add_article"),
    url(r'^register/', views.register, name="register"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout"),
    # url(r'^up_down/', views.up_down),
    # url(r'^comment/', views.comment),
    # url(r'^comment_tree/(\d+)/', views.comment_tree),
    # url(r'^(\w+)/article/(\d+)/$', views.article_detail),
    url(r'^$', views.home, name="home")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
