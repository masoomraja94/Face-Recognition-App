import numpy as np
from keras.preprocessing import image
from pathlib import Path
from keras.models import model_from_json

import image_area

count = 0
idx_to_name = {}
p = Path('data/')
dirs = p.glob('*')
for d in dirs:
    idx_to_name[count] = str(d).split('\\')[-1][:-4]
    count += 1


with open("model.json", "r") as file:
    model = model_from_json(file.read())
model.load_weights("model.h5")
model._make_predict_function()


def preprocess_image(img):
    image_area.crop_img(img)
    img = image.load_img(img, target_size=(224, 224, 3))
    img = image.img_to_array(img)
    img = img.reshape((1, 224, 224, 3))
    return img


def encode_image(img):
    img = preprocess_image(img)
    return img


def predict_caption(photo):
    idx = model.predict(photo)
    print(idx[0])
    name = idx_to_name[np.argmax(idx[0])]
    return name


def caption_this_image(image):
    enc = encode_image(image)
    caption = predict_caption(enc)

    return caption
