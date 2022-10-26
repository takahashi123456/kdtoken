from django.urls import path, include
from rest_framework import routers
from . import views
from . import apis

app_name = 'polls'

# router = routers.DefaultRouter()
# router.register('test', apis.test)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/', apis.api.as_view(), name='api'),
    path('api/<int:pk>', apis.DetailView.as_view(), name='detail'),
    path('test/', views.test, name='test'),
]
