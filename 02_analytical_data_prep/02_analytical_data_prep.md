## Section 02: Analytical Data Prep

A great deal of work in data mining projects is spent on data munging. Below some common problems are listed along with their symptoms and potential solutions.

Problem | Symptoms | Solution
--- | --- | ---
**[Incomplete data](#incomplete)** | Useless models and meaningless results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**[Biased Data](#bias)** | Biased models and biased, inaccurate results. | Get more data. Get better data. [Design of Experiment](https://en.wikipedia.org/wiki/Design_of_experiments) approaches.
**Wide Data** | Long, intolerable compute times. Meaningless results due to curse of dimensionality. | [Feature selection](#f-selection). [Feature extraction](#f-extraction).
**Sparse Target Variable** | Single class model predictions. Biased model predictions. | [Proportional Oversampling](#over-samp). Inverse prior probability weighting. Mixture models.
**Outliers** | Biased models and biased, inaccurate results. Unstable parameter estimates and rule generation. Unreliable, out-of-domain predictions. | [Discretization](#discret). [Winsorizing](#winsor).
**Missing Values** | Information loss. Biased models and biased, inaccurate results. | [Imputation](#impute). [Discretization](#discret). Tree-based models.
**High Cardinality Categorical Variables** | Over-fit models and inaccurate results. Long, intolerable compute times. Unreliable, out-of-domain predictions. | [Rate-by-level](#r-by-level) or variants e.g. perturbed rate-by-level or [Weight of Evidence](http://support.sas.com/documentation/cdl/en/prochp/66409/HTML/default/viewer.htm#prochp_hpbin_details02.htm). [Average-, Median, BLUP-by-level](#a-by-level) [Discretization](#discret). Embedding approaches.
**Disparate Variable Scales** | Unreliable parameter estimates, biased models, and biased, inaccurate results. | [Standardization](#standard)
**Strong Multicollinearity (correlation)** | Unstable parameter estimates, unstable rule generation, and unstable predictions. | [Feature selection](#f-selection). [Feature extraction](#f-extraction). Regularization.
**Dirty Data** | Information loss. Biased models and biased, inaccurate results. Long, intolerable compute times. Unstable parameter estimates and rule generation. Unreliable out-of-domain predictions. | Combination of solution strategies.

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
