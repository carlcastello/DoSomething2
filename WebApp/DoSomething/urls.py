# from django.contrib.auth.views import login, logout
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^id=(?P<id>[0-9a-zA-Z-_ ]+)&type=(?P<category>[a-zA-Z_ ]+)/$', views.DetailView.as_view(), name="detail_view"),
    url(r'^events/$', views.EventView.as_view(), name="event_view"),
    url(r'^events/lat=(?P<latitude>[0-9.-]+)lng=(?P<longitude>[0-9.-]+)$', views.EventView.as_view(), name="event_view"),
    url(r'^categories/$', views.CategoriesView.as_view(), name="categories_view"),
    url(r'^categories/(?P<type>[a-zA-Z_ ]+)/$', views.CategoryListView.as_view(), name="categories_list_view"),

    # url(r'^update-database/$', views.UpdateView.as_view(), name="update_view"),
    url(r'^initialize-database/$', views.InitializeView.as_view(), name="initialize_view"),
    url(r'^delete-database/$', views.DeleteView.as_view(), name="initialize_view"),
]