## Section 02: Analytical Data Prep

A great deal of work in data mining projects is spent on data munging. Below some common data problems that can cause models and predictions to be inaccurate are listed along with their symptoms and potential solutions.

#### Enterprise Miner Materials
* [Example data](data/loans.sas7bdat)
* [Diagram notes](notes/02_analytical_data_prep.pdf)
* [Diagram XML](xml/02_analytical_data_prep.xml)
* [Introductory Video(s)](https://www.youtube.com/playlist?list=PLVBcK_IpFVi-xzvJiOlf33UvVbRoLRu0z)

#### Supplementary References
* [Label, Segment, Featurize: a cross domain framework for prediction engineering](http://www.jmaxkanter.com/static/papers/DSAA_LSF_2016.pdf)
* *Introduction to Data Mining* - chapter 2
* *Introduction to Data Mining* - [chapter 2 notes](https://www-users.cs.umn.edu/~kumar/dmbook/dmslides/chap2_data.pdf)

#### [Sample Quiz](quiz/sample/quiz_2.pdf)

#### [Quiz key](quiz/key/quiz_2.pdf)

#### Class notes

Problem | Symptoms | Solution
--- | --- | ---
**[Incomplete data](#incomplete)** | Useless models and meaningless results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**[Biased Data](#bias)** | Biased models and biased, inaccurate results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**Wide Data** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature selection](02_analytical_data_prep.md#feature-selection---view-notebook). [Feature extraction](02_analytical_data_prep.md#feature-extraction---view-notebook). L1 Regularization.
**Sparse data<sup>&#10013;</sup>** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature extraction](02_analytical_data_prep.md#feature-extraction---view-notebook). Appropriate data representation, i.e. COO, CSR. Appropriate algorithm selection, e.g. factorization  machines.
**Imbalanced Target Variable** | Single class model predictions. Biased model predictions. | [Proportional Oversampling](02_analytical_data_prep.md#oversampling---view-notebook). Inverse prior probability weighting. Mixture models, e.g. zero-inflated regression methods.
**Outliers** | Biased models and biased, inaccurate results. Unstable parameter estimates and rule generation. Unreliable out-of-domain predictions. | [Discretization](02_analytical_data_prep.md#discretization---view-notebook). [Winsorizing](02_analytical_data_prep.md#winsorizing---view-notebook). Appropriate algorithm selection, e.g. Huber loss functions.
**Missing Values** | Information loss. Biased models and biased, inaccurate results. | [Imputation](02_analytical_data_prep.md#imputation---view-notebook). [Discretization](02_analytical_data_prep.md#discretization---view-notebook). Appropriate algorithm selection, e.g. Tree-based models, naive Bayes classification.
**Character Variables<sup>&#10013;</sup>** | Information loss. Biased models and biased, inaccurate results. Computational errors. | [Encoding](02_analytical_data_prep.md#encoding---view-notebook). Appropriate algorithm selection, e.g. Tree-based models, naive Bayes classification.
**High Cardinality Categorical Variables** | Over-fit models and inaccurate results. Long, intolerable compute times. Unreliable out-of-domain predictions. | [Target Encoding (categorical)](https://github.com/jphall663/GWU_data_mining/blob/master/02_analytical_data_prep/02_analytical_data_prep.md#target-encoding-categorical---view-notebook) or variants e.g. perturbed rate-by-level or [Weight of Evidence](http://support.sas.com/documentation/cdl/en/prochp/66409/HTML/default/viewer.htm#prochp_hpbin_details02.htm). [Target Encoding (numeric)](https://github.com/jphall663/GWU_data_mining/blob/master/02_analytical_data_prep/02_analytical_data_prep.md#target-encoding-numeric---view-notebook) or variants average-, median, BLUP-by-level. [Discretization](02_analytical_data_prep.md#discretization---view-notebook). Embedding approaches, e.g. entity embedding neural networks, factorization machines.
**Disparate Variable Scales** | Unreliable parameter estimates, biased models, and biased, inaccurate results. | [Standardization](02_analytical_data_prep.md#standardization---view-notebook), Appropriate algorithm selection, e.g. Tree-based models.
**Strong Multicollinearity (correlation)** | Unstable parameter estimates, unstable rule generation, and unstable predictions. | [Feature selection](02_analytical_data_prep.md#feature-selection---view-notebook). [Feature extraction](02_analytical_data_prep.md#feature-extraction---view-notebook). L2 Regularization.
**Dirty Data** | Information loss. Biased models and biased, inaccurate results. Long, intolerable compute times. Unstable parameter estimates and rule generation. Unreliable out-of-domain predictions. | Combination of solution strategies.

<sup>&#10013;</sup> In some cases this is not a problem at all. Some algorithms and software packages handle this automatically and elegantly ... some don't.

#### Incomplete data
When a data set simply does not contain information about the phenomenon of interest. There is no analytical remedy for incomplete data. You must collect more and better data, and probably dispose of the original incomplete set.

#### Biased data
When a data set contains information about the phenomenon of interest, but that information is consistently and systematically wrong. There is no analytical remedy for biased data. You must collect more and better data, and probably dispose of the original biased set.

#### Feature selection - [view notebook](src/py_part_2_feature_selection.ipynb)
Finding the best subset of original variables from a data set, typically by measuring the original variable's relationship to the target variable and taking the subset of original variables with the strongest relationships with the target. Feature selection decreases the impact of the curse of dimensionality and usually increases the signal-to-noise ratio in a data set, resulting in faster training times and more accurate models. Because feature selection uses original variables from a data set, its results are usually more interpretable than feature extraction techniques.

#### Feature extraction - [view notebook](src/py_part_2_feature_extraction.ipynb)
Combining the original variables in a data set into a new, smaller set of more representative variables, very often using unsupervised learning methods. Feature extraction may also be referred to as 'dimension reduction'. Feature extraction is the unsupervised analog of feature selection, i.e. it tends to decreases the impact of the curse of dimensionality and usually increases the signal-to-noise ratio in a data set. Feature extraction techniques combine the original variables in the data set in complex ways, usually creating uninterpretable new variables.

#### Oversampling - [view notebook](src/py_part_2_over_sample.ipynb)
Taking all the rows containing rare events in a data set and increasing them proportionally to the number of rows not containing rare values. 'Undersampling' is the opposite and equally valid approach where the rows not containing rare events are decreased proportionally to the number of rows containing rare events. With rare events, models will often find that the most accurate possible outcome is to predict the rare event never happens. Both oversampling and undersampling artificially inflate the frequency of rare events, which helps models learn to predict rare events.

#### Encoding - [view notebook](src/py_part_2_encoding.ipynb)
Changing the representation of a variable. Very often in data mining applications categorical, character variables are encoded to numeric variables to be used with algorithms that cannot accept character or categorical variables.

#### Target Encoding (Categorical) - [view notebook](src/py_part_2_target_encode_categorical.ipynb)
An encoding method for changing categorical variables into numeric variables when the target is a binary categorical variable. Particularly helpful when a categorical variable has many levels.

#### Target Encoding (Numeric) - [view notebook](src/py_part_2_target_encode_numeric.ipynb)
An encoding method for changing categorical variables into numeric variables when the target is a numeric variable. Particularly helpful when a categorical variable has many levels.

#### Discretization - [view notebook](src/py_part_2_discretization.ipynb)
Changing a numeric variable into an ordinal or nominal categorical variable based on value ranges of the original numeric variable. Discretization can also be referred to as 'binning'. Discretization has many benefits:
* When restricted to using linear models, binning helps introduce nonlinearity because each bin in a variable gets its own parameter.
* Binning smoothes complex signals in training data, often decreasing overfitting.
* Binning deals with missing values elegantly by assigning them to their own bin.
* Binning handles outliers elegantly by assigning all outlying values, in training and new data, to the 'high' or 'low' bin. (Outliers damage predictive models that seek to minimize squared error because they create disproportionately large, i.e. squared, residuals which optimization routines will try to minimize at the expense of minimizing the error for more reliable data points.)

#### Winsorizing - [view notebook](src/py_part_2_winsorize.ipynb)
Removing outliers in a variable's value and replacing them with more central values of that variable. (Outliers damage predictive models that seek to minimize squared error because they create disproportionately large, i.e. squared, residuals which optimization routines will try to minimize at the expense of minimizing the error for more reliable data points.)

#### Imputation - [view notebook](src/py_part_2_impute.ipynb)
Replacing missing data with an appropriate, non-missing value. In predictive modeling imputing should be used with care. Missingness is often predictive. Also imputation changes the distribution of the input variable learned by the model.

#### Standardization - [view notebook](src/py_part_2_standardize.ipynb)
Enforcing similar scales on a set of variables. For distance-based algorithms (e.g. k-means) and algorithms that use gradient-related methods to create model parameters (e.g. regression, artificial neural networks) variables must be on the same scale, or variables with large values will incorrectly dominate the training process.

#### A Data Preperation Lib Kes Wrote (works with spark, pandas, and h2o frames)
* [DataPreperation Library src](src/DataPreperation.py)
* [view notebook example](src/housing.ipynb)
* [view notebook html](http://htmlpreview.github.com/?https://github.com/kcrandall/GWU_data_mining/blob/master/02_analytical_data_prep/src/housing.html)
*<i>Not all the functions have been strenuously tested for all use cases, may have bugs (email kmcrandall@gwmail.gwu.edu if you find one).</i>
