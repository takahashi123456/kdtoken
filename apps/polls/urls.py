from django.urls import path
from . import views
from . import apis

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/', apis.api.as_view(), name='api'),
    path('api/<int:pk>', apis.DetailView.as_view(), name='detail'),
]
