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

* [Interpretability: Good, Bad, and Ugly slides](notes/MLI_good_bad_ugly.pdf)

* [Instructor notes](notes/instructor_notes.pdf)

* Practical ML interpretability examples

  * [Monotonic XGBoost models, partial dependence, and individual conditional expectation plots](https://github.com/jphall663/interpretable_machine_learning_with_python/blob/master/xgboost_pdp_ice.ipynb)

  * [Decision tree surrogates, reason codes, and ensembles of explanations](https://github.com/jphall663/interpretable_machine_learning_with_python/blob/master/dt_surrogate_loco.ipynb)

  * [LIME](https://github.com/jphall663/interpretable_machine_learning_with_python/blob/master/lime.ipynb)

  * [Sensitivity and residual analysis](https://github.com/jphall663/interpretable_machine_learning_with_python/blob/master/resid_sens_analysis.ipynb)  

* [Comparison of LIME, Shapley, and treeinterpreter explanations](https://github.com/h2oai/mli-resources/tree/master/lime_shap_treeint_compare)

#### References

**General**

* [Towards A Rigorous Science of Interpretable Machine Learning](https://arxiv.org/pdf/1702.08608.pdf)
* [Explaining Explanations: An Approach to Evaluating Interpretability of Machine Learning](https://arxiv.org/pdf/1806.00069.pdf)
* [A Survey Of Methods For Explaining Black Box Models](https://arxiv.org/pdf/1802.01933.pdf)
* [Trends and Trajectories for Explainable, Accountable and Intelligible Systems: An HCI Research Agenda](https://dl.acm.org/citation.cfm?id=3174156)

***

* [Ideas for Machine Learning Interpretability](https://www.oreilly.com/ideas/ideas-on-interpreting-machine-learning)
* [An Introduction to Machine Learning Interpretability](https://www.safaribooksonline.com/library/view/an-introduction-to/9781492033158/) (or [Blackboard](https://blackboard.gwu.edu) electronic reserves)

***

**Techniques**

* **Partial Dependence**: *Elements of Statistical Learning*, Section 10.13
* **LIME**: [“Why Should I Trust You?” Explaining the Predictions of Any Classifier](http://www.kdd.org/kdd2016/papers/files/rfp0573-ribeiroA.pdf)
* **LOCO**: [Distribution-Free Predictive Inference for Regression](http://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf)
* **ICE**: [Peeking inside the black box: Visualizing statistical learning with plots of individual conditional expectation](https://arxiv.org/pdf/1309.6392.pdf)
* **Surrogate Models**
  * [Extracting tree structured representations of trained networks](https://papers.nips.cc/paper/1152-extracting-tree-structured-representations-of-trained-networks.pdf)
  * [Interpreting Blackbox Models via Model Extraction](https://arxiv.org/pdf/1705.08504.pdf)
* **TreeInterpreter**: [Random forest interpretation with scikit-learn](http://blog.datadive.net/random-forest-interpretation-with-scikit-learn/)
* **Shapley Explanations**: [A Unified Approach to Interpreting Model Predictions](http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.pdf)
* **Explainable neural networks (xNN)**: [Explainable Neural Networks based on Additive Index Models](https://arxiv.org/pdf/1806.01933.pdf)
