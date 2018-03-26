
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/(?P<id>\d+)$', views.show_item),
    url(r'^wish_items/(?P<id>\d+)/delete$', views.delete_item),
    url(r'^wish_items/create$', views.create_item),
    url(r'^add_item$', views.add_item),
    url(r'^wishlist_add/(?P<id>\d+)$', views.wishlist_add),
    url(r'^wishlist_remove/(?P<id>\d+)$', views.wishlist_remove),
    url(r'^logout$', views.logout),
    url(r'^process$', views.process)
]