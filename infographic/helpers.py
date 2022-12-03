from PIL import Image, ImageDraw, ImageFont
from hotel.models import Hotel, Facility
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generateImage(hotel, facilities):
    canvasUrl = static('hotel-background.png')
    canvas = Image.open(imgUrl)

    # Local testing
    # canvas = Image.open('E:\\RPL\\TK-RPL\static\hotel-background.png')

    # Font preferences
    titleFont = ImageFont.truetype('arial.ttf', 45)
    subtitleFont = ImageFont.truetype('arial.ttf', 30)
    descriptionFont = ImageFont.truetype('arial.ttf', 20)
    fontColor = (100, 41, 2)

    width, height = canvas.size
    draw = ImageDraw.Draw(canvas)

    # Draw hotel name
    hotelName = hotel.name
    textWidth, textHeight = draw.textsize(hotelName, font=titleFont)
    xText = (width - textWidth) / 2
    yText = 135
    draw.text((xText, yText), hotelName, font=titleFont, fill = fontColor)

    # Draw facility Header
    textWidth, textHeight = draw.textsize("Fasilitas", font=titleFont)
    xText = (width - textWidth) / 2
    yText = 420
    draw.text((xText, yText), "Fasilitas", font=titleFont, fill = fontColor)

    # Draw facilities
    yText = 430
    for facility in facilities:
        # Draw facility name
        facility_name = '- ' + facility.name
        xText = 90
        yText = yText + 33
        draw.text((xText, yText), facility_name, font=subtitleFont, fill = fontColor)

        # Draw facility description
        facility_description = facility.description
        xText = 110
        yText = yText + 30
        draw.text((xText, yText), facility_description, font=descriptionFont, fill = fontColor)
    return canvas
