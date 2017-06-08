import os
import random
from PIL import Image
import numpy as np

root_path = os.path.dirname(os.getcwd())

os.chdir(root_path)
os.getcwd()
wd = os.getcwd() # Get working directory

# MNIST
mnist_data_dir = "data/mnist_png"
data_sets = ["training", "testint"]
classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Image Processing Functions
def png_to_vec(path_to_img):
	img = Image.open(path_to_img)
	img_arr = np.array(img)
	return(img_arr.ravel().tolist())

# Create Training and Test Sets
nrows_training = 60000
nrows_testing = 10000
samples = 128
samples_training = np.random.choice(classes,samples).tolist()
samples_testing = np.random.choice(classes,samples).tolist()

mnist_data_dir = "data/mnist_png"
data_sets = ["training", "testing"]
list_training_dirs = map(lambda x: os.path.join(mnist_data_dir, "training", x), samples_training)
list_training_dirs = map(lambda x: os.path.join(mnist_data_dir, "testing", x), samples_testing)

list_training_img_path = map(lambda x: os.path.join(x, random.choice(os.listdir(x))), list_training_dirs)
list_testing_img_path = map(lambda x: os.path.join(x, random.choice(os.listdir(x))), list_training_dirs)

list_training_img_vectors = map(lambda x: png_to_vec(x), list_training_img_path)
list_testing_img_vectors = map(lambda x: png_to_vec(x), list_testing_img_path)

#	Build Model
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout

x_train = list_training_img_vectors
y_train = keras.utils.to_categorical(samples_training, num_classes=10)

x_test = list_testing_img_vectors
y_test = keras.utils.to_categorical(samples_testing, num_classes=10)

model = Sequential()

model.add(Dense(64, input_shape=(784,), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation="sigmoid"))

model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=20, batch_size=128)

print(model.evaluate(x_test, y_test, batch_size=128))
