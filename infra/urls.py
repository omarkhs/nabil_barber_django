from django.conf.urls import url
from infra import views

urlpatterns = [
    url(r'^register/$', views.register_view),
    url(r'^login/$', views.login_view),
    # added the url for logout view
    url(r'^logout/$', views.logout_view),
    url(r'^user/$', views.user_view),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_view),
]
