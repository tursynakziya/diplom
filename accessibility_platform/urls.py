from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

# Тіл ауыстыру үшін — тек осы жол i18n-сыз болуы керек
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # ← тіл ауыстыру
]

# Барлық беттер i18n_patterns ішінде болуы керек
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('settings/', views.settings_view, name='settings'),
    path('speech-to-text/', views.speech_to_text, name='speech_to_text'),
    path('', include('core.urls')),
    prefix_default_language=False  # қазақша үшін /kk/ префикс болмайды
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)