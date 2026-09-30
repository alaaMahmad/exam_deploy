from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('shows', views.shows, name='shows'),
    path('create', views.create_show, name='create_show'),
    path('edit/<int:id>', views.edit_show, name='edit_show'),
    path('view/<int:id>', views.view_show, name='view_show'),
    path('delete/<int:id>', views.delete_show, name='delete_show'),


    path('add/comment/<int:id>', views.add_comment, name='add_comment'),
    path('delete/comment/<int:id>/<int:show_id>', views.delete_comment),
    
]