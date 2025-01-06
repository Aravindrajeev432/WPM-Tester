from django.urls import path
from . import views

app_name = 'speed_test'

urlpatterns = [
    path('', views.home, name='home'),
    path('get_text/', views.get_text, name='get_text'),
    path('save_result/', views.save_result, name='save_result'),
    path('results/', views.view_results, name='results'),
    path('mistakes/', views.view_mistakes, name='mistakes'),
    path('manage_words/', views.manage_words, name='manage_words'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
    path('custom_test/', views.custom_test, name='custom_test'),
    path('get_custom_text/', views.get_custom_text, name='get_custom_text'),
    path('delete_result/<int:result_id>/', views.delete_result, name='delete_result'),
]
