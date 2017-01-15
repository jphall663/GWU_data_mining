## Section 02: Analytical Data Prep

A great deal of work in data mining projects is spent on data munging. Below some common data problems that can cause models and predictions to be inaccurate are listed along with their symptoms and potential solutions.

Problem | Symptoms | Solution
--- | --- | ---
**[Incomplete data](#incomplete)** | Useless models and meaningless results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**[Biased Data](#bias)** | Biased models and biased, inaccurate results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**Wide Data** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature selection](#f-selection). [Feature extraction](#f-extraction). L1 Regularization.
**Sparse data<sup>^</sup>** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature extraction](#f-extraction). Appropriate data representation, i.e. COO, CSR. Appropriate algorithm selection, e.g. factorization  machines.
**Sparse Target Variable** | Single class model predictions. Biased model predictions. | [Proportional Oversampling](#over-samp). Inverse prior probability weighting. Mixture models, e.g. zero-inflated regression methods.
**Outliers** | Biased models and biased, inaccurate results. Unstable parameter estimates and rule generation. Unreliable, out-of-domain predictions. | [Discretization](#discret). [Winsorizing](#winsor). Appropriate algorithm selection, e.g. Huber loss functions.
**Missing Values** | Information loss. Biased models and biased, inaccurate results. | [Imputation](#impute). [Discretization](#discret). Appropriate algorithm selection, e.g. Tree-based models, naive Bayes classification.
**Character Variables<sup>^</sup>** | Information loss. Biased models and biased, inaccurate results. Computational errors. | [Encoding](#encode). Appropriate algorithm selection, e.g. Tree-based models, naive Bayes classification.
**High Cardinality Categorical Variables** | Over-fit models and inaccurate results. Long, intolerable compute times. Unreliable, out-of-domain predictions. | [Rate-by-level](#r-by-level) or variants e.g. perturbed rate-by-level or [Weight of Evidence](http://support.sas.com/documentation/cdl/en/prochp/66409/HTML/default/viewer.htm#prochp_hpbin_details02.htm). [Average-, Median, BLUP-by-level](#a-by-level) [Discretization](#discret). Embedding approaches, e.g. entity embedding neural networks, factorization machines.
**Disparate Variable Scales** | Unreliable parameter estimates, biased models, and biased, inaccurate results. | [Standardization](#standard), Appropriate algorithm selection, e.g. Tree-based models.
**Strong Multicollinearity (correlation)** | Unstable parameter estimates, unstable rule generation, and unstable predictions. | [Feature selection](#f-selection). [Feature extraction](#f-extraction). L2 Regularization.
**Dirty Data** | Information loss. Biased models and biased, inaccurate results. Long, intolerable compute times. Unstable parameter estimates and rule generation. Unreliable out-of-domain predictions. | Combination of solution strategies.

^ In some cases this is not a problem at all. Some algorithms and software packages handle this automatically and elegantly ... some don't.

<a name='incomplete'/>
#### Incomplete data

<a name='bias'/>
#### Biased data

<a name='f-selection'/>
#### Feature selection

<a name='f-extraction'/>
#### Feature extraction

<a name='over-samp'/>
#### Over sampling

<a name='encode'/>
#### Encoding

<a name='discret'/>
#### Discretization

<a name='winsor'/>
#### Winsorizing

<a name='impute'/>
#### Imputation

<a name='r-by-level'/>
#### Rate-by-level

<a name='a-by-level'/>
#### Average-by-level

<a name='standard'/>
#### Standardization
