from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from infra import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet)

register = views.UserViewSet.as_view({
    'post' : 'create'
})

login = views.UserViewSet.as_view({
    'post' : 'login'
})

logout = views.UserViewSet.as_view({
    'post' : 'logout'
})

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^', include(router.urls))
]
