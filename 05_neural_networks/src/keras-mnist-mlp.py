import os
path = os.path.dirname(os.getcwd())

# MNIST Data
import pandas as pd

pd_train_data = pd.read_csv(path+"/data/train.csv", header=None)
pd_test_data = pd.read_csv(path+"/data/test.csv", header=None)

train_data = pd_train_data.as_matrix()
test_data = pd_test_data.as_matrix()

x_train = train_data[:,0:784]
y_train = train_data[:,784]

x_test = test_data[:,0:784]
y_test = test_data[:,784]

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
from keras.layers import Dense, Dropout

model = Sequential()

model.add(Dense(64, input_shape=(784,), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation="sigmoid"))

model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=20, batch_size=128)

print(model.evaluate(x_test, y_test, batch_size=128))
