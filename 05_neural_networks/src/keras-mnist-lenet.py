import os
path = os.path.dirname(os.getcwd())

#	MNIST Data
import pandas as pd

pd_train_data = pd.read_csv(path+"/data/train.csv", header=None)
pd_test_data = pd.read_csv(path+"/data/test.csv", header=None)

train_data = pd_train_data.as_matrix()
test_data = pd_test_data.as_matrix()

x_train = train_data[:,0:784]
y_train = train_data[:,784]

x_test = test_data[:,0:784]
y_test = test_data[:,784]

x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32')
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32')

## Normalize data
x_train /= 255
x_test /= 255

from keras.utils import np_utils
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

#	Build Model
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dense

model = Sequential()

# Convolution and pooling 1
model.add(Conv2D(filters=6, kernel_size=(2,2), input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=2))
model.add(Activation("sigmoid"))

# Convolution and pooling 2
model.add(Conv2D(filters=16, kernel_size=(5,5)))
model.add(MaxPooling2D(pool_size=2))
model.add(Activation("sigmoid"))

# Convolution 3
model.add(Conv2D(filters=120, kernel_size=(4,4)))

# Fully-Connected
model.add(Flatten())
model.add(Dense(84))
model.add(Activation("tanh"))

# Output layer
model.add(Dense(10))
model.add(Activation('softmax'))

model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=20, batch_size=128)

print(model.evaluate(x_test, y_test, batch_size=128))
