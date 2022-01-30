import easyocr
from pylab import rcParams

rcParams['figure.figsize'] = 16, 16

def initialize_EasyOCR():
        global reader

        reader = easyocr.Reader(['en','th'])

def OCR_with_user_image(image):
        global reader

        output = reader.readtext(image)
        
        message_from_image = ""
        for message in range(0,len(output)):
                # print(output[message][1])

                message_from_image += output[message][1]

        # print(message_list)
        return message_from_image

initialize_EasyOCR()
        
