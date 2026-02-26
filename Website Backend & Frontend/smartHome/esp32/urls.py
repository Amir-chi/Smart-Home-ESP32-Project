from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("" , views.ReceiveMessage.as_view()),
    path("get_picture/", views.get_latest_photo),
    path("api/receive_message/" , views.ReceiveBotMessage.as_view()),   
    path("get_led_status/" , views.get_led_status),
    path("api/get_history/" , views.get_history),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)