## Section 10: Practical Model Interpretability

Machine learning algorithms create potentially more accurate models than
linear models, but any increase in accuracy over more traditional,
better-understood, and more easily explainable techniques is not practical for
those who must explain their models to regulators or customers. For many
decades, the models created by machine learning algorithms were taken to be
black-boxes. However, a recent flurry of research has introduced credible
techniques for interpreting complex, machine-learned models. Materials
presented here illustrate applications or adaptations of these techniques for
practicing data scientists.

#### Class Notes

* [O'Reilly AI Conference Slides](notes/instructor_notes.pdf)

* Practical ML interpretability examples

  * [Decision tree surrogate models](src/dt_surrogate.ipynb)

  * [Practical LIME](src/lime.ipynb)

  * [Leave-one-covariate-out (LOCO) local feature importance and reason codes](src/loco.ipynb)

  * [Partial dependence and individual conditional expectation (ICE)](src/pdp_ice.ipynb)  

  * [Sensitivity analysis](src/sensitivity_analysis.ipynb)

  * [Monotonic models with XGBoost](src/mono_xgboost.ipynb)

#### References

**General**

* [Towards A Rigorous Science of Interpretable Machine Learning](https://arxiv.org/pdf/1702.08608.pdf)</br>
by Finale Doshi-Velez and Been Kim
* [Ideas for Machine Learning Interpretability](https://www.oreilly.com/ideas/ideas-on-interpreting-machine-learning)

***

**Techniques**

* **Partial Dependence**: *Elements of Statistical Learning*, Section 10.13
* **LIME**: [“Why Should I Trust You?” Explaining the Predictions of Any Classifier](http://www.kdd.org/kdd2016/papers/files/rfp0573-ribeiroA.pdf)</br>
by Marco Tulio Ribeiro, Sameer Singh, and Carlos Guestrin
* **LOCO**: [Distribution-Free Predictive Inference for Regression](http://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf)</br>
by Jing Lei, Max G’Sell, Alessandro Rinaldo, Ryan J. Tibshirani, and Larry Wasserman
* **ICE**: [Peeking inside the black box: Visualizing statistical learning with plots of individual conditional expectation](https://arxiv.org/pdf/1309.6392.pdf)
* **Surrogate Models**
  * [Extracting tree structured representations of trained networks](https://papers.nips.cc/paper/1152-extracting-tree-structured-representations-of-trained-networks.pdf)
  * [Interpreting Blackbox Models via Model Extraction](https://arxiv.org/pdf/1705.08504.pdf)
