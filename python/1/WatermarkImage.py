import numpy as np
import cv2
import random


class WatermarkImage:

    def __init__(self, original_image=False, message=""):

        if original_image is False:
            self.org = np.zeros((512, 512), np.uint8)
        else:
            self.org = cv2.imread(original_image, 0)  #f.k.a. img

        self.message = message

        if len(self.message) < 32:
            difference = 32 - len(self.message)
            self.message += difference * ' '

        self.message_binary = ""
        self.message_numbers = []
        self.temporary_binary = ""


        self.message_detected = ""
        self.message_binary_detected = ""
        self.detected_letters_binary = []

        self.height = self.org.shape[0]
        self.width = self.org.shape[1]

        self.K = 32
        self.Mb = self.width / self.K
        self.Nb = self.height / self.K

        self.message_matrix = np.zeros((16,16), np.uint8)  #formerly known as blank_image_signed

        self.watermark = np.zeros((self.width, self.height), np.int8)  # f.k.a. resized_image_signed

        self.watermark_visible = np.zeros((self.width, self.height), np.uint8)  # f.k.a. resized_image_signed

        self.noise = np.zeros((self.width, self.height), np.int8)  #f.k.a. noise_signed
        self.noise_is_set = False

        self.noised_watermark = np.zeros((self.width, self.height), np.int8)  #f.k.a. noise_mark

        self.img_with_message = self.org  #f.k.a. new_image

        self.kernel = np.array([[-1, -1, -1, -1, -1],
                                [-1, 1, 2, 1, -1],
                                [-1, 2, 4, 2, -1],
                                [-1, 1, 2, 1, -1],
                                [-1, -1, -1, -1, -1]])

        self.dst = np.zeros((self.width, self.height), np.uint8)

        self.demmod_img = np.zeros((self.width, self.height), np.int8)

        self.watermark_detected = np.zeros((self.width, self.height), np.uint8)  #f.k.a. ZnakDetekt

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def convert_to_eight_bit(self,string):
        if len(string) == 8:
            return string
        else:
            difference = 8 - len(string)
            newstring = difference * '0'
            newstring += string
            return newstring

    def set_message_matrix(self):
        # at this moment we do not use paremeter: "message"
        # We are still using random numbers to fill matrix
#        for i in range(self.K):
#            for j in range(self.K):
#                self.message_matrix[i, j] = random.randint(0, 1)
#                if self.message_matrix[i][j] == 0:
#                    self.message_matrix[i][j] = -1
        for c in self.message:
            self.temporary_binary = bin(ord(c))
            self.eight_bit_binary = self.convert_to_eight_bit(self.temporary_binary[2:])
            self.message_binary += self.eight_bit_binary
        for i in range(16):
            for j in range(16):
                if self.message_binary[i*16+ j] == '1':
                    self.message_matrix[i, j] = 1
                else:
                    self.message_matrix[i, j] = -1



    def set_watermark(self):
        for i in range(self.Mb):
            for j in range(self.Nb):
                self.watermark[i * self.K : ((i+1)*self.K) - 1,j*self.K:((j+1)*self.K) - 1] = self.message_matrix[i][j]
                self.watermark_visible[i * self.K : ((i+1)*self.K) - 1,j*self.K:((j+1)*self.K) - 1] = \
                    self.message_matrix[i][j]

    def set_noise(self,max_noise):
        for i in range(self.width):
            for j in range(self.height):
                self.noise[i][j] = random.randint(1, max_noise)
        self.noise_is_set = True

    def set_noised_watermark(self):
        self.noised_watermark = self.noise * self.watermark

    def set_img_with_message(self,image_from_file = False):
        if image_from_file is False:
            self.img_with_message = self.org + self.noised_watermark
        else:
            self.img_with_message = cv2.imread(image_from_file, 0)
            self.height = self.img_with_message.shape[0]
            self.width = self.img_with_message.shape[1]
            self.Mb = self.width / self.K
            self.Nb = self.height / self.K

    def write_watermark(self,max_noise=2):
        self.set_message_matrix()
        self.set_watermark()
        self.set_noise(max_noise)
        self.set_noised_watermark()
        self.set_img_with_message()


    def set_dst(self):
        self.dst = cv2.filter2D(self.img_with_message, -1, self.kernel)

    def set_demmod_img(self):
        self.demmod_img = self.dst * self.noise

    def set_watermark_detected(self):
        for i in range(self.Mb):
            for j in range(self.Nb):
                self.watermark_detected[i * self.K : ((i+1)*self.K) - 1,j * self.K:((j+1)*self.K) - 1] = np.sign(np.sum(self.demmod_img[i * self.K : ((i+1)*self.K) - 1,j * self.K:((j+1)*self.K) - 1]))
                if np.sign(np.sum(self.demmod_img[i * self.K : ((i+1)*self.K) - 1,j * self.K:((j+1)*self.K) - 1])) > 0:
                    self.message_binary_detected += '1'
                else:
                    self.message_binary_detected += '0'
#        for i in range(self.Mb):
#            for j in range(self.Nb):
#                self.watermark_detected[(i - 1) * self.K + 1:i * self.K + 1, (j - 1) * self.K + 1:j * self.K + 1] = np.sign(np.sum(self.demmod_img[(i - 1) * self.K + 1:i * self.K + 1, (j - 1) * self.K + 1:j * self.K + 1]))
#                if np.sign(np.sum(self.demmod_img[(i - 1) * self.K + 1:i * self.K + 1, (j - 1) * self.K + 1:j * self.K + 1])) > 0:
#                    self.message_binary_detected += '1'
#                else:
#                    self.message_binary_detected += '0'

    def set_message_detected(self):
        self.detected_letters_binary = [self.message_binary_detected[i:i+8] for i in range(0, len(self.message_binary_detected), 8)]
        for item in self.detected_letters_binary:
            self.c = chr(int(item,2))
            self.message_detected += self.c

    def check_watermark_detected_f(self):
        self.check_watermark_detected = self.watermark_detected - self.watermark_visible
        self.error_rate = np.sum(self.check_watermark_detected)

    def read_watermark(self):
        self.set_dst()
        if self.noise_is_set is False:
            self.set_noise()
        self.set_demmod_img()
        self.set_watermark_detected()
        self.set_message_detected()
        self.check_watermark_detected_f()

    def write_all_images_to_files(self):
        cv2.imwrite('message_matrix.jpeg', self.message_matrix)
        cv2.imwrite('watermark.jpeg', self.watermark)
        cv2.imwrite('watermark_visible.jpeg', self.watermark_visible)
        cv2.imwrite('noise.jpeg', self.noise)
        cv2.imwrite('noised_watermark.jpeg', self.noised_watermark)
        cv2.imwrite('img_with_message.jpeg', self.img_with_message)
        cv2.imwrite('dst.jpeg', self.dst)
        cv2.imwrite('demmod_img.jpeg', self.demmod_img)
        cv2.imwrite('watermark_detected.jpeg', self.watermark_detected)
        cv2.imwrite('check_watermark_detected.jpeg', self.check_watermark_detected)


#####################################################################
# end of class WatermarkImage
#####################################################################
