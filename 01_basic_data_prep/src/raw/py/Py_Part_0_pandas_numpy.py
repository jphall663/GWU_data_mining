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
# this will create 2000 row × 6 column dataset
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
