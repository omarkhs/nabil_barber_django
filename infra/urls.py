from django.conf.urls import url
from infra import views

urlpatterns = [
    url(r'^user/$', views.user_view),
]
