## Section 01: Basic Data Prep

#### Basic data operations

A great deal of work in data mining projects is spent on data munging. Below some of the basic operations are illustrated and defined. Code examples are provided in common languages.

![alt text](basic_data_operations.png)

**Subset/Select/Filter/Slice Rows** - Selecting rows or reducing the number of rows in a data set by some criterion.

**Subset/Select/Slice Columns** - Selecting(/variables) or reducing the number of columns(/variables) in a data set by some criterion.

**Sort/Arrange/Order By** - Arranging the rows of a data set in sequential order based on the values of one or more variables.

**Group By** - Grouping the rows of a data set together based on the values of one or more variables.

**Transpose** - Rearranging a data set such that the row and column(/variable) values are switched.

**Merge/Bind** - Combining data sets side-by-side regardless of the values of any variable(s).

**Join/Bind** - Combining data sets side-by-side based on matching values of variables in both data sets.

**Append/Bind** - Stacking data sets bottom-to-top regardless of the values of any variable(s).

#### Code examples
* [Python Pandas](01_basic_data_prep.md#python-pandas---view-notebook) - [view notebook](src/notebooks/py/Py_Part_0_pandas_numpy.ipynb)
* R
  * [Basics, dplyr, and ggplot](01_basic_data_prep.md#r-basics-dplyr-and-ggplot---view-notebook) - [view notebook](src/notebooks/r/R_Part_0_Basics_dplyr_and_ggplot2.ipynb)
  * [data.table](01_basic_data_prep.md#r-datatable---view-notebook) - [view notebook](src/notebooks/r/R_Part_1_data.table.ipynb)
* SAS
  * [Base SAS and PROC SGPLOT](01_basic_data_prep.md#base-sas-and-proc-sgplot---clonedownload-notebook) - [clone/download notebook](src/notebooks/sas)
  * [PROC SQL](01_basic_data_prep.md#sas-proc-sql---clonedownload-notebook) - [clone/download notebook](src/notebooks/sas)

#### Class Notes:
* [Instructor Notes](notes/01_instructor_notes.pdf)
* *Introduction to Data Mining* - [chapter 2 notes](https://www-users.cs.umn.edu/~kumar/dmbook/dmslides/chap2_data.pdf)

#### Required Reading

* *Introduction to Data Mining* - chapter 2, sections 2.1-2.3
* [*Tidy Data*](https://www.jstatsoft.org/article/view/v059i10)

#### [Sample Quiz](quiz/sample/quiz_1.pdf)

#### [Quiz key](quiz/key/quiz_01.pdf)

#### [Assignment](assignment/assignment_1.pdf)

#### [Assignment Key](assignment/key) 

#### Supplementary References
* Simple [benchmark](https://github.com/szilard/benchm-databases) of data processing tools by [@szilard](https://github.com/szilard)

***

#### Python Pandas - [view notebook](src/notebooks/py/Py_Part_0_pandas_numpy.ipynb)
```python

"""
Copyright (C) 2017 J. Patrick Hall, jphall@gwu.edu

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

"""

#%% standard output ###########################################################
# print is the primary function used to write to the console in Python
# print is a *function* in Python 3
# print is a *statement* in Python 2

print('Hello World!') # Python 3
print 'Hello World!'  # Python 2

# an object with no functions or operators is also printed to the console
x = 'Hello World!'
x

#%% importing libraries #######################################################
# python contains many libraries, often called modules
# modules are:
# * nearly always free and open source
# * installed using many different methods - a package manager like conda,
#     readily available through the Anaconda release of Python
#     (https://www.continuum.io/downloads) - is often a good solution for
#     installing and managing packages/modules
# * of relatively high and uniform quality and but licensing can vary
# * imported using the import statement

# import packages
# packages can be aliased using the as statement

import string                   # module with string utilities
import pandas as pd             # module with many utilities for dataframes
import numpy as np              # module with numeric and math utilities
import matplotlib.pyplot as plt # module for plotting

#%% generating a sample data set ##############################################

# set the number of rows and columns for the sample data set
n_rows = 1000
n_vars = 2

### create lists of strings that will become column names
# lists are:
# * a common data structure in python
# * surrounded by square brackets []
# * can contain different data types as list elements
# * often created by a speficic type pythonic syntax, list comprehensions
# * indexed from 0, unlike SAS or R
# * slicable using numeric indices

# list comprehension
# str() converts to string
# range() creates a list of values from arg1 to arg2
num_col_names = ['numeric' + str(i+1) for i in range(0, n_vars)]
num_col_names

# type() can be used to determine the class of an object in python
type(num_col_names)

# anonymous functions
# the lamba statement is used to define simple anonymous functions
# map() is very similar to to lapply() in R
# it applies a function to the elements of a list
char_col_names = map(lambda j: 'char' + str(j+1), range(0, n_vars))
char_col_names

# string.ascii_uppercase is a string constant of uppercase letters
print(string.ascii_uppercase)

# another list comprehension
# slice first seven letters of the string
text_draw = [(letter * 8) for letter in string.ascii_uppercase[:7]]
text_draw

# create a random numerical columns directly using numpy
# the numerical columns will originally be a 2-D numpy array
randoms = np.random.randn(n_rows, n_vars)
randoms[0:5]
type(randoms)

# create numerical columns of Pandas dataframe from numpy array
# notice that a key is generated automatically
num_cols = pd.DataFrame(randoms, columns=num_col_names)
num_cols.head()
type(num_cols)

# create random character columns as a Pandas dataframe
# use numpy sampling function choice() to generate a numpy array of random text
# create Pandas dataframe from numpy 2-D array
char_cols = pd.DataFrame(np.random.choice(text_draw, (n_rows, n_vars)),
                         columns=char_col_names)
char_cols.head()

# use Pandas concat() to join the numeric and character columns
scratch_df = pd.concat([num_cols, char_cols], axis=1)
scratch_df.head()

#%% plotting variables in a dataframe #########################################
# pandas has several builtin plotting utilities
# pandas hist() method to plot a histogram of numeric1

# pandas alllows slicing by dataframes index using ix[]
# ix[:, 0] means all rows of the 0th column - or numeric1
scratch_df.ix[:, 0].plot.hist(title='Histogram of Numeric1')


# use pandas scatter() method to plot numeric1 vs. numeric2
scratch_df.plot.scatter(x='numeric1', y='numeric2',
                        title='Numeric1 vs. Numeric2')

#%% subsetting pandas dataframes ##############################################

### by columns

# subsetting by index
# one column returns a Pandas series
# a Pandas series is like a single column vector
scratch_df.iloc[:, 0].head()
type(scratch_df.iloc[:, 0])

# more than one columns makes a dataframe
# iloc enables location by index
scratch_df.iloc[:, 0:2].head()
type(scratch_df.iloc[:, 0:2])

# subsetting by variable name
scratch_df['numeric1'].head()
scratch_df.numeric1.head()

# loc[] allows for location by column or row label
scratch_df.loc[:, 'numeric1'].head()

# loc can accept lists as an input
scratch_df.loc[:, ['numeric1', 'numeric2']].head()

### by rows

# subsetting by index
scratch_df[0:3]

# selecting by index
scratch_df.iloc[0:5, :]

# select by row label
# here index/key values 0:5 are returned
scratch_df.loc[0:5, :]

### boolean subsetting

scratch_df[scratch_df.numeric2 > 0].head()
scratch_df[scratch_df.char1 == 'AAAAAAAA'].head()
scratch_df[scratch_df.char1.isin(['AAAAAAAA', 'BBBBBBBB'])].head()
scratch_df[scratch_df.numeric2 > 0].loc[5:10, 'char2']

#%% updating the dataframe ####################################################

# must use .copy() or this will be a symbolic link
scratch_df2 = scratch_df.copy()

# pandas supports in place overwrites of data
# overwrite last 500 rows of char1 with ZZZZZZZZ
scratch_df2.loc[500:, 'char1'] = 'ZZZZZZZZ'
scratch_df2.tail()

# iat[] allows for fast location of specific indices
scratch_df2.iat[0, 0] = 1000
scratch_df2.head()

#%% sorting the dataframe #####################################################

# sort by values of one variable
scratch_df2.sort_values(by='char1').head()

# sort by values of multiple variables and specify sort order
scratch_df3 = scratch_df2.sort_values(by=['char1', 'numeric1'],
                                      ascending=[False, True]).copy()
scratch_df3.head()

# sort by the value of the dataframe index
scratch_df2.sort_index().head()

#%% adding data to the dataframe ##############################################
# pandas concat() supports numerous types of joins and merges
# pandas merge() supports joins and merges using more SQL-like syntax
# i.e. merge(left, right, on=)
# pandas append() supports stacking dataframes top-to-bottom

# create a toy dataframe to join/merge onto scratch_df
scratch_df3 = scratch_df3.drop(['numeric1', 'numeric2'] , axis=1)
scratch_df3.columns = ['char3', 'char4']
scratch_df3.tail()

# default outer join on indices
# indices are not in identical, matching order
# this will create 2000 row � 6 column dataset
scratch_df4 = pd.concat([scratch_df, scratch_df3])
scratch_df4

# outer join on matching columns
# axis=1 specificies to join on columns
# this performs the expected join
scratch_df5 = pd.concat([scratch_df, scratch_df3], axis=1)
scratch_df5.head()
scratch_df5.shape

# append
scratch_df6 = scratch_df.append(scratch_df)
scratch_df6.shape

#%% comparing dataframes ######################################################
# Use Pandas equals() to compare dataframes
# Row order is not ignored

scratch_df.equals(scratch_df)
scratch_df.equals(scratch_df.sort_values(by='char1'))
scratch_df.equals(scratch_df2)

#%% summarizing dataframes ####################################################
# Pandas offers several straightforward summarization functions

scratch_df.mean()
scratch_df.mode()
scratch_df.describe()

#%% by group processing #######################################################
# use pandas groupby() to create groups for subsequent processing

# use summary function size() on groups created by groupby()
counts = scratch_df.groupby('char1').size()
plt.figure()
counts.plot.bar(title='Frequency of char1 values (Histogram of char1)')

# groupby the values of more than one variable
group_means = scratch_df.groupby(['char1', 'char2']).mean()
group_means

#%% transposing a table #######################################################
# transposing a matrix simply switches row and columns values
# transposing a dataframe is more complex because of metadata associated with
#   variable names and row indices

# pandas .T performs a transpose
scratch_df.T.iloc[:, 0:5]

# often, instead of simply transposing, a data set will need to be reformatted
#   in a melt/stack -> column split -> cast action described in Hadley
#   Wickham's *Tidy Data*:
#   https://www.jstatsoft.org/article/view/v059i10
#
# see the stack and unstack methods for Pandas dataframes

#%% exporting and importing a dataframe
# many to_* methods available for exporting dataframes to other formats
# many read_* methods available for creating dataframes from other formats

# export to csv
scratch_df.to_csv('scratch.csv')

# import from csv
scratch_df7 = pd.read_csv('scratch.csv')

```

#### R Basics, dplyr, and ggplot - [view notebook](src/notebooks/r/R_Part_0_Basics_dplyr_and_ggplot2.ipynb)
```r

###############################################################################
# Copyright (C) 2017 J. Patrick Hall, jphall@gwu.edu
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

### standard output ###########################################################
# two primary R core functions are used to print information to the console
#   print() and cat()
# print is a generic function that responds differently to different classes
#   of R objects
# note that '.' is just a character, it does not denote object membership
#   as in Java and Python
# cat() simply attempts to print string literals
# an object with no functions or operators is also printed to the console

x <- 'Hello World!'
print(x)
cat(x)
x

class(x) <- 'some.class'
print(x)
cat(x)
x

### import packages ###########################################################

# R contains thousands of packages for many different purposes
# Packages are:
#   - nearly always free and open source
#   - installed using the install.packages() function or a GUI command
#   - of varying quality and licensing
#   - loaded using the library() function, after being installed

library(dplyr)    # popular package for data wrangling with consistent syntax
library(ggplot2)  # popular package for plotting with consistent syntax

# surpress warnings about versions and object masking
# using suppressPackageStartupMessages()
# suppressPackageStartupMessages(library(dplyr))
# suppressPackageStartupMessages(library(ggplot2))

### working directory #########################################################

# enter the directory location of this file within single quotes
# '<-' is the preferred assignment operator in R
# '/' is the safest directory separator character to use

git_dir <- '/path/to/GWU_data_mining/01_basic_data_prep/src/raw/r'

# set the working directory
# the working directory is where files are written to and read from by default
# setwd() sets the working directory
# getwd() prints the current working directory
setwd(git_dir)
getwd()

### generate a sample data set ################################################

# set the number of rows and columns for the sample data set
n_rows <- 1000
n_vars <- 5

# create a key variable
# a key variable has a unique value for each row of a data set
# seq() generates values from a number (default = 1), to another number, by
#   a certain value (default = 1)
# many types of data structures in R have key variables (a.k.a. row names) by
#   default
key <- seq(n_rows)

# show the first five elements
# most data structures in R can be 'sliced', i.e. using numeric indices
#   to select a subset of items
key[1:5]

# create lists of strings that will become column names
# paste() concatentates strings with a separator character in between them
num_vars <- paste('numeric', seq_len(n_vars), sep = '')
num_vars

char_vars <- paste('char', seq_len(n_vars), sep = '')
char_vars

# initialize a data.frame with the key variable
scratch_df <- data.frame(INDEX = key)

# add n_var numeric columns, each with n_row rows, to the data.frame
# each column contains random uniform numeric values generated by runif()
# replicate() replicates n_row length lists of numeric values n_vars times
scratch_df[, num_vars] <- replicate(n_vars, runif(n_rows))

# head() displays the top of a data structure
head(scratch_df)

# add n_var character columns, each with n_row rows, to the data.frame
# create a list of strings from which to generate random text variables
# sapply() applies a function to a sequence of values
# LETTERS is a character vector containing uppercase letters
# an anonymous function is defined that replicates a value 8 times with no
#   seperator character
# replicate() replicates n_var lists of n_row elements from text_draw sampled
#   randomly from test_draw using the sample() function
text_draw <- sapply(LETTERS[1:7],
                    FUN = function(x) paste(rep(x, 8), collapse = ""))
text_draw

scratch_df[, char_vars] <- replicate(n_vars,
                                     sample(text_draw, n_rows, replace = TRUE))
head(scratch_df)

# convert from standard data.frame to dlpyr table
# dplyr is a popular, intuitive, and effcient package for manipulating data sets
# R has many data types: http://www.statmethods.net/input/datatypes.html
scratch_tbl <- tbl_df(scratch_df)

# use the dplyr::glimpse function to see a summary of the generated data set
glimpse(scratch_tbl)

### plotting variables in the table ###########################################
# ggplot allows you to overlay graphics using the '+' operator
# plot univariate densities of numeric1 and char1 using the geom_bar()
#   components
# gtitle adds title
# coord_flip rotates the bar chart

ggplot(scratch_tbl, aes(numeric1)) +
  geom_bar(stat = "bin", fill = "blue", bins = 100) +
  ggtitle('Histogram of Numeric1')

ggplot(scratch_tbl, aes(char1)) +
  geom_bar(aes(fill=char1)) +
  ggtitle('Histogram of Char1') +
  coord_flip()

### subsetting the table ######################################################

# subset variables using dplyr::select
# subset a range of variables with similar names and numeric suffixes
# subset all the variables whose names begin with 'char'
# subset variables by their names
num_vars <- select(scratch_tbl, num_range('numeric', 1:n_vars))
head(num_vars)

char_vars <- select(scratch_tbl, starts_with('char'))
head(char_vars)

mixed_vars <- select(scratch_tbl, one_of('numeric1', 'char1'))
head(mixed_vars)

# subset rows using multiple dplyr functions
# subset rows using their numeric indices
# subset top rows based on the value of a certain variable
# subset rows where a certain variable has a certain value
some_rows <- slice(scratch_tbl, 1:10)
some_rows

sorted_top_rows <- top_n(scratch_tbl, 10, numeric1)
sorted_top_rows

AAAAAAAA_rows <- filter(scratch_tbl, char1 == 'AAAAAAAA')
head(AAAAAAAA_rows)

### updating the table ########################################################
# dplyr, as a best practice, does not support in-place overwrites of data

# dplyr::transform enables the creation of new variables from existing
#   variables
scratch_tbl2 <- transform(scratch_tbl,
                          new_numeric = round(numeric1, 1))
head(scratch_tbl2)

# dplyr::mutate enables the creation of new variables from existing
#   variables and computed variables
scratch_tbl2 <- mutate(scratch_tbl,
                       new_numeric = round(numeric1, 1),
                       new_numeric2 = new_numeric * 10)
head(scratch_tbl2)

# dplyr::transmute enables the creation of new variables from existing
#   variables and computed variables, but keeps only newly created variables
scratch_tbl2 <- transmute(scratch_tbl,
                          new_numeric = round(numeric1, 1),
                          new_numeric2 = new_numeric * 10)
head(scratch_tbl2)

### sorting the table #########################################################
# sort tables using dplyr::arrange
# sort by one variable
# sort by two variables

sorted <- arrange(char_vars, char1)
head(sorted)

sorted2 <- arrange(char_vars, char1, char2)
head(sorted2)

### adding data to the table ##################################################
# add data to a table using dplyr:: bind and dplyr::join
# bind smashes tables together
# join combines tables based on matching values of a shared variable

bindr <- bind_rows(sorted, sorted2)
nrow(bindr)

bindc <- bind_cols(sorted, sorted2)
ncol(bindc)

# create two tables to join on a key variable
sorted_left <- arrange(select(scratch_tbl, one_of('INDEX', 'char1')), char1)
right <- select(scratch_tbl, one_of('INDEX', 'numeric1'))

# Perform join
# joined table contains `char1` from the left table
#   and `numeric1` from the right table
#  matched by the value of `INDEX`
joined <- left_join(sorted_left, right, by = 'INDEX')
head(joined)

### comparing tables ##########################################################
# comparing tables using dplyr::all.equal
# dplyr::all.equal will test tables for equality despite the order of rows
#   and/or columns
# very useful for keeping track of changes to important tables

# Create a table for comparision
test <- select(scratch_tbl, one_of('INDEX', 'numeric1', 'char1'))

# Compare
print(all.equal(joined, test, ignore_row_order = FALSE))
print(all.equal(joined, test, ignore_col_order = FALSE))
print(all.equal(joined, test))

### summarizing tables ########################################################
# combine rows of tables into summary values with dplyr::summarise and
#   dplyr::summarise_each
# summarize one variable using summarise, avg is the name of the created var
# summarize many variables using summarise_each, funs() defines the summary
#   function

ave <- summarise(num_vars, avg = mean(numeric1))
ave

all_aves <-summarise_each(num_vars, funs(mean))
all_aves

### by group processing #######################################################
# By groups allow you to divide and process a data set based on the values of
#   one or more variables
# dplyr::group_by groups a data set together based on the values of a certain
#   variable
# operations can then be applied to groups
grouped <- group_by(joined, char1)
grouped <- summarise(grouped, avg = mean(numeric1))
grouped

### Transposing a table #######################################################
# Transposing a matrix simply switches row and columns values
# Transposing a data.frame or dplyr table is more complex because of metadata
#   associated with variable names and row indices

transposed = t(scratch_tbl)
glimpse(transposed)

# Often, instead of simply transposing, a data set will need to be reformatted
# in a melt/stack-column split-cast action described in Hadley Wickham's
# 'Tidy Data' https://www.jstatsoft.org/article/view/v059i10
# see also dplyr::gather and dplyr::spread()

### exporting and importing the table #########################################
# the R core function write.table enables writing text files
# the similar R core function read.table enables reading text files

# export
# use the sep option to specifiy the columns delimiter character
# row.names = FALSE indicates not to save the row number to the text file
filename <- paste(git_dir, 'scratch.csv', sep = '/')
write.table(scratch_tbl, file = filename, quote = FALSE, sep = ',',
            row.names = FALSE)

# import
import <- read.table(filename, header = TRUE, sep = ',')
```

#### R data.table - [view notebook](src/notebooks/r/R_Part_1_data.table.ipynb)
```r

###############################################################################
# Copyright (C) 2017 J. Patrick Hall, jphall@gwu.edu
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

### data.table is an efficient package for manipulating data sets #############
# data.table is implemented in optimized C and often attempts to update
#   items by reference to avoid copying large amounts of data
# data.table is a subclass of data.frame and generally accepts data.frame
#   syntax
# general form of a data.table is dt[i, j, by]
#   i is row index, indexed from 1 ...
#   j is col index, indexed from 1 ...
#   by is by-group var name

library(data.table)

# enter the directory location of this file within single quotes
git_dir <- '/path/to/GWU_data_mining/01_basic_data_prep/src/raw/r'

# set the working directory
setwd(git_dir)
getwd()

### generate a sample data set ################################################

# set the number of rows and columns for the sample data set
n_rows <- 1000
n_vars <- 3

# create a key variable
key <- seq(n_rows)

# create lists of strings that will become column names
num_vars <- paste('numeric', seq_len(n_vars), sep = '')
char_vars <- paste('char', seq_len(n_vars), sep = '')

# create a list of strings from which to generate random text variables
text_draw <- sapply(LETTERS[1:7],
                    FUN = function(x) paste(rep(x, 8), collapse = ""))

# create a sample data.table
scratch_dt <- data.table(key,
                         replicate(n_vars, runif(n_rows)),
                         replicate(n_vars, sample(text_draw, n_rows,
                                                  replace = TRUE)))

# the data.table::set* family of methods in data.table always updates items
#   by reference for efficiency
setnames(scratch_dt, c('key', num_vars, char_vars))
scratch_dt

### plotting ##################################################################
# data.table enables simple plotting for numeric variables

scratch_dt[,plot(numeric1, numeric2)]

### subsetting the table ######################################################

### by column

# selecting a single column results in a vector
class(scratch_dt[,char1])
length(scratch_dt[,char1])

# multiple columns can be selected

# specifying multiple columns by a vector results in a concatenated vector
class(scratch_dt[,c(numeric1, char1)])
length(scratch_dt[,c(numeric1, char1)])

# specifying multiple columns by list results in a data.table
class(scratch_dt[,list(numeric1, char1)])
scratch_dt[,list(numeric1, char1)]

# '.' is an alias for 'list'
class(scratch_dt[,.(numeric1, char1)] )
scratch_dt[,.(numeric1, char1)]

# computed columns
scratch_dt[1:5, round(numeric1, 1)] # compute standalone vector
scratch_dt[, .(new_numeric = round(numeric1, 1))] # assign name

### by row

scratch_dt[3:5] # use numeric indices/slicing
scratch_dt[3:5,]
scratch_dt[char1 == 'DDDDDDDD']
scratch_dt[char1 %in% c('DDDDDDDD', 'EEEEEEEE')]

# .N contains the number of rows or the last row
scratch_dt[.N]
scratch_dt[,.N]

### sorting the table #########################################################

# data.table::setorder reorders columns by reference
sorted <- setorder(scratch_dt, char1)
sorted

# when used in data.table order() also reorders columns by reference
sorted <- scratch_dt[order(char1)]
sorted

# sort orders can be specified by using order()
sorted2 <- scratch_dt[order(char1, -numeric1)]
sorted2

# data.table::setkey reorders columns by reference by the specified key
#  variable (here called 'key') and sets the variable to the key of the
#  data.table for future operations
# subsetting and selecting by the key variable will be more efficient
#  in future operations
sorted3 <- setkey(scratch_dt, key)
sorted3

### updating the table ########################################################

# update rows by reference using the := operator
# data.table supports overwrite of data
scratch_dt2 <- scratch_dt[key > 500, char1 := 'ZZZZZZZZ']
scratch_dt2

# create new columns by reference using the := operator
scratch_dt2[, new_numeric := round(numeric1, 1)]
scratch_dt2  

### adding data to the table ##################################################

# use data.table::rbindlist to stack data.tables vertically
bindr <- rbindlist(list(sorted, sorted2))
nrow(bindr)

# data.table::merge joins tables side-by-side using a common key variable
# joining data.tables without prespecified keys (i.e. by using data.table::setkey)
#   requires that a key for the join be specified
# The prefix 'x.' is added to the left table variable names by default
# The prefix 'y.' is added to the right table variables names by default
joined1 <- merge(sorted, sorted2, by = c('key'))
joined1

# joining data.tables with prespecified keys does not require that a key be
#   specified when data.table::merge is called
# Add a key to the scratch_dt2 table
scratch_dt2 <- setkey(scratch_dt2[,.(key, char1, new_numeric)], key)
scratch_dt2

# Now sorted3 and scratch_dt2 can be joined without specifiying a key
joined2 <- merge(sorted3, scratch_dt2)
joined2

### by group processing #######################################################
# by groups allow you to divide and process a data set based on the values
#   of a certain variable
# general form of a data.table is dt[i, j, by]
#   by is by group variable name

scratch_dt2[, sum(new_numeric), by = char1]
scratch_dt2[1:500, sum(new_numeric), by = char1]

# .N returns the number of rows in each by group
scratch_dt2[, .N, by = char1]

# by groups can also be a list
scratch_dt[, mean(new_numeric), by = .(char1, char2)]

# .SD represents all the variables except the by variable(s)
scratch_dt2[, lapply(.SD, sum), by = char1]

# .N can be used to find the first and last rows of each by group
scratch_dt2[, .SD[c(1, .N)], by = char1]

### operations can be chained #################################################

# chaining
scratch_dt2[, .(new_numeric2 = sum(new_numeric)), by = char1][new_numeric2 > 40]

# no chaining
scratch_dt3 <- scratch_dt2[, .(new_numeric2 = sum(new_numeric)), by = char1]
scratch_dt3[new_numeric2 > 40]

### Transposing a table #######################################################
# Transposing a matrix simply switches row and columns values
# Transposing a data.frame or data.table is more complex because of metadata
#   associated with variable names and row indices

transposed = t(scratch_dt)
str(transposed)

# Often, instead of simply transposing, a data set will need to be reformatted
# in a melt/stack-column split-cast action described in Hadley Wickham's
# 'Tidy Data' https://www.jstatsoft.org/article/view/v059i10
# see also dcast.data.table and melt.data.table

### exporting and importing the table #########################################
# fread and fwrite allow for optimized file i/o
# fwrite only availabe in data.table version > 1.9.7
# available from http://Rdatatable.github.io/data.table

# use fwrite to write a file
fwrite(scratch_dt, 'scratch_dt.csv')

# use fread to read a file
scratch_dt <- fread('scratch_dt.csv')
head(scratch_dt)
```

#### Base SAS and PROC SGPLOT - [clone/download notebook](src/notebooks/sas)
```sas

******************************************************************************;
* Copyright (C) 2015 by SAS Institute Inc., Cary, NC 27513 USA               *;
*                                                                            *;
* Licensed under the Apache License, Version 2.0 (the "License");            *;
* you may not use this file except in compliance with the License.           *;
* You may obtain a copy of the License at                                    *;
*                                                                            *;
*   http://www.apache.org/licenses/LICENSE-2.0                               *;
*                                                                            *;
* Unless required by applicable law or agreed to in writing, software        *;
* distributed under the License is distributed on an "AS IS" BASIS,          *;
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   *;
* See the License for the specific language governing permissions and        *;
* limitations under the License.                                             *;
******************************************************************************;

******************************************************************************;
* NOTE: examples are meant for the free SAS University Edition               *;
* to install see: http://www.sas.com/en_us/software/university-edition.html  *;
******************************************************************************;

******************************************************************************;
* SECTION 1: Hello World! - Standard SAS Output                              *;
******************************************************************************;

* the _null_ data step allows you to execute commands;
* or read a data set without creating a new data set;
data _null_;
	put 'Hello world!';
run;

* print the value of a variable to the log;
* VERY useful for debugging;
data _null_;
	x = 'Hello world!';
	put x;
	put x=;
run;

* file print writes to the open standard output;
* usually html or listing;
data _null_;
	file print;
	put 'Hello world!';
run;

* logging information levels;
* use these prefixes to print color-coded information to the log;
data _null_;
	put 'NOTE: Hello world!';
	put 'WARNING: Hello world!';
	put 'ERROR: Hello world!';
run;

* you can also use the put macro statement;
* SAS macro statements are often used for program flow control around DATA;
*   step statements and SAS procedures;
* This tutorial will only use simple macro statements;
%put Hello world!;
%put NOTE: Hello world!;
%put WARNING: Hello world!;
%put ERROR: Hello world!;

%put 'Hello world!'; /* macro variables are ALWAYS strings */

* the macro preprocessor resolves macro variables as text literals;
* before data step code is executed;
%let x = Hello world!;
%put &x;
%put '&x'; /* single quotes PREVENT macro resolution */
%put "&x"; /* double quotes ALLOW macro resolution */

******************************************************************************;
* SECTION 2 - SAS data sets                                                  *;
******************************************************************************;

*** sas data sets ************************************************************;

* the sas data set is the primary data structure in the SAS language;
* now you will make one called scratch;
* The size of data set is more typically defined by the size of the SAS data
*   set(s) from which it is created;

%let n_rows = 1000; /* define number of rows */
%let n_vars = 5;    /* define number of character and numeric variables */

* options mprint; /* to see the macro variables resolve uncomment this line */
data scratch;

  /* data sets can be made permanent by creating them in a library */
  /* syntax: data <library>.<table> */
  /* a library is like a database */
  /* a library is usually directly mapped to a filesystem directory */  
	/* since you did not specify a permanent library on the data statement */
	/* the scratch set will be created in the temporary library work */
	/* it will be deleted when you leave SAS */

	/* SAS is strongly typed - it is safest to declare variables */
	/* using a length statement - especially for character variables */
	/* $ denotes a character variable */

	/* arrays are a data structure that can exist during the data step */
	/* they are a reference to a group of variables */
	/* horizontally across a data set */
	/* $ denotes a character array */
	/* do loops are often used in conjuction with arrays */
	/* SAS arrays are indexed from 1, like R data structures */

	/* a key is a variable with a unique value for each row */

	/* mod() is the modulo function */
	/* the %eval() macro function performs math operations */
	/* before text substitution */

	/* the drop statement removes variables from the output data set */

	/* since you are not reading from a pre-existing data set */
	/* you must output rows explicitly using the output statement */

	length key 8 char1-char&n_vars $ 8 numeric1-numeric&n_vars 8;
	text_draw = 'AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG';
	array c $ char1-char&n_vars;
	array n numeric1-numeric&n_vars;
	do i=1 to &n_rows;
		key = i;
		do j=1 to %eval(&n_vars);
			/* assign a random value from text_draw */
			/* to each element of the array c */
			c[j] = scan(text_draw, floor(7*ranuni(12345)+1), ' ');
			/* assign a random numeric value to each element of the n array */
			/* ranuni() requires a seed value */
			n[j] = ranuni(%eval(&n_rows*&n_vars));
		end;
	  if mod(i, %eval(&n_rows/10)) = 0 then put 'Processing line ' i '...';
		drop i j text_draw;
		output;
	end;
	put 'Done.';
run;

* (obs=) option enables setting the number of rows to print;
proc print data=scratch (obs=5); run;

*** basic data analysis ******************************************************;

* use proc contents to understand basic information about a data set;
proc contents data=scratch;
run;

* use proc freq to analyze categorical data;
proc freq
	/* nlevels counts the discreet levels in each variable */
	/* the colon operator expands to include variable names with prefix char */
	data=scratch nlevels;
	/* request frequency bar charts for each variable */
	tables char: / plots=freqplot(type=bar);
run;

* use proc univariate to analyze numeric data;
proc univariate
	data=scratch;
	/* request univariate statistics for variables names with prefix 'numeric' */
	var numeric:;
	/* request histograms for the same variables */
	histogram numeric:;
	/* inset basic statistics on the histograms */
	inset min max mean / position=ne;
run;

*** basic data manipulation **************************************************;

* subsetting columns;
* create scratch2 set;
data scratch2;
	/* set statement reads from a pre-existing data set */
	/* no output statement is required - this is more typical */
	/* using data set options: keep, drop, etc. is often more efficient than */
	/* corresponding data step statements */
	/* : notation */
	set scratch(keep=numeric:);
run;

* print first five rows;
proc print data=scratch2(obs=5); run;

* overwrite scratch2 set;
data scratch2;
    /* ranges of vars specified using var<N> - var<M> syntax */
	set scratch(keep=char1-char&n_vars);
run;

* print first five rows;
proc print data=scratch2(obs=5); run;

* overwrite scratch2 set;
data scratch2;
	/* by name */
	set scratch(keep=key numeric1 char1);
run;

* print first five rows;
proc print data=scratch2(obs=5); run;

* subsetting and modifying columns;
* select two columns and modify them with data step functions;
* overwrite scratch2 set;
data scratch2;
	/* use length statement to ensure correct length of trans_char1 */
	/* the lag function saves the value from the row above */
	/* lag will create a numeric missing value in the first row */
	/* tranwrd finds and replaces character values */
	set scratch(keep=key char1 numeric1
		rename=(char1=new_char1 numeric1=new_numeric1));
 	length trans_char1 $8;
	lag_numeric1 = lag(new_numeric1);
	trans_char1 = tranwrd(new_char1, 'GGGGGGGG', 'foo');
run;

* print first five rows;
* notice that '.' represents numeric missing in SAS;
proc print data=scratch2(obs=5); run;

* subsetting rows;
* select only the first row and impute the missing value;
* create scratch3 set;
data scratch3;
	/* the where data set option can subset rows of data sets */
	/* there are MANY other ways to do this ... */
	set scratch2 (where=(key=1));
	lag_numeric1 = 0;
run;

* print;
proc print data=scratch3; run;

* subsetting rows;
* remove the problematic first row containing the missing value;
* from scratch2 set;
data scratch2;
	set scratch2;
	if key > 1;
run;

* print first five rows;
proc print data=scratch2(obs=5); run;

* combining data sets top-to-bottom;
* add scratch3 to the bottom of scratch2;
proc append
	base=scratch2  /* proc append does not read the base set */
	data=scratch3; /* for performance reasons base set should be largest */
run;

* sorting data sets;
* sort scratch2 in place;
proc sort
	data=scratch2;
	by key; /* you must specificy a variables to sort by */
run;

* print first five rows;
proc print data=scratch2(obs=5); run;

* sorting data sets;
* create the new scratch4 set;
proc sort
	data=scratch2
	out=scratch4; /* specifying an out set creates a new data set */
	by new_char1 new_numeric1; /* you can sort by many variables */
run;

* print first five rows;
proc print data=scratch4(obs=5); run;

* combining data sets side-by-side;
* to create messy scratch5 set;
data scratch5;
	/* merge simply attaches two or more data sets together side-by-side*/
	/* it overwrites common variables - be careful */
	merge scratch scratch4;
run;

* print first five rows;
proc print data=scratch5(obs=5); run;

* combining data sets side-by-side;
* join columns to scratch from scratch2 when key variable matches;
* to create scratch6 correctly;
data scratch6;
	/* merging with a by variable is safer */
	/* it requires that both sets be sorted */
	/* then rows are matched when key values are equal */
	/* very similar to SQL join */
	merge scratch scratch2;
	by key;
run;

* print first five rows;
proc print data=scratch6(obs=5); run;

* don't forget PROC SQL;
* nearly all common SQL statements and functions are supported by PROC SQL;
* join columns to scratch from scratch2 when key variable matches;
* to create scratch7 correctly;
proc sql noprint; /* noprint suppresses procedure output */
	create table scratch7 as
	select *
	from scratch
	join scratch2
	on scratch.key = scratch2.key;
quit;

* print first five rows;
proc print data=scratch7(obs=5); run;

* comparing data sets;
* results from data step merge with by variable and PROC SQL join;
* should be equal;
proc compare base=scratch6 compare=scratch7;
run;

* export data set;
* to default directory;
* to create a csv file;
proc export
	data=scratch7
	/* likely the correct directory for SAS University Edition */
	outfile='/folders/myfolders/sasuser.v94/scratch.csv'
	/* create a csv */
	dbms=csv
	/* replace an existing file with that name */
	replace;
run;

* import data set;
* from default directory;
* from the csv file;
* to overwrite scratch7 set;
proc import
	/* import from scratch7.csv */
	/* likely the correct directory for SAS University Edition */
	datafile='/folders/myfolders/sasuser.v94/scratch.csv'
	/* create a sas table in the work library */
	out=scratch7
	/* from a csv file */
	dbms=csv
	/* replace an existing data set with that name */
	replace;
run;

* by group processing;
* by variables can be used in the data step;
* the data set must be sorted;
* create scratch8 summary set;
data scratch8;
	set scratch4;
	by new_char1 new_numeric1;
	retain count 0; /* retained variables are remembered from row-to-row */
	if last.new_char1 then do; /* first. and last. can be used with by vars */
		count + 1; /* shorthand to increment a retained variable */
		output; /* output the last row of a sorted by group */
	end;
run;

* using PROC PRINT without the data= option prints the most recent set;
proc print; run;

* by group processing;
* by variables can be used efficiently in most procedures;
* the data set must be sorted;
proc univariate
	data=scratch4;
	var lag_numeric1;
	histogram lag_numeric1;
	inset min max mean / position=ne;
	by new_char1;
run;

* transpose;
proc transpose
	data=scratch
	out=scratch8;
run;

* print;
proc print; var _NAME_ col1-col5; run;

* transposing a sas data set can be a complex process;
* because of metadata associated with variable names;

* often, instead of simply transposing, a data set will need to be reformatted;
* in a melt/stack - column split - cast action described in Tidy Data by
* Hadley Wickham: https://www.jstatsoft.org/article/view/v059i10
* see also:
*  https://github.com/sassoftware/enlighten-apply/tree/master/SAS_UE_TidyData

******************************************************************************;
* SECTION 3 - generating analytical graphics                                 *;
******************************************************************************;

*** histograms using PROC SGPLOT *********************************************;

proc sgplot
	/* sashelp.iris is a sample data set */
	/* binwidth - bin width in terms of histogram variable */
	/* datalabel - display counts or percents for each bin */
	/* showbins - use bins to determine x-axis tickmarks */
	data=sashelp.iris;
	histogram petalwidth /
		binwidth=2
		datalabel=count
		showbins;
run;

*** bubble plots using PROC SGPLOT *******************************************;

proc sgplot
	/* group - color by a categorical variable */
	/* lineattrs - sets the bubble outline color and other outline attributes */
	data=sashelp.iris;
	bubble x=petalwidth y=petallength size=sepallength /
		group=species
		lineattrs=(color=grey);
run;

*** scatter plot with regression information using PROC SGPLOT ***************;

proc sgplot
	/* clm - confidence limits for mean predicted values */
	/* cli - prediction limits for individual predicted values */
	/* alpha - set threshold for clm and cli limits */
	data=sashelp.iris;
	reg x=petalwidth y=petallength /
	clm cli alpha=0.1;
run;

*** stacked bar chart using PROC SGPLOT **************************************;

proc sgplot
	/* sashelp.cars is a sample data set */
	/* vbar variable on x-axis */
	/* group - splits vertical bars */
	/* add title */
	data=sashelp.cars;
	vbar type / group=origin;
	title 'Car Types by Country of Origin';
run;
```

#### SAS PROC SQL - [clone/download notebook](src/notebooks/sas)
```sas

******************************************************************************;
* Copyright (C) 2017 by J. Patrick Hall, jphall@gwu.edu                      *;
*                                                                            *;
* Permission is hereby granted, free of charge, to any person obtaining a    *;
* copy of this software and associated documentation files (the "Software"), *;
* to deal in the Software without restriction, including without limitation  *;
* the rights to use, copy, modify, merge, publish, distribute, sublicense,   *;
* and/or sell copies of the Software, and to permit persons to whom the      *;
* Software is furnished to do so, subject to the following conditions:       *;
*                                                                            *;
* The above copyright notice and this permission notice shall be included    *;
* in all copies or substantial portions of the Software.                     *;
*                                                                            *;
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS    *;
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,*;
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL    *;
* THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER *;
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING    *;
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER        *;
* DEALINGS IN THE SOFTWARE.                                                  *;
******************************************************************************;

******************************************************************************;
* simple SQL operations demonstrated using SAS PROC SQL                      *;
* a *VERY BASIC* introduction to SQL                                         *;
******************************************************************************;

******************************************************************************;
* NOTE: examples are meant for the free SAS University Edition               *;
* to install see: http://www.sas.com/en_us/software/university-edition.html  *;
* Refer to part 0                                                            *;
******************************************************************************;

*** simulate some small example tables using SAS data step *******************;
* table1 has a primary key called key and two numeric variables: x1 and x2;
* table1 is located in the SAS work library, it could be called work.table1;
data table1;
	do key=1 to 20;
		x1 = key * 10;
		x2 = key + 10;
		output;
	end;
run;
proc print; run;

* table2 has a primary key called key and two character variables: x3 and x4;
* table2 is located in the SAS work library, it could be called work.table2;
data table2;
	do key=2 to 20 by 2;
		x3 = scan('a b c d e f g h i j', key/2);
		x4 = scan('k l m n o p q r s t', key/2);
		output;
	end;
run;
proc print; run;

******************************************************************************;
* SAS PROC SQL allows users to execute valid SQL statements;
* often called queries, from SAS;
* in a more typical SQL environment the proc sql and quit statements;
* would be unnecessary and unrecognized in a query;

proc sql;

 	* display basic information about table1 in the SAS log;
 	* in SQL parlance work is the database and table1 is the table;
	describe table work.table1;

quit;

proc sql;

	* display the variable x1 from table1;
	select x1 from work.table1;

quit; 	

* the NOPRINT option can be used to supress output;
* very important for large tables;
proc sql /* noprint */;

	* create table3 in the work library/database;
	* x1 from table1 will be named x5 in the new table;
	* the SQL statement as creates a temporary name or alias;
	create table table3 as
	select key, x1 as x5
	from table1;

quit;

proc sql;

	* a where clause is used to subset rows of a table;
	* the order by statement sorts displayed results or created tables;
	* desc refers to descending sort order;
	create table table4 as
	select key, x2 as x6
	from table1
	where key <= 10
	order by x6 desc;

quit;

proc sql;

	* insert can be used to add data to a table;
	insert into table1
	values (21, 210, 31);

quit;

proc sql;

	* update can be used to change the value of previously existing data;
	update table1
	set key = 6, x1 = 60, x2 = 16
	where key = 7;

quit;

proc sql; 	

	* an inner join only retains rows from both tables;
	* where key values match;
	create table table5 as
	select *
	from table1
	join table2
	on table1.key = table2.key;

quit;

proc sql;

	* left joins retain all the rows from one table;
	* and only retain rows where key values match from the other table;
	* aliases can also be used for tables;
	create table table6 as
	select *
	from table1 as t1 /* left table */
	left join table2 as t2 /* right table */
	on t1.key = t2.key;

quit;

proc sql;

	* the where statement cannot be used with aggregate functions;
	* instead use the having statement;
	* where sum_x1 > 100 would cause errors in this query;
	create table table7 as
	select key, sum(x1) as sum_x1
	from table1
	group by key
	having sum_x1 > 100;

quit;

proc sql;

	* a subquery is a query embedded in another query;
	select *
	from
	(select key, x1, x2
	from table1
	where key <= 10);

quit;
```
