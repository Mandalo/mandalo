from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view_assign/', views.view_assign, name='view_assign'),
    url(r'^submit/', views.upload, name='upload')
]
