from django.conf.urls import url
from DSS import views

urlpatterns=[
	url(r'^magazine/$',views.main, name='main'),]
