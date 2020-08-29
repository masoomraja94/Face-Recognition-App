# WARNING : DON'T TAKE ANY INPUT BEFORE ENTERING 'q' ------->

# Write a Python Script that Captures images from your webcam video stream
# Extracts all Faces from the image frame (using 'harrcascades' pre trained for face detection)
# Stores the Face information into numpy arrays

# 1. Read and show video stream , capture images
# 2. Detect Faces and show Bounding Box
# 3. Flatten the largest face image (gray scale) and save in a numpy array
# 4. Repeat the above for multiple people to generate training data
# 5. Gray frame for Memory Efficiency

import cv2
import numpy as np

# Init Camera
cap = cv2.VideoCapture(0)

# Face Detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.txt')

skip = 0
face_data = []
dataset_path = './data/'

while True:
    ret, frame = cap.read()
    
    if ret==False:
        continue
        
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces=face_cascade.detectMultiScale(frame, 1.3, 5)
    
    faces = sorted(faces, key=lambda f: f[2]*f[3])
    
    #Pick the Last face (largest according to area)
    for face in faces[-1:]:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        
        # Extract (Crop out the required face) -> Region of Interest
        offset = 10   # 10 Pixels -> Extra Padding at boundry to face
        # Slicing of Image with 10 Px(offset) as Padding
        face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]   # It is in form of (y,x) not (x,y)
        face_section = cv2.resize(face_section, (224, 224))
        
        # Store every 10th Image
        skip+=1
        if skip%10==0:
            face_data.append(face_section)
            print(len(face_data))
        
    cv2.imshow('Frame', frame)
    #cv2.imshow('Face Section',face_section)
    key_pressed=cv2.waitKey(1) & 0xFF
    if key_pressed==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Convert our face list array into numpy array
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0], -1))
print(face_data.shape)

# Save this data into file system
file_name = input('Enter the name of the Person : ')
np.save(dataset_path+file_name+'.npy', face_data)
print('Data Successfully Saved at '+dataset_path+file_name+'.npy')