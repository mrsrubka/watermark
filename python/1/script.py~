#import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
import numpy as np
import cv2
import random

# Load an color image in grayscale
img = cv2.imread('lena.bmp',0)

# Parametry
K = 32     # rozmiar bloku dla jednego bitu znaku wodnego (K x K pikseli)


width, height = img.shape[:2]
Mb = width/K
Nb = height/K
watermark = [ [ 0 for i in range(K) ] for j in range(K) ]
for i in range(K):
	for j in range(K):
		watermark[i][j] = random.randint(0,1) - 1
		if watermark[i][j] == 0:
			watermark[i][j] = -1
blank_image = np.zeros((K,K), np.uint8)
for i in range(K):
	for j in range(K):
		blank_image[i,j] = random.randint(0,1)
		if blank_image[i][j] == 0:
			blank_image[i][j] = -1
blank_image_signed = np.zeros((K,K), np.int8)
for i in range(K):
	for j in range(K):
		if blank_image[i][j] == 255:
			blank_image_signed[i][j] = -1
		else:
			blank_image_signed[i][j] = blank_image[i][j]


resized_image = np.zeros((width,height), np.uint8)
for i in range(1,Mb+1):
	for j in range(1,Nb+1):
		resized_image[(i-1)*K+1:i*K+1,(j-1)*K+1:j*K+1] = blank_image[i][j]  

resized_image_signed = np.zeros((width,height), np.int8)
for i in range(width):
	for j in range(height):
		if resized_image[i,j] > 128:
			resized_image_signed[i,j] = resized_image[i,j] - 256
		else:
			resized_image_signed[i,j] = resized_image[i,j] 



cv2.imshow('image',blank_image)
#cv2.waitKey(1000)
cv2.imshow('image',resized_image_signed)
#cv2.waitKey(1000)
#cv2.imwrite('resized_image.bmp',resized_image)
cv2.imwrite('resized_image.jpg',resized_image)
#cv2.waitKey(1000)
#cv2.imwrite('resized_image_signed.bmp',resized_image_signed)
cv2.imwrite('resized_image_signed.jpg',resized_image_signed)

noise = np.zeros((width,height), np.uint8)
#noise = np.zeros((width,height), np.uint8)
#noise = np.zeros((width,height))

for i in range(width):
	for j in range(height):
		noise[i][j] = random.randint(1,6)
#noise_mark = np.dot(noise,watermark)

noise_signed = np.zeros((width,height), np.int8)
for i in range(width):
	for j in range(height):
		if noise[i,j] > 128:
			noise_signed[i,j] = noise[i,j] - 256
		else:
			noise_signed[i,j] = noise[i,j] 

print noise.shape, blank_image.shape, resized_image.shape
cv2.imshow('image',noise)
#cv2.waitKey(1000)


#watermark = np.zeros((width,height), np.uint8)
#for i in range(width):
#	for j in range(height):
#		ran = random.randint(0,1)
#		if ran == 0:
#			ran = -1
#		watermark[(i-1)*K+1 : i*K, (j-1)*K+1 : j*K] = ran

#for i in range(width):
#	for j in range(height):
#		if resized_image[i][j] == 255:
#			resized_image[i][j] = -1
#print resized_image
print "noise:"
print noise
#print resised_image


#noise_mark_preview = np.dot(noise,resized_image)
noise_mark_preview = noise * resized_image

#noise_mark_signed = np.dot(noise_signed,resized_image_signed)
noise_mark_signed = noise_signed * resized_image_signed


noise_mark = noise_mark_preview
#cv2.imshow('image',noise_mark)
#cv2.waitKey(1000)

cv2.imshow('image',noise_mark_signed)
#cv2.waitKey(1000)

#print "noise_mark:"
#print noise_mark

print "noise_mark_signed:"
print noise_mark_signed

new_img = img + noise_mark_signed
cv2.imshow('image',new_img)
#cv2.waitKey(1000)
#cv2.imwrite('new_img.bmp',new_img)
cv2.imwrite('new_img.jpeg',new_img)

#print img

#####################################################################

#L=10
#L2 = 2*L+1
#w = np.hamming(L2)
#w2 = w * np.transpose(w)
#ham2d = np.sqrt(np.outer(w,w))

#f0 = 0.5
#wc = np.pi * f0
#xv,yv = np.meshgrid(np.linspace(-L,L),np.linspace(-L,L))
# albo:
#xv,yv = np.meshgrid(np.linspace(-L,L,10),np.linspace(-L,L,10))
#temp = np.divide(wc*np.sqrt(xv**2 + yv**2),2*np.pi*np.sqrt(xv**2 + yv**2))
#besselj = scipy.special.jn(1, temp)
#lp = wc * besselj

#kernel = np.ones((5,5),np.float32)/25
#kernel = np.matrix('0 1 0 ; 1 -4 1 ; 0 1 0')

kernel = np.array([[-1, -1, -1, -1, -1],
                   [-1,  1,  2,  1, -1],
                   [-1,  2,  4,  2, -1],
                   [-1,  1,  2,  1, -1],
                   [-1, -1, -1, -1, -1]])

dst = cv2.filter2D(new_img,-1,kernel)

cv2.imshow('image',dst)
#cv2.waitKey(1000)
#cv2.imwrite('dst.bmp',dst)
cv2.imwrite('dst.jpeg',dst)



#####################33

img_dem = dst * noise_signed



cv2.imshow('image',img_dem)
#cv2.waitKey(1000)
#cv2.imwrite('img_dem.bmp',img_dem)
cv2.imwrite('img_dem.jpeg',img_dem)

ZnakDetekt = np.zeros((width,height), np.uint8)
for i in range(1,Mb+1):
	for j in range(1,Nb+1):
		ZnakDetekt[(i-1)*K+1:i*K+1,(j-1)*K+1:j*K+1] = np.sign(np.sum(np.sum(img_dem[(i-1)*K+1:i*K+1,(j-1)*K+1:j*K+1])))
cv2.imshow('image',ZnakDetekt)
#cv2.waitKey(1000)
#cv2.imwrite('ZnakDetekt.bmp',ZnakDetekt)
cv2.imwrite('ZnakDetekt.jpeg',ZnakDetekt)
