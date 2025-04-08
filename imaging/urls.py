from django.urls import path
from . models import Message

from . import views
urlpatterns = [
    path('<int:pk>',views.CreateImages.as_view(),name='images'),
    path('boss/<int:pk>',views.Boss.as_view(),name='boss'),
    path('view-image/',views.ViewImage.as_view(),name='view-image'),
    path('dashboard/',views.Dashboard.as_view(),name='dashboard'),
    path('delete-image/<int:pk>',views.delete_image,name="delete-image")    
]
