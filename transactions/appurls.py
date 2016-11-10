from django.conf.urls import url

from transactions import views

app_name = 'app_transactions'
urlpatterns = [
    url(r'^$', views.app, name='app'),
]
