from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('braille/download/<str:filename>', views.braille_download, name='braille_download'),
    path('download/text/<int:file_id>/', views.download_text_file, name='download_text_file'),
    path('file/<int:file_id>/delete/', views.delete_user_file, name='delete_user_file'),
    path('signup/', views.signup, name='signup'), 
    path('profile/', views.profile, name='profile'),
    path('speech-to-text/', views.speech_to_text, name='speech_to_text'),
    path('transcribe-mic/', views.transcribe_mic, name='transcribe_mic'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/<int:user_id>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/files/<int:file_id>/delete/', views.admin_delete_file, name='admin_delete_file'),
    path('admin-panel/notify/', views.admin_send_notification, name='admin_send_notification'),
    path('admin-panel/settings/', views.admin_save_settings, name='admin_save_settings'),
    path('admin-panel/messages/<int:message_id>/mark/', views.admin_mark_message, name='admin_mark_message'),
    path('admin-panel/messages/<int:message_id>/reply/', views.admin_reply_message, name='admin_reply_message'),
    path('send-message/', views.send_message_to_admin, name='send_message_to_admin'),
    path('update-disability/', views.update_disability, name='update_disability'),
]
