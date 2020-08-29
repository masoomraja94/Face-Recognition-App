import cv2
from PIL import Image

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.txt')

def crop_img(img):
    frame = cv2.imread(img)
    face_section = frame
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)

    faces = sorted(faces, key=lambda f: f[2] * f[3])

    for face in faces[-1:]:
        x, y, w, h = face

        offset = 10
        face_section = frame[y - offset:y + h + offset, x - offset:x + w + offset]
        face_section = cv2.resize(face_section, (224, 224))
        face_section = cv2.cvtColor(face_section, cv2.COLOR_BGR2RGB)

    im = Image.fromarray(face_section)
    im.save(img)

    return
