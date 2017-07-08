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