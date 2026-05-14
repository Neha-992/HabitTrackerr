from django.urls import path
from . import views

urlpatterns = [

    path('add-habit/', views.add_habit, name='add_habit'),

    path('delete-habit/<int:id>/',
         views.delete_habit,
         name='delete_habit'),

    path('complete-habit/<int:id>/',
         views.complete_habit,
         name='complete_habit'),

    path('edit-habit/<int:id>/',
         views.edit_habit,
         name='edit_habit'),
]