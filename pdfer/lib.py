from PIL import Image, ImageDraw, ImageFont
def get_text_size(text, font_size):
    image = Image.new('RGB', (512, 256), (255, 255, 255))   
    drawer = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('Helvetica.ttf', font_size)
    
    size = drawer.textsize(text.replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"), font=fnt)
    return size[0]
