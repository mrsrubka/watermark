#import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
import numpy as np
import cv2
import random

class WatermarkImage:
	def __init__(self, original_image, message):
		self.org = cv2.imread(original_image,0) #f.k.a. img
		self.message = message
		
		self.height = self.org.shape[0]
		self.width = self.org.shape[1]

		self.K = 32
		self.Mb = self.width / self.K
		self.Nb = self.height / self.K

		self.message_matrix = np.zeros((self.K,self.K), np.uint8) #formerly known as blank_image_signed

		self.watermark = np.zeros((self.width,self.height), np.uint8) # f.k.a. resized_image_signed

		self.noise = np.zeros((self.width,self.height), np.int8) #f.k.a. noise_signed

		self.noised_watermark = np.zeros((self.width,self.height), np.int8) #f.k.a. noise_mark

		self.img_with_message = self.org #f.k.a. new_image


		self.kernel = np.array([[-1, -1, -1, -1, -1],
					   [-1,  1,  2,  1, -1],
					   [-1,  2,  4,  2, -1],
					   [-1,  1,  2,  1, -1],
					   [-1, -1, -1, -1, -1]])

		self.dst = self.org

		self.demmod_img = self.org

		self.watermark_detected = np.zeros((self.width,self.height), np.uint8) #f.k.a. ZnakDetekt
		
	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def set_message_matrix(self,message):
	# at this moment we do not use paremeter: "message"
	# We are still using random numbers to fill matrix
		for i in range(self.K):
			for j in range(self.K):
				self.message_matrix[i,j] = random.randint(0,1)
				if self.message_matrix[i][j] == 0:
					self.message_matrix[i][j] = -1

	def set_watermark(self):
		for i in range(1,self.Mb+1):
			for j in range(1,self.Nb+1):
				self.watermark[(i-1)*self.K+1:i*self.K+1,(j-1)*self.K+1:j*self.K+1] = self.message_matrix[i][j]  

	def set_noise(self):
		for i in range(self.width):
			for j in range(self.height):
				self.noise[i][j] = random.randint(1,6)

	def set_noised_watermark(self):
		self.noised_watermark = self.noise * self.watermark

	def set_img_with_message(self):
		self.set_message_matrix("")
		self.set_watermark()
		self.set_noise()
		self.set_noised_watermark()
		self.img_with_message = self.org + self.noised_watermark

	
	def set_dst(self):
		self.dst = cv2.filter2D(self.img_with_message,-1,self.kernel)
	
	def set_demmod_img(self):
		self.demmod_img = self.dst * self.noise
	
	def set_watermark_detected(self):
		for i in range(1,self.Mb+1):
			for j in range(1,self.Nb+1):
				self.watermark_detected[(i-1)*self.K+1:i*self.K+1,(j-1)*self.K+1:j*self.K+1] = np.sign(np.sum(np.sum(self.demmod_img[(i-1)*self.K+1:i*self.K+1,(j-1)*self.K+1:j*self.K+1])))	

	def read_watermark(self):
		self.set_dst()
		self.set_demmod_img()
		self.set_watermark_detected()

#####################################################################

img = WatermarkImage('lena.bmp',"")
img.set_img_with_message()
cv2.imwrite('img_with_message.jpeg',img.img_with_message)
#####################################################################

#cv2.imwrite('.jpeg',img.)

img.read_watermark()

cv2.imwrite('message_matrix.jpeg',img.message_matrix)
cv2.imwrite('watermark.jpeg',img.watermark)
cv2.imwrite('noise.jpeg',img.noise)
cv2.imwrite('noised_watermark.jpeg',img.noised_watermark)
cv2.imwrite('img_with_message.jpeg',img.img_with_message)
cv2.imwrite('dst.jpeg',img.dst)
cv2.imwrite('demmod_img.jpeg',img.demmod_img)
cv2.imwrite('watermark_detected.jpeg',img.watermark_detected)


