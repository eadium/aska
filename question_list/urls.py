from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'question_list'
urlpatterns = [
    path('', views.listing, name='index'),
    path('ask', views.ask, name='ask'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('tag/<str:tag>', views.tag, name='tag'),
    path('tag', views.tag, name='tag'),
    
    path('question/<int:question_id>', views.question_view, name='question'),
    path('question', views.question_view, name='question'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)