from django.shortcuts import render
from hotel.models import Hotel, Facility
from .models import Infographic
from .forms import GetInfographicForm
from PIL import Image, ImageDraw, ImageFont
from django.templatetags.static import static
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from .helpers import generateImage
from django.core.files import File
from django.core.files.base import ContentFile
from io import BytesIO

# Create your views here.

@csrf_exempt
def getInfographic(request, hotelId):
    if request.method == 'GET':
        try:
            hotelObject = Hotel.objects.get(pk=hotelId)
        except Hotel.DoesNotExist:
            hotelObject = None
    if hotelObject != None:
        facilityObjects = Facility.objects.filter(hotel=hotelObject)
    else:
        return JsonResponse({
            "success": False,
            "message": "Hotel with id " + str(hotelId) + " not found!",
            "infographicUrl": "null"
            })

    try:
        infographic = Infographic.objects.get(hotel = hotelObject)
    except Infographic.DoesNotExist:
        infographic = None

    if infographic == None:
        canvas = generateImage(hotelObject, facilityObjects)
        blob = BytesIO()
        canvas.save(blob, format='PNG')
        img_content = ContentFile(blob.getvalue(), 'infographic_'+hotelId+'.png')
        newInfographic = Infographic(name='Infographic ' + hotelObject.name, hotel=hotelObject, image=img_content)
        newInfographic.save()
        return JsonResponse({
            "success": True,
            "message": "OK",
            "infographicUrl": newInfographic.image.url
            })
    else:
        return JsonResponse({
            "success": True,
            "message": "OK",
            "infographicUrl": infographic.image.url
            })
        
    