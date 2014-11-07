import numpy as np
#import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import random

img = cv2.imread('lena.bmp',0)

dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
magnitude_spectrum = img
magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
magnitude_spectrum.astype(int)

#plt.subplot(121),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
#plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()

cv2.imshow('image',magnitude_spectrum)
cv2.imwrite('magnitude_spectrum.jpeg',magnitude_spectrum)
cv2.waitKey(1000)
#cv2.imshow('image',dft)
cv2.waitKey(1000)
#cv2.imshow('image',dft_shift)
cv2.waitKey(1000)

