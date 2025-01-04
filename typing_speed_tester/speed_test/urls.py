from django.urls import path
from . import views

app_name = 'speed_test'

urlpatterns = [
    path('', views.home, name='home'),
    path('get_text/', views.get_text, name='get_text'),
    path('save_result/', views.save_result, name='save_result'),
    path('manage_words/', views.manage_words, name='manage_words'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
    path('results/', views.view_results, name='results'),
]
