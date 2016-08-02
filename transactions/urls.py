from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from transactions import views

app_name = 'transactions'
urlpatterns = [
    url(r'^$', views.TransactionList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.TransactionDetail.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
