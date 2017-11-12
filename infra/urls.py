from django.conf.urls import url
from infra import views

urlpatterns = [
    url(r'^userslist/$', views.users_list),
]
