from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('group/<str:slug>/', views.group, name='group'),
    path('new/', views.new_post, name='new_post'),
    path("<username>/", views.profile, name="profile"),
    path("<username>/<post_id>/", views.post_view, name="post"),
    path("<username>/<post_id>/edit/", views.post_edit, name="post_edit"),
    path("<username>/<post_id>/comment/", views.add_comment, name="add_comment"),
]
