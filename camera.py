from stuffz import init, scale #My personal library of useful mechanics.
from face_exp import getEmotion
import cv2
from PIL import Image
import numpy as np


def get_frame(frame):
	prevX, prevY, prevW, prevH = init(4)
	hasFace = True
	try:
		emotion = getEmotion(frame).lower()
	except:
		emotion = 'none'
	print(f'DETECTED EMOTION: {emotion}')
	emojis = {'default':'emoji.png', 'happy': 'emoji.png', 'angry':'angry.png', 'suprised':'suprised.png', 'fearful':'suprised.png', 'sad':'sad.png', 'neutral':'neutral.png'}
	emoji = ''
	#In case of error.
	try:
		emoji = emojis[emotion]
	except:
		emoji = emojis['default']
	#Reread emoji image to prevent loss of quality over time, and to load current expression.
	s_img = cv2.imread(emoji, cv2.IMREAD_UNCHANGED)
	try:
		frame = scale(frame, 78)
	except:
		print("Reached end of video.")
	#Coordinates of face.
	faceX, faceY = None, None
	faceCascade = cv2.CascadeClassifier("face.xml")
	faces = faceCascade.detectMultiScale(frame,scaleFactor=1.3,minNeighbors=5)
	if faces == ():
		print("NO FACES PRESENT")
		hasFace = False
		try:
			s_img = cv2.resize(s_img, (prevW, prevH))
		except:
			pass
	else:
		for (x, y, w, h) in faces:
			faceX, faceY = x, y
			prevX, prevY, prevW, prevH = x, y, w, h
			print(f'Previous X, Y, set: ({prevX}, {prevY})')
			print(f'--\nX: {x}\nY: {y}')
			try:
				s_img = cv2.resize(s_img, (w, h))
			except:
				pass
	
	p_s_img = Image.fromarray(cv2.cvtColor(s_img, cv2.COLOR_BGR2RGBA))
	p_l_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
	p_final = p_l_img.copy()
	if hasFace:
		try:
			p_final.paste(p_s_img, (faceX,faceY), p_s_img)
		except NameError:
			pass
	else:
		print(f'Running no face code\nPASTING ON COORDS: ({prevX}, {prevY})')
		try:
			p_final.paste(p_s_img, (prevX,prevY), p_s_img)
		except NameError:
			pass
		else:
			print(f"Printed emoji on ({prevX}, {prevY}).")
	final = cv2.cvtColor(np.array(p_final), cv2.COLOR_RGB2BGR)
	final = cv2.flip(final, 1)
	return final