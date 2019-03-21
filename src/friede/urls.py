from django.conf.urls import url
from . import views

app_name = 'friede'
urlpatterns = [
    url( r'^.*$', views.index, name='index' ),

]
