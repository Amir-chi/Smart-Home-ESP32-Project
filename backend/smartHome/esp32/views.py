import json
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import logging

from .services import extranct_command_from_picture , extract_command_from_text , extract_command_from_voice 
from .models import Esp32Picture , LedStatus , CommandHistory
from .utils import set_led_status , process_and_send_commands


logger = logging.getLogger(__name__)

LED_NAMES = ["led0" , "led1" , "led2" , "led3"]

class ReceiveMessage(View):
    
    template_name = "esp32/main.html"
    
    def get(self , request):
        
        return render(request , self.template_name)    
       
    
    def post(self , request):
        
        channel_layer = get_channel_layer()
        
        textInput = request.POST.get("command")
        image_input = request.FILES.get("image")
        voice_input = request.FILES.get("audio")
        

        try :
            if textInput:
                command = extract_command_from_text(textInput).choices[0].message.content
                process_and_send_commands(command , channel_layer)

            if image_input:
                command = extranct_command_from_picture(image_input.read())
                process_and_send_commands(command , channel_layer)
                
            if voice_input:
                command = extract_command_from_voice(voice_input).choices[0].message.content
                process_and_send_commands(command , channel_layer)
        
        except Exception as e:
            logger.error(f"Error processing input: {e}")
              
        return render(request , self.template_name)
    
    
    
class ReceiveBotMessage(APIView):
    
    
    def post(self , request):

        channel_layer = get_channel_layer()
        data_type = request.data.get("type")
        data = request.data
        
        try : 
            
            if data_type == "command":
                self._handle_command(data , channel_layer)
                    
            if data_type == "text":
                
                command = extract_command_from_text(data.get("data")).choices[0].message.content
                process_and_send_commands(command , channel_layer)
                
            if data_type == "voice":
                command = extract_command_from_voice(data.get("voice")).choices[0].message.content
                process_and_send_commands(command , channel_layer)
        
        except Exception as e:
            logger.error(f"Bot message error: {e}")
            return Response({"result": "failed", "error": str(e)}, status=400)    
            
        return Response({"result" : "success"})
    
    
    def _handle_command(self, data: dict, channel_layer) -> None:
        
        action = data.get("action", "")

        if "flash" in action:
            set_led_status(action)

        if action == "capture":
            
            payload = {k: v for k, v in data.items() if k != "type"}
            
            async_to_sync(channel_layer.group_send)(
                'chat', {'type': 'message',
                         'message': payload}
            )
            
            async_to_sync(channel_layer.group_send)(
                'bot_group',
                {'type': 'send_text', 
                 'content': 
                     {'status': 'processing',
                      'message': 'Request sent to ESP32'}}
            )
            
                
        else:
            
            async_to_sync(channel_layer.group_send)(
                'chat',
                {'type': 'message', 
                 'message': {'action': action}}
            )
    

def get_latest_photo(request):

    image = Esp32Picture.objects.order_by("created_at").last()
    
    if not image : 
        return JsonResponse({'status': 'error', 'message': 'No image found'}, status=404)
      
    
    return JsonResponse({
        'status': 'success',
        'image_url': image.image.url
    })
        
    
    
    

def get_led_status(request):
    statuses = LedStatus.objects.filter(led_name__in=LED_NAMES).values("led_name", "led_status")
    response = {item["led_name"]: item["led_status"] for item in statuses}
    print(response)
    return JsonResponse(response)


def get_history(request):
    history = CommandHistory.objects.order_by("-created_at").values("id", "command", "created_at")
    history_list = [
        {
            "id": item["id"],
            "command": item["command"],
            "timestamp": item["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        }
        for item in history
    ]
    return JsonResponse(history_list, safe=False)