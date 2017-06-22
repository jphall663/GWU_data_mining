## Section 05: Neural Networks

Neural networks are important because of their ability to approximate **any** relationship between input variables and target variables. In practice they tend to be difficult to train and difficult to interpret, but excel at pattern recognition tasks in images and sound. A new field of neural networks, known as *deep learning*, has been responsible for some of the most important recent breakthroughs in machine learning and artificial intelligence.

#### Class Materials

* [Overview of neural networks](notes/instructor_notes.pdf)

* Overview of training neural networks in Enterprise Miner - [Blackboard electronic reserves](https://blackboard.gwu.edu)

* [More details on training neural networks](notes/tan_notes.pdf)

* [Wen's deep learning notes](notes/cnn-gwu.pdf)

* [EM neural network example](xml/05_neural_networks.xml)

* [H2O neural network examples](src/py_part_5_neural_networks.ipynb)

* [Kaggle Digit Recognizer Starter Kit](src/py_part_5_MNIST_DNN.ipynb)

* [H2O autoencoder example](src/py_part_5_MNIST_autoencoder.ipynb)

* [MNIST data augmentation example](src/py_part_5_MNIST_data_augmentation.ipynb)

* [Wen's MNIST Keras example](src/py_part_5_MNIST_keras_lenet.ipynb)

#### [Sample Quiz](quiz/sample/quiz_5.pdf)

#### [Quiz key](quiz/key/quiz_5_key.pdf)

#### [Assignment](assignment/assignment_5.pdf)

#### [Assignment key](assignment/key/assignment_5_key.pdf)

#### Supplementary References

* [*Deep Learning with H2O*](http://h2o-release.s3.amazonaws.com/h2o/rel-ueno/1/docs-website/h2o-docs/booklets/DeepLearningBooklet.pdf)

* [*The Definitive Performance Tuning Guide for H2O Deep Learning*](https://blog.h2o.ai/2015/02/deep-learning-performance/)

* *Predictive Modeling and Neural Networks in Enterprise Miner* - 
[Blackboard electronic reserves](https://blackboard.gwu.edu)

***

* *Introduction to Data Mining*</br>
Section 5.4

* [*Elements of Statistical Learning*](http://statweb.stanford.edu/~tibs/ElemStatLearn/printings/ESLII_print10.pdf)</br>
Chapter 11

* [*Pattern Recognition in Machine Learning*](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)</br>
Chapter 5

* [*Deep Learning*](http://www.deeplearningbook.org/)</br>
Chapters 6 - 9 

* [*Gradient-Based Learning Applied to Document Recognition*](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)</br>
The seminal convolutional neural network paper from 1998 by Yann Lecun

* [*Reducing the Dimensionality of Data Using Neural Networks*](https://www.cs.toronto.edu/~hinton/science.pdf)</br>
The seminal deep learning paper from 2006 by Geoffrey Hinton

* Papers about problems with neural networks:

  * [Intriguing Properties of Neural Networks](http://cs.nyu.edu/~zaremba/docs/understanding.pdf)
  
  * [Deep Neural Networks are Easily Fooled: High Confidence Predictions for Unrecognizable Images](http://arxiv.org/pdf/1412.1897v2.pdf) 

***

* [Advanced Class Notes](notes/advanced_notes.pdf)

* [*Neural Network Zoo*](http://www.asimovinstitute.org/neural-network-zoo/) article </br>
Quick summary of the many different types of neural networks

* [An overview of gradient descent optimization algorithms](http://sebastianruder.com/optimizing-gradient-descent/index.html)

* Neural network FAQ by Warren Sarle: ftp://ftp.sas.com/pub/neural/FAQ.html#A2 </br> More than you ever wanted to know about traditional neural networks (some info may be dated and/or obsolete.)

* [Quora answers regarding standard neural networks and deep learning](https://www.quora.com/profile/Patrick-Hall-4/answers/Artificial-Neural-Networks-ANNs)

* [Decent GPU Theano/Keras install instructions for Windows](https://datanoord.wordpress.com/2016/02/02/setup-a-deep-learning-environment-on-windows-theano-keras-with-gpu-enabled/)

* [Decent CPU Theano/TensorFlow/Keras install instructions for Mac](http://machinelearningmastery.com/setup-python-environment-machine-learning-deep-learning-anaconda/)

***

* MNIST Data

  * [Yann LeCun's MNIST page](http://yann.lecun.com/exdb/mnist/)
  * [MNIST as CSV](https://pjreddie.com/projects/mnist-in-csv/)

#### Hacky definitions for hard deep learning concepts

**Max. Out** - A type of activation that outputs the maximum input to a 
neuron.

**Momentum** - An gradient descent hyper-parameter that helps carry the 
optimization over local minima and converge faster. Momentum creates a velocity
vector *v* from previous the iteration's parameters. In 
the current iteration this vector is added to the current parameter updates, 
increasing updates for dimensions whose gradients point in the same direction 
and reducing updates for dimensions whose gradients change directions, 
resulting in decreased oscillation. Momentum is usually set to max-out at a 
certain value: "terminal velocity".

**Nesterov Accelerated Gradient** - A type of SGD that uses the momentum 
formula to calculate the gradient on approximate new parameters. (Like looking 
into to the future by using the gradient on the approximate next position on 
the error surface, so you're gradient might be better behaved).

**Adagrad** - A type of SGD that updates parameters for sparse features with 
bigger gradients and parameters for dense features with smaller gradients, by 
scaling the learning rate by 1/sum(past parameter-wise gradients). 

**Adadelta** - An alternative to Adagrad. Adagrad always drives the learning 
rate to zero. Adadelta uses a decaying average of past gradients instead of 
the sum of all past gradients to avoid this. 
