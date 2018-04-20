from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^main', views.main),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^addwish/(?P<rec_id>\d+)$', views.addwish),
    url(r'^edit/(?P<rec_id>\d+)$', views.edit),
    url(r'^edit/(?P<rec_id>\d+)/confirm$', views.modify),
    url(r'^delete/(?P<rec_id>\d+)$', views.delete),
    # url(r'^hate/(?P<rec_id>\d+)$', views.hate),
    url(r'^wish_items/create$', views.wishcreate),
    url(r'^wish_items/(?P<rec_id>\d+)$', views.wishview),
    url(r'^add/(?P<rec_id>\d+)$', views.add),


    

]