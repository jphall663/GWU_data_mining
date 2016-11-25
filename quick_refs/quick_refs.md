## Quick references

* [Glossary](#glossary)
* [Best Practices](#best-practices)
* [Algorithms: Part 1](#algos-1)
* [Algorithms: Part 2](#algos-2)

<a name='glossary' />
## Glossary

Term | Definition| 
------------ | ------------- | 
**Autoencoder** | An extension of the Deep Learning framework. Can be used to compress input features (similar to PCA). Sparse autoencoders are simple extensions that can increase accuracy. Use autoencoders for:<br>- generic dimensionality reduction (for pre-processing for any algorithm)<br>-  anomaly detection (for comparing the reconstructed signal with the original to find differences that may be anomalies)<br>- layer-by-layer pre-training (using stacked auto-encoders)
**Backpropogation** | Uses a known, desired output for each input value to calculate the loss function gradient for training. If enabled, performed after each training sample in [**Deep Learning**](#DL). |
**Balanced classes** | Oversampling the minority classes to balance the distribution. 
**Beta constraints** | Supplied maximum and minimum values for the predictor (Beta) parameters, typicaly for GLMs.
**Binary** | A variable with only two possible outcomes. Refer to [**binomial**](#Binomial).
<a name="Binomial"></a>**Binomial** |  A variable with the value 0 or 1. Binomial variables assigned as 0 indicate that an event hasn't occurred or that the observation lacks a feature, where 1 indicates occurrence or instance of an attribute.
**Bins** | Bins are linear-sized from the observed min-to-max for the subset that is being split. Large bins are enforced for shallow tree depths. Based on the tree decisions, as the tree gets deeper, the bins are distributed symmetrically over the reduced range of each subset. 
<a name="Categorical"></a>**Categorical** | A qualitative, unordered variable (for example, *A*, *B*, *AB*, and *O* would be values for the category *blood type*); synonym for [enumerator](#Enum) or [factor](#Factor). <a name="Classification"></a>**Classification** | A model whose goal is to predict the category for the [**response**](#Response) input.
<a name="Cloud"></a>**Cloud** | Synonym for a linked cluster of computers.  Refer to the definition for [cluster](#Cluster). 
<a name="Cluster"></a>**Cluster** | 1. A group of computing nodes that work together; when a job is submitted to a cluster, all the nodes in the cluster work on a portion of the job. Synonym for [**cloud**](#Cloud). <br>2. In statistics, a cluster is a group of observations from a data set identified as similar according to a particular clustering algorithm.</br>
**Confusion matrix** | Table that depicts the performance of the algorithm (using the false positive rate, false negative, true positive, and true negative rates). 
<a name="Continuous"></a>**Continuous** | A variable that can take on all or nearly all values along an interval on the real number line (for example, height or weight). The opposite of a [**discrete**](#Discrete) value, which can only take on certain numerical values (for example, the number of patients treated).
**CSV file** | CSV is an acronym for comma-separated value. A CSV file stores data in a plain text format. 
<a name="DL"></a>**Deep Learning** | Uses a composition of multiple non-linear transformations to model high-level abstractions in data. See also [LeCun, Bengio and Hinton 2015](http://www.nature.com/nature/journal/v521/n7553/full/nature14539.html).
<a name="Dependent"></a>**Dependent variable** | The [**response**](#Response) column in a data set; what you are trying to measure, observe, or predict. The opposite of an [**independent variable**](#Independent).
**Deviance** | Deviance is the difference between an expected value and an observed value. It plays a critical role in defining GLM models. For a more detailed discussion of deviance.
<a name="DistKV"></a>**Distributed key/value (DKV)**| Distributed key/value store. Refer also to [**key/value store**](#KVstore). 
<a name="Discrete"></a>**Discrete** | A variable that can only take on certain numerical values (for example, the number of patients treated). The opposite of a [**continuous**](#Continuous) variable. 
<a name="Enum"></a>**Enumerator/enum** | A data type where the value is one of a defined set of named values known as "elements", "members", or "enumerators." For example, *cat*, *dog*, & *mouse* are enumerators of the enumerated type *animal*. 
<a name="Epoch"></a>**Epoch** | A round or iteration of model training or testing. Refer also to [**iteration**](#Iteration).
<a name="Factor"></a>**Factor** | A data type where the value is one of a defined set of categories. Refer to [**Enum**](#Enum) and [**Categorical**](#Categorical). 
**Family** | The distribution options available for predictive modeling in GLM. 
**Feature** | Synonym for attribute, predictor, or independent variable. Usually refers to the data observed on features given in the columns of a data set.  
**Feed-forward** | Associates input with output for pattern recognition. 
**Gzipped (gz) file** | Gzip is a type of commonly used file compression. 
**HEX format** |  Records made up of hexadecimal numbers representing machine language code or constant data.
<a name="Independent"></a>**Independent variable** | The factors can be manipulated or controlled (also known as predictors). The opposite of a [**dependent variable**](#Dependent). 
**Hit ratio** | (Multinomial only) The number of times the prediction was correct out of the total number of predictions. 
**Integer** | A whole number (can be negative but cannot be a fraction). 
<a name="Iteration"></a>**Iteration** | A round or instance of model testing or training. Also known as an [**epoch**](#Epoch). 
**JVM** | Java virtual machine. 
**Key/value pair** | A type of data that associates a particular key index to a certain datum.
<a name="KVstore"></a>**Key/value store** | A tool that allows storage of schema-less data. Data usually consists of a string that represents the key, and the data itself, which is the value. Refer also to [**distributed key/value**](#DistKV). 
**L1 regularization** | A regularization method that constrains the absolute value of the weights and has the net effect of dropping some values (setting them to zero) from a model to reduce complexity and avoid overfitting. 
**L2 regularization** | A regularization method that constrains the sum of the squared weights. This method introduces bias into parameter estimates but frequently produces substantial gains in modeling as estimate variance is reduced.
**Link function** | A user-defined option in GLM. 
**Loss function** | The function minimized in order to achieve a desired estimator; synonymous to objective function and criterion function. For example, linear regression defines the set of best parameter estimates as the set of estimates that produces the minimum of the sum of the squared errors. Errors are the difference between the predicted value and the observed value.  
**MSE** | Mean squared error; measures the average of the squares of the error rate (the difference between the predictors and what was predicted). 
**Multinomial** | A variable where the value can be one of more than two possible outcomes (for example, blood type). 
**N-folds** | User-defined number of cross validation models. 
**Node** | In distributed computing systems, nodes include clients, servers, or peers. In statistics, a node is a decision or terminal point in a classification tree.
**Numeric** | A column type containing real numbers, small integers, or booleans. 
**Offset** | A parameter that compensates for differences in units of observation (for example, different populations or geographic sizes) to make sure outcome is proportional. 
**Parse** | Analysis of a string of symbols or datum that results in the conversion of a set of information from a person-readable format to a machine-readable format.
**POJO** | Plain Old Java Object; a way to export a model and implement it in a Java application. 
<a name="Regression"></a>**Regression** | A model where the input is numerical and the output is a prediction of numerical values. Also known as "quantitative"; the opposite of a [**classification**](#Classification) model.  
<a name="Response"></a>**Response column** | The [**dependent**](#Dependent) variable in a model or data set. 
**Real** | A fractional number. 
**ROC Curve** | Graph representing the ratio to true positives to false positives. 
**Scoring history** | Represents the error rate of the model as it is built.
**Seed** | A starting point for randomization. Seed specification is used when machine learning models have a random component; it allows users to recreate the exact "random" conditions used in a model at a later time. 
**Separator** | What separates the entries in the dataset; usually a comma, semicolon, etc.
**Sparse** | A dataset where many of the rows contain blank values or "NA" instead of data.  
**Standard deviation** | The standard deviation of the data in the column, defined as the square root of the sum of the deviance of observed values from the mean divided by the number of elements in the column minus one. Abbreviated *sd*. 
**Standardization** | Transformation of a variable so that it is mean-centered at 0 and scaled by the standard deviation; helps prevent precision problems. 
**Supervised learning** | Model type where the input is labeled so that the algorithm can identify it and learn from it. 
**Unsupervised learning** | Model type where the input is not labeled. 
**Validation** | An analysis of how well the model fits. 
**Variable importance** | Represents the statistical significance of each variable in the data in terms of its affect on the model. 
**Weights** | A parameter that specifies certain outcomes as more significant (for example, if you are trying to identify incidence of disease, one "positive" result can be more meaningful than 50 "negative" responses). Higher values indicate more importance. 
**XLS file** | A Microsoft Excel 2003-2007 spreadsheet file format. 
**YARN** | Yet Another Resource Manager; used to manage Hadoop clusters. 

#### Copyright (c) 2016 by H2O.ai team
#### Source: https://github.com/h2oai/h2o-3/blob/master/h2o-docs/src/product/tutorials/glossary.md

<a name='best-practices' />
## Best Practices
![Alt text](low_res_PNG/MLQuickRefBestPractices.png?raw=true "General Best Practices Table")

#### Copyright (c) 2016 by SAS Institute
#### Source: https://github.com/sassoftware/enlighten-apply/tree/master/ML_tables

<a name='algos-1' />
## Algorithms: Part 1
![Alt text](low_res_PNG/MLQuickRefAlgos1.PNG?raw=true "Mostly Supervised Algo Table")

#### Copyright (c) 2016 by SAS Institute
#### Source: https://github.com/sassoftware/enlighten-apply/tree/master/ML_tables

<a name='algos-2' />
## Algorithms: Part 2
![Alt text](low_res_PNG/MLQuickRefAlgos2.PNG?raw=true "Mostly Unupervised Algo Table")

#### Copyright (c) 2016 by SAS Institute
#### Source: https://github.com/sassoftware/enlighten-apply/tree/master/ML_tables