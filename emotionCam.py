#Importing the necessary libraries 
import cv2
from PIL import Image
import numpy as np 
from face_exp import getEmotion
#Creating a VideoCapture object to read the video
video_loc = r'C:\Users\Administrator\Documents\EmojiCam\test.mp4'
cap = cv2.VideoCapture(0)

def scale(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized
  
#Previous position and size of emoji.
#If no face is found
prevX = 0
prevY = 0
prevW = 0
prevH = 0
#While video is running, loop through it.
while (cap.isOpened()):
    hasFace = True
    # Capture frame-by-frame 
    ret, frame = cap.read()
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
        break
    # Display original video
    cv2.imshow('Original Video', cv2.flip(frame, 1))
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
    cv2.imshow('Processed', cv2.flip(final, 1))
    # define q as the exit button 
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break
  
# release the video capture object 
cap.release() 
# Closes all the windows currently opened. 
cv2.destroyAllWindows() 