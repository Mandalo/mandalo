from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view_assgn/', views.view_assgn, name='view_assgn')
]
