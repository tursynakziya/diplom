from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Барлық views функцияларын қолдану үшін

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Авторизация жүйесі (Login, Logout)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Тіркелу (Signup)
    path('signup/', views.signup, name='signup'), 
    
    # Платформа туралы (About) - осы жерге қосылды
    path('about/', views.about, name='about'),
    
    # Қолжетімділік баптаулары (Settings)
    path('settings/', views.settings_view, name='settings'),
    
    # Негізгі қолданбаның (core) ішкі сілтемелері
    path('', include('core.urls')),
]

# Медиа файлдарды (аудио/pdf) браузерде көрсету баптауы
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)