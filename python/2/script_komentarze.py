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

#poniżej ciąg: "BudapesztBudapesztBudapesztBudapeszt..."
#zamienia na wektor znaków ascii: [121 99 121 ... ]
for i in range(512+1):
	letter = key_word[i%len(key_word)]
	nr_in_ascii = ord(letter)
	key_word_numbers.append(nr_in_ascii)

#key_word_numbers to teraz wektor z "BudapesztBudapesztBudapesztBudapeszt..." ale zapisany liczbami

message ="chromodynamika kwantowa"
message_binary = ""
message_numbers = []


#poniżej dla każdej literki bierzemy jego kod ascii - funkcja ord i zapisujemy binarnie - funkcja bin
# jest problem bo funkcja bin zwraca string "0b110"
# a my nie potrzebujemy 0b na poczatku
# więc jezeli a = "abcd"
# to print a[2:] da nam: "cd" czyli: wydrukuj od drugiego znaku do końca.
for c in message:
	temporary_binary = bin(ord(c))
	message_binary += temporary_binary[2:]

#w ten sposób message_binary to ciąg zer i jedynek
#gdzie każde kolejne 7 bitów to jakiś CHAR (reprezentowany przez ascii)
# UWAGA! wykorzystujemy 7-bit ascii, wiec nie ma polskich znakow!!!

for c in message_binary:
	message_numbers.append(int(c))

# teraz message_numbers to to samo co message_binary, ale przekonwertowane ze stringa do wektora.


#poniżej zapisujemy na zdjeciu bit 1 (jako czarny czyli 0) a bit 0 (jako biały czyli 255) 
#Trochę głupio, ale doszedłem do wniosku, że dla ludzi naturalne jest:
# biały = 0 a czarny = 1
# nie moja wida, że 255 to biały :(
### !!! y to wektor ze słowa kluczowego, który zapewnia, że bity nie bedą zapisywane z góry do dołu jeden pod drugim, tylko będą trochę pływały.

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

#wyżej: jeżeli bit jest badziej biały (>=127) to dopisujemy (+=) do stringa 0
# i odwrotnie

detected_letters_binary = []

#to niżej to ciężko wytłumaczyć, może wejdź w linka?

# The line below is written with the help of
# http://stackoverflow.com/questions/9475241/split-python-string-every-nth-character
detected_letters_binary = [detected_bits[i:i+7] for i in range(0, len(detected_bits), 7)]

#The following line is a alternative:
#detected_letters_binary = map(''.join, zip(*[iter(detected_bits)]*7))

detected_message = ""
for item in detected_letters_binary:
	c = chr(int(item,2))
	detected_message += c

print "\tDetected message is....", detected_message



# no detekcja to jest po prostu odwrócenie algorytmu zapisu.
# jezeli jest jakis problem z jaką funkcją, albo ze składnią no to dajcie znać.

# To że zapisujemy na zdjęciu białą czy czarną kropkę to tylko tak na razie,żeby było WIDAĆ gołym okiem.
#potem można pomyśleć nad innym sposobem, np. zmiana najmniej znaczacego bitu (po polsku parzystość) która miała by oznaczać znak bitu.
# tO po to aby jak najmniej zniekształcić oryginał.

