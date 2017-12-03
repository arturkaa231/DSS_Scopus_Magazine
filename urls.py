from django.conf.urls import url
from DSS import views

urlpatterns=[
	url(r'^magazine/$',views.main, name='main'),
	url(r'^download_file/$',views.download_file, name='download_file')]
