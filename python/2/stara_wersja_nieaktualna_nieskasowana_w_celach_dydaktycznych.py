import numpy as np
#import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import random

# Load an color image in grayscale
img = cv2.imread('lena.bmp',0)
new_img = img

key_word = "Budapeszt"

key_word_numbers = []
for i in range(512+1):
	letter = key_word[i%len(key_word)]
	nr_in_ascii = ord(letter)
	key_word_numbers.append(nr_in_ascii)

message ="c_h_r_omodynamikaKwantowachromodynamikaKwantowa"
message_binary = ""
message_numbers = []

for c in message:
	temporary_binary = bin(ord(c))
	message_binary += temporary_binary[2:]

for c in message_binary:
	message_numbers.append(int(c))

for i in range(len(message_numbers)):
	y = key_word_numbers[i]
	if message_numbers[i] == 0:
		new_img[i,y] = 255
	else:
		new_img[i,y] = 0

cv2.imshow('image',new_img)
cv2.waitKey(1000)
cv2.imwrite('new_img.bmp',new_img)
cv2.imwrite('new_img.jpeg',new_img)



###########################################

detected_bits = ""
for i in range(len(message_numbers)):
	y = key_word_numbers[i]
	if new_img[i,y] >= 127:
		detected_bits += "0"
	else:
		detected_bits += "1"

detected_letters_binary = []

# The line below is writen with the help of
# http://stackoverflow.com/questions/9475241/split-python-string-every-nth-character
detected_letters_binary = [detected_bits[i:i+7] for i in range(0, len(detected_bits), 7)]

#The following line is a alternative:
#detected_letters_binary = map(''.join, zip(*[iter(detected_bits)]*7))

detected_message = ""
for item in detected_letters_binary:
	c = chr(int(item,2))
	detected_message += c

print "\tDetected message is....", detected_message

