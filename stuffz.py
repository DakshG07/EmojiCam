import cv2

def init(amount, fill=0):
	"""Initialize any amount of variables with fill."""
	result = []
	counter = 0
	while counter < amount:
		result.append(fill)
		counter += 1
	return result

def a(number):
	"""Add one to a number."""
	number += 1
	return number

def scale(img, scale_percent):
	"""Scale a cv2 image."""
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height)
	# resize image
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	return resized