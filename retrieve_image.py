from bs4 import BeautifulSoup
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image, ImageChops
import random
import requests
from textblob import TextBlob
import time
import urllib.request

from apikeys import apikey, cx

from genetic_approx import run_evolve

cardspath = 'cards'
desired_width = 225
desired_height = 300
BACKGROUND_COLOR = 'white'

def getImageFromGoogleSearchImage(image):
	# convert Google Search image object to Pillow Image
	my_bytes_io = BytesIO()
	my_bytes_io.seek(0)
	raw_image_data = image.get_raw_data()
	image.copy_to(my_bytes_io, raw_image_data)
	image.copy_to(my_bytes_io)
	my_bytes_io.seek(0)
	img = Image.open(my_bytes_io)
	return img

def getImage(word):
	# gis = GoogleImagesSearch(apikey, cx)

	# # set search parameters
	# # maximum results num is 10
	# _search_params = {
		# 'q': word,
		# 'num': 10,
		# 'safe': 'off',
		# 'fileType': 'jpg',
		# # 'imgType': 'photo',
		# 'imgSize': 'large',
	# }
	
	# # do search
	# gis.search(search_params=_search_params)
	
	# # randomly select 1 image from results
	# results = random.sample(gis.results(), 1)
	# result = results[0]
    
	# img = getImageFromGoogleSearchImage(result)
    
	img = Image.open("test2.jpg")
	width, height = img.size
	resize_ratio = max(desired_width/width, desired_height/height)
	img = img.resize((round(resize_ratio * width), round(resize_ratio * height)))
    # 4-tuple defining the left, upper, right, and lower pixel coordinate
	img = img.crop((0, 0, desired_width, desired_height))
    
	img.show()
	print("going into evolution")
	new_img = run_evolve(img, desired_width, desired_height)
    # new_img.show()

getImage('mother')

