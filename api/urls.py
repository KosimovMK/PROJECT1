from django.urls import path

from . import views

urlpatterns = [
    path('notes/', views.get_notes),  # localhost:8000/api/notes/
    path('notes/new/', views.create_note),
    path('notes/<uuid:id>/', views.note_detail),

    path('users/', views.get_users),
    path('users/new/', views.create_user),
    path('users/<int:id>/', views.user_detail),
]
