## Section 02: Analytical Data Prep

A great deal of work in data mining projects is spent on data munging. Below some common data problems that can cause models and predictions to be inaccurate are listed along with their symptoms and potential solutions.

Problem | Symptoms | Solution
--- | --- | ---
**[Incomplete data](#incomplete)** | Useless models and meaningless results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**[Biased Data](#bias)** | Biased models and biased, inaccurate results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**Wide Data** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature selection](#f-selection). [Feature extraction](#f-extraction). L1 Regularization.
**Sparse data<sup>&#10013;</sup>** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature extraction](#f-extraction). Appropriate data representation, i.e. COO, CSR. Appropriate algorithm selection, e.g. factorization  machines.
**Imbalanced Target Variable** | Single class model predictions. Biased model predictions. | [Proportional Oversampling](#oversamp). Inverse prior probability weighting. Mixture models, e.g. zero-inflated regression methods.
**Outliers** | Biased models and biased, inaccurate results. Unstable parameter estimates and rule generation. Unreliable out-of-domain predictions. | [Discretization](#discret). [Winsorizing](#winsor). Appropriate algorithm selection, e.g. Huber loss functions.
**Missing Values** | Information loss. Biased models and biased, inaccurate results. | [Imputation](#impute). [Discretization](#discret). Appropriate algorithm selection, e.g. Tree-based models, naive Bayes classification.
**Character Variables<sup>&#10013;</sup>** | Information loss. Biased models and biased, inaccurate results. Computational errors. | [Encoding](#encode). Appropriate algorithm selection, e.g. Tree-based models, naive Bayes classification.
**High Cardinality Categorical Variables** | Over-fit models and inaccurate results. Long, intolerable compute times. Unreliable out-of-domain predictions. | [Rate-by-level](#r-by-level) or variants e.g. perturbed rate-by-level or [Weight of Evidence](http://support.sas.com/documentation/cdl/en/prochp/66409/HTML/default/viewer.htm#prochp_hpbin_details02.htm). [Average-, Median, BLUP-by-level](#a-by-level). [Discretization](#discret). Embedding approaches, e.g. entity embedding neural networks, factorization machines.
**Disparate Variable Scales** | Unreliable parameter estimates, biased models, and biased, inaccurate results. | [Standardization](#standard), Appropriate algorithm selection, e.g. Tree-based models.
**Strong Multicollinearity (correlation)** | Unstable parameter estimates, unstable rule generation, and unstable predictions. | [Feature selection](#f-selection). [Feature extraction](#f-extraction). L2 Regularization.
**Dirty Data** | Information loss. Biased models and biased, inaccurate results. Long, intolerable compute times. Unstable parameter estimates and rule generation. Unreliable out-of-domain predictions. | Combination of solution strategies.

<sup>&#10013;</sup> In some cases this is not a problem at all. Some algorithms and software packages handle this automatically and elegantly ... some don't.

<a name='incomplete'/>
#### Incomplete data

<a name='bias'/>
#### Biased data

<a name='f-selection'/>
#### Feature selection - [view notebook](src/py_part_2_feature_selection.ipynb)

<a name='f-extraction'/>
#### Feature extraction - [view notebook](src/py_part_2_feature_extraction.ipynb)

<a name='oversamp'/>
#### Oversampling - [view notebook](src/py_part_2_over_sample.ipynb)

<a name='encode'/>
#### Encoding - [view notebook](src/py_part_2_encoding.ipynb)

<a name='discret'/>
#### Discretization - [view notebook](src/py_part_2_discretization.ipynb)

<a name='winsor'/>
#### Winsorizing - [view notebook](src/py_part_2_winsorize.ipynb)

<a name='impute'/>
#### Imputation - [view notebook](src/py_part_2_impute.ipynb)

<a name='r-by-level'/>
#### Rate-by-level - [view notebook](src/py_part_2_rate-by-level.ipynb)

<a name='a-by-level'/>
#### Average-by-level - [view notebook](src/py_part_2_average-by-level.ipynb)

<a name='standard'/>
#### Standardization - [view notebook](src/py_part_2_standardize.ipynb)
