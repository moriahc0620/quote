from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes), # dashboard/homepage
    url(r'^add_to_list$', views.add_to_list), # feature to add to my best from quotable quotes
    url(r'^remove_from_list$', views.remove_from_list), # feature to remove from my favorites
    url(r'^users/(?P<quote_id>\d+)$', views.quotes), # feature for other user's page
    url(r'^contribute_quote$', views.contribute_quote),
]
