#!/usr/bin/env python
# import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
from WatermarkImage import WatermarkImage

#file_path = raw_input("Please enter file path")
#users_message = raw_input("Please enter your message")

file_path = 'lena.bmp'
users_message = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

img = WatermarkImage(file_path, users_message)
img.write_watermark()
#####################################################################

#file_with_message_path = raw_input("Please enter file path")

#img_with_message_path = 'img_with_message.jpeg'

#img_to_decode = WatermarkImage()

#img_to_decode.set_img_with_message(img_with_message_path)

#img_to_decode.read_watermark()

img.read_watermark()
#####################################################################
img.write_all_images_to_files()

print img.message_detected
