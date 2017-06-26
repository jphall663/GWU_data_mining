## Section 10: Model Interpretability

Machine learning algorithms offer potentially more accurate models than 
linear models, but any increase in accuracy over more traditional, 
better-understood, and more easily explainable techniques is not practical for
those who must explain their models to regulators or customers. For many
decades, the models created by machine learning algorithms were taken to be
black-boxes. However, a recent flurry of research has introduced credible
techniques for interpreting complex, machine-learned models.

#### Class Notes 

* [Instructor notes](notes/instructor_notes.pdf)

* Basic ML interpretability examples

  * [Decision tree surrogate models](src/dt_surrogate.ipynb)
  
  * [Partial dependence and ICE](src/pdp_ice.ipynb)

  * [LOCO local feature importance](src/loco.ipynb)
  
#### Supplementary References

* [Towards A Rigorous Science of Interpretable Machine Learning](https://arxiv.org/pdf/1702.08608.pdf)</br>
by and Been Kim

* [Ideas for Machine Learning Interpretability](https://www.oreilly.com/ideas/ideas-on-interpreting-machine-learning)

***

* [*Elements of Statistical Learning*](http://statweb.stanford.edu/~tibs/ElemStatLearn/printings/ESLII_print10.pdf)</br>
Section 10.13

* [*Pattern Recognition in Machine Learning*](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)</br>
Chapter 10

***

* [“Why Should I Trust You?” Explaining the Predictions of Any Classifier](http://www.kdd.org/kdd2016/papers/files/rfp0573-ribeiroA.pdf)</br>
by Marco Tulio Ribeiro, Sameer Singh, and Carlos Guestrin

* [Distribution-Free Predictive Inference for Regression](http://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf)</br>
by Jing Lei, Max G’Sell, Alessandro Rinaldo, Ryan J. Tibshirani, and Larry Wasserman

* [Peeking inside the black box: Visualizing statistical learning with plots of individual conditional expectation.](https://arxiv.org/pdf/1309.6392.pdf)

* [Extracting trees structured representations of trained networks](https://papers.nips.cc/paper/1152-extracting-tree-structured-representations-of-trained-networks.pdf)
