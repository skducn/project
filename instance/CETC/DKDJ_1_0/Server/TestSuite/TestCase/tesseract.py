import pytesseract
from PIL import Image
image = Image.open('code3.png')
code = pytesseract.image_to_string(image)
print code