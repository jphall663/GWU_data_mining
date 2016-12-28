## Interpreting Machine Learning

## Contents

### Part 1: Seeing all your data
[Correlation graphs](#corr-graph)</br>
[2-D projections](#2d-proj)</br>
[Glyphs](#glyph)

### Part 2: Using machine learning in regulated industry
[OLS regression alternatives](#ols-alt)</br>
[Build toward machine learning model benchmarks](#ml-benchmark)</br>
[Machine learning in traditional analytics processes](#ml-process)</br>
[Small, interpretable ensembles](#small-ensembles)

### Part 3: Understanding complex machine learning models
[Surrogate models](#surr-mod)</br>
[Local Interpretable Model-agnostic Explanations](#lime)</br>
[Maximum activation analysis](#max-act)</br>
[Constrained neural networks](#constr-nn)</br>
[Variable importance measures](#var-imp)</br>
[Partial dependence plots](#par-dep)</br>
[TreeInterpreter](#treeint)</br>
[Residual analysis](#res-analysis)

<a name='corr-graph'/>
## Correlation Graphs

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.001.png)

The nodes of this graph are the variables in a data set. The weights between the nodes are defined by the absolute value of their pairwise 
Pearson correlation. 

To create:
calculate Pearson correlation between columns/variables
build undirected graph where each node is a column/variable
connection weights between nodes are defined by Pearson correlation absolute values; weights below a certain threshold are not displayed
node size is determined by number of connections (node degree)
node color is determined by a graph communities calculation 
node position is defined by a graph force field algorithm

Free graph software: https://gephi.org/

**How does it enhance understanding?**

By visually displaying relationships between columns

**How does it enhance trust?**

Model reflects graph/graph reflects model

Trust is increased if known relationships are displayed and/or correct modeling results are reflected in the graph - also if patterns are stable or change predictably over time 

Stability to perturbation of the data, stability over time

<a name='2d-proj'/>
## 2-D projections

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.002.png)

There are numerous types of useful projections (or “embeddings”):
Principal Component Analysis (PCA)
Multidimensional Scaling (MDS)
t-SNE (t-distributed Stochastic Neighbor Embedding)
Autoencoder networks

Here PCA and autoencoders are shown - better scalability than many other methods

Autoencoder projections can be augmented by training clusters in the original high dimensional data before projecting into lower dimensional space - look for clusters to be preserved in 2-D projections and confirm cluster relationships are reasonable on 2-D plots. For instance older, richer customers should be relatively far from younger, less affluent customers.

**How does it enhance understanding?**

all records are shown in a single 2-D plot

**How does it enhance trust?** 

Trust is increased if known or expected structures (i.e. clusters, outliers, hierarchy, sparsity) are preserved and displayed in 2-D plots - also if patterns are stable or change predictably over time

Stability to perturbation of the data, stability over time

<a name='glyph'/>
## Glyphs

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.003.png)
![alt text](readme_pics/Interpretable_Machine_Learning_Pics.004.png)

Glyphs are typically much easier to digest than just staring at plain rows of data

Here the four variables are represented by their position in a square and their values are represented by a color.

**How does it enhance understanding?**

Glyphs are typically much easier to digest than just staring at plain rows of data

**How does it enhance trust?**

<a name='ols-alt'/>
## OLS regression alternatives

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.005.png)

Penalized regression:
-   Penalized regression techniques are particularly well-suited for wide data. 
Avoid the multiple comparison problem that can arise with stepwise variable selection. 
They can be trained on datasets with more columns than rows. 
They preserve interpretability by selecting a small number of original variables for the final model using L1 regularization
Nearly always predictive
 
(L1 also works to increase interpretability across many different types of models.)

Fewer assumptions
Well suited for N << p
No multiple comparison issues during variable selection
Preserves interpretability by selecting a small number of variables (L1 penalty) 

GAMs:
-  Generalized additive models fit linear terms to certain variables and nonlinear splines to other variables
Allowing you to hand-tune a trade-off between interpretability and accuracy
Can be predictive based on the application

Fit linear terms to certain variables
Fit nonlinear splines to other variables
Hand-tune a trade-off between interpretability and accuracy 

Quantile regression: 
-  Fit a traditional, interpretable linear model to different percentiles of your training data 
 Allowing you to find different sets of variables for modeling different behaviors across a customer market or portfolio of accounts
more inferential than predictive 

Fit an interpretable linear model to different percentiles of training data
Find different sets of drivers across percentiles of an entire customer market or portfolio of accounts

https://web.stanford.edu/~hastie/local.ftp/Springer/OLD/ESLII_print4.pdf

**How does it enhance understanding?**

It is the same understandable, trust worthy models used in different ways

**How does it enhance trust?**

having less assumptions
By being more accurate
not just modeling the mean

<a name='ml-benchmark'/>
## Build toward machine learning model benchmarks

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.006.png)

Machine learning models typically incorporate a large number of implicit variable interactions and easily fit nonlinear, non-polynomial patterns in data. If a traditional regression model is much less accurate than a machine learning model, the traditional regression model may be missing important interactions or a piecewise modeling approach maybe necessary.

Machine learning models often take into consideration a large number of implicit variable interactions
-   If your regression model is much less accurate than your ML model, you’ve probably missed some important interaction(s)
-   Decision trees area great way to see the potential interactions
Important interactions may only be occurring at certain values of certain variables

ML models intrinsically allow:
high degree interactions between input variables - include 2nd, 3rd degree interactions to approximate
nonlinear, nonpolynomial behavior across the domain of a single input variable - use piecewise models to approximate

**How does it enhance understanding?**

**How does it enhance trust?**

It helps us make our understandable, trust worthy models more accurate

<a name='ml-process'/>
## Machine learning in traditional analytics processes

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.007.png)

How does it increase trust and understanding?
It helps us make our understandable, trust worthy models more accurate and helps us use them more efficiently

Introduce nonlinear predictors into the model
(Predictors that capture more complex, nonlinear, nonpolynomial relationships)

Based on past model performance data:
     -  Use an ML model as a gate to pick which linear model to use
      - Use a machine learning model to predict when traditional deployed models need to be retrained or replaced before their predictive power lessen

**How does it enhance understanding?**

**How does it enhance trust?**

It helps us make our understandable, trust worthy models more accurate and helps us use them more efficiently

<a name='small-ensembles'/>
## Small, interpretable ensembles

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.008.png)

**How does it enhance understanding?**

It allows us to boost the accuracy of traditional trustable models without sacrificing too much interpretability

**How does it enhance trust?**

It increases trust if models compliment each other in expected ways, e.g. 
A logistic regression model that is good at rare events slightly increases a good decision tree model that is not good at rare events in the presence of rare events

<a name='surr-mod'/>
## Surrogate models

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.009.png)

First fit a complex machine learning model to your training data. 

Then train a single decision tree on the original training data, but instead of using the actual target in the training data, use the predictions of the more complex algorithm as the target for this single decision tree.

Interpretable models used as a proxy to explain complex models
For example:
Fit a complex machine learning model to your training data. 
Then train a single decision tree on the original training data, but use the predictions of the more complex algorithm as the target for this single decision tree
This single decision tree will likely* be a more interpretable proxy you can use to explain the more complex machine learning model

*  Few (possibly no?) theoretical guarantees that the surrogate model is highly representative of the more complex model

**How does it enhance understanding?**

It helps us understand the inner workings of a complex system

**How does it enhance trust?**

It increases trust if we can see the logic in the surrogate model matches our domain experience or expectation
It increases trust if the logic is stable under mild perturbations of the data 

<a name='lime'/>
## Local Interpretable Model-agnostic Explanations
![alt text](readme_pics/Interpretable_Machine_Learning_Pics.010.png)

Pick or simulate ‘marker’ records/examples 
Score them for probability or value of target with complex ML model 
Choose a ‘query’ record/example with a prediction to be explained 
Weight ‘marker’ records/examples closest to the query record/example 
Train an L1 regularized linear model on the data set of ‘marker’ records/examples
The parameters of the linear model will help explain the prediction for the ‘query’ record/example

-   Local surrogate model + more structured type of activation analysis
You can include ‘marker’ records/examples in your training data 
For traditional analytics data, explanatory data samples could potentially be simulated – e.g. customers with highest, lowest, and median credit scores

https://www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime
https://arxiv.org/pdf/1606.05386.pdf

**How does it enhance understanding?**

It helps us understand the predictions made for key observations
It helps us understand the behavior of the model at local, important places no matter how complex the global model is

**How does it enhance trust?**

It increases trust because we can see how the model makes decisions for key observations 
It increases trust if we see decisions being made about similar observations being made in similar ways

<a name='max-act'/>
## Maximum activation analysis

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.011.png)

Examples are found or simulated that maximally activate certain neurons, layers, or filters in a neural network or certain nodes or trees in decision tree models.

Which data creates the maximum output from certain neurons
Which neurons create the maximum output for some archetypal data example
You can include ‘marker’ records/examples in your training data 

http://yosinski.com/deepvis
http://yosinski.com/media/papers/Yosinski__2015__ICML_DL__Understanding_Neural_Networks_Through_Deep_Visualization__.pdf

**How does it enhance understanding?**

It increases understanding because it elucidates the structure of the model
(If we have dogs and cats in our data we would expect certain neurons to maximally learn certain visually features, i.e. dog nose neuron is activated for all dog picks, but  not in cat pictures)
It increases understanding because see interactions when input units activate the same hidden unit consistently

**How does it enhance trust?**

It increases trust if we see stability in what units are activated for similar inputs 
It increases trust if similar data points proceed through the model in the same way
It increases trust if interactions and structure match  

<a name='constr-nn'/>
## Constrained neural networks

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.012.png)

Scale inputs to be non-negative
Transform inputs such that their relationship with the target is monotonically increasing or decreasing 
Enables the human user to parse extra information from machine learning models:
In a neural network with only positive weights
For a binary classification task where the target value 1 indicates an event and the target value 0 indicates a non-event
All predictor variables are non-negative and monotonically increasing with respect to the target
Higher values of that predictor lead to increased occurrences of the target event
By following the maximum activation of neurons through the network it may even be possible to determine high-order interactions

Binning does reduce the resolution of the information presented to the model during training
But it can lead to better generalization (intricate patterns in the training data can be noise)
Allows for elegant handling of outliers

**How does it enhance understanding?**

It increases understanding because it we can learn interactions, important variables, and the direction in which a input effects the predicted outcome

**How does it enhance trust?**

It increases trust if these are parsimonious with domain expertise or expectations
It increases trust if similar data points proceed through the model in the same way 
It increases trust if interactions, important features, and direction of an input are consistent for similar data sets

<a name='var-imp'/>
## Variable importance measures

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.013.png)

In Tree:
Split criterion change caused by an input for each node

In RF:
Split criterion change caused by an input for each node
Difference in OOB predictive accuracy when the predictor of interest is shuffled 
(shuffling is seen as ‘zeroing out’ the effect of the variable in the trained model, because other variables are not shuffled)

In GBM:
Split criterion change caused by an input for each node

Simplistic variable importance measures can be biased toward larger scale variables or variables with a large number of categories

**How does it enhance understanding?**

It increases understanding because we can learn important variables and their relative rank 

**How does it enhance trust?**

It increases trust if these rankings match domain expertise or expectations
It increases trust if these ranks are repeatable in similar data

<a name='par-dep'/>
## Partial dependence plots

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.014.png)

https://web.stanford.edu/~hastie/local.ftp/Springer/OLD/ESLII_print4.pdf, pg. 374

“Partial dependence tells us how the value of a variable influences the model predictions after we have averaged out the influence of all other variables. (For linear regression models, the resulting plots are simply straight lines whose slopes are equal to the model parameters.)” 
- https://cran.r-project.org/web/packages/datarobot/vignettes/PartialDependence.html

Can be calculated efficiently for tree-based models, because of tree structure 

Interesting variant: https://github.com/numeristical/introspective

**How does it enhance understanding?**

It increases understanding because we can see the behavior of individual inputs and their 2 way interactions

**How does it enhance trust?**

It increases trust if the displayed behavior is consistent with domain expertise and expectations
It increases trust if displayed behavior is repeatable

<a name='treeint'/>
## TreeInterpreter

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.015.png)

**How does it enhance understanding?**

**How does it enhance trust?**

<a name='res-analysis'/>
## Residual analysis

![alt text](readme_pics/Interpretable_Machine_Learning_Pics.016.png)

**How does it enhance understanding?**

**How does it enhance trust?**