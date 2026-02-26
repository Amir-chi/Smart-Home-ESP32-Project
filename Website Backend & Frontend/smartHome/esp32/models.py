from django.db import models



class Esp32Picture(models.Model):
    image = models.ImageField(upload_to='esp32_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class CommandHistory(models.Model):
    command = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class LedStatus(models.Model):
    led_name = models.CharField()
    led_status = models.CharField()