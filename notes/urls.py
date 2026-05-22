from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),

    path('register/', views.register_view, name='register'),

    path('logout/', views.logout_view, name='logout'),

    path('add-note/', views.add_note, name='add_note'),

    path('note/<int:id>/', views.note_detail, name='note_detail'),

    path('edit-note/<int:id>/', views.edit_note, name='edit_note'),

    path('delete-note/<int:id>/', views.delete_note, name='delete_note'),

    path('summary/<int:id>/', views.generate_summary, name='generate_summary'),

    # API JSON
    path('api/notes/', views.api_notes, name='api_notes'),

]