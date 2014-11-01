#!/usr/bin/env python
# import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
from WatermarkImage import WatermarkImage

img = WatermarkImage('lena.bmp')
img.write_watermark()
#####################################################################
img.read_watermark()
#####################################################################
img.write_all_images_to_files()


