## Section 04: Decision Trees

Decision trees strike a nice balance between interpretability and accuracy. They pick up on nonlinearity and high degree interactions, but they still produce simple rules or diagrams that explain their decisions. They're also a very robust modeling technique that can generally accept missing values, variables of disparate scales, and correlated variables.

Many techniques have evolved for combining multiple decision trees into ensembles models. These ensembles decrease the error from variance a single tree can produce in new data, while typically not increasing error from bias. Tree-based ensembles are often the most accurate types of models for tabular data.

#### Class Notes

* [Overview of decision trees](notes/instructor_notes.pdf)

* Overview of training decision trees in Enterprise Miner - [Blackboard electronic reserves](https://blackboard.gwu.edu)

* [More decision tree splitting and stopping strategies](notes/tan_notes.pdf)

* [Advanced notes](notes/msba_2017_ml_week_3_FINAL.pdf)

* [EM decision tree example](xml/04_decision_trees.xml)

* [H2o decision tree ensemble examples](src/py_part_4_decision_tree_ensembles.ipynb)

* [Kaggle House Prices example notebook](src/py_part_4_kaggle_xgboost.ipynb)

#### [Sample Quiz](quiz/sample/quiz_4.pdf)

#### [Quiz Key](quiz/key/quiz_4.pdf)

#### Supplementary References

* [XGBoost GitHub](https://github.com/dmlc/xgboost)

* [*Gradient Boosting Machines with H2O*](http://h2o-release.s3.amazonaws.com/h2o/rel-tverberg/5/docs-website/h2o-docs/booklets/GBMBooklet.pdf)

* [H2O GBM Tuning Tutorial for Python](https://github.com/h2oai/h2o-3/blob/master/h2o-docs/src/product/tutorials/gbm/gbmTuning.ipynb)

* *Predictive Modeling and Decision Trees in Enterprise Miner* - [Blackboard electronic reserves](https://blackboard.gwu.edu)

***

* [*Introduction to Statistical Learning*](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Fourth%20Printing.pdf)</br>
Chapter 8

* [*Introduction to Data Mining*](http://www-users.cs.umn.edu/~kumar/dmbook/ch4.pdf)</br>
Chapter 4

* [*Elements of Statistical Learning*](https://web.stanford.edu/~hastie/ElemStatLearn/printings/ESLII_print12.pdf)</br>
Chapters 10 and 15

* [*Pattern Recognition in Machine Learning*](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)</br>
Chapter 14

* [*Random Forests*](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf)</br>
by Leo Breiman

* [*Greedy Function Approximation: A Gradient Boosting Machine*](https://statweb.stanford.edu/~jhf/ftp/trebst.pdf)</br>
by Jerome Freidman

* [*Extremely Randomized Trees*](https://pdfs.semanticscholar.org/336a/165c17c9c56160d332b9f4a2b403fccbdbfb.pdf)</br>
by Pierre Geurts, Damien Ernst and Louis Wehenkel

* Stacked and blended ensemble models:
  * [Stacked Generalization](http://machine-learning.martinsewell.com/ensembles/stacking/Wolpert1992.pdf)</br>
    by David Wolpert, 1992
  * [Super Learner](http://biostats.bepress.com/ucbbiostat/paper222/)</br>
    by Van Der Laan et al, 2007
  * [Stacknet](https://github.com/kaz-Anova/StackNet)</br>
    by Marios Michailidis
  * [Ensemble Models in SAS Enterprise Miner](https://support.sas.com/resources/papers/proceedings16/SAS3120-2016.pdf)
