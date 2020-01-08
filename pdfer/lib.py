from PIL import Image, ImageDraw, ImageFont
import os

def get_text_size(text, font_size):
    image = Image.new('RGB', (512, 256), (255, 255, 255))   
    drawer = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('times.ttf', font_size)
    if os.name == "nt":
        fnt = ImageFont.truetype('times.ttf', font_size)
    else:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")
    
    size = drawer.textsize(text.replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"), font=fnt)
    return size[0]
