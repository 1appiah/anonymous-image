from django.urls import path

from . import views


urlpatterns = [
    path('register/',views.CustomUserCreate.as_view(),name='create_user'),
    path('all-authors/',views.AllAuthors.as_view(),name='all-users'),

]
