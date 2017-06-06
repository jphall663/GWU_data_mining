# imports
import pandas as pd
import numpy as np
import time
import os

import sys
from operator import add
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import functions as F #https://stackoverflow.com/questions/39504950/python-pyspark-get-sum-of-a-pyspark-dataframe-column-values

from get_type_lists import get_type_lists
from target_encoder import target_encoder
from feature_combiner import feature_combiner

sc = SparkContext(appName="App")
sc.setLogLevel('WARN') #Get rid of all the junk in output
sqlContext = SQLContext(sc)
spark = SparkSession.builder \
        #.master("local") \
        .appName("App") \
        # .config("spark.some.config.option", "some-value") \
        .getOrCreate()

Y            = 'y'
ID_VAR       = 'ID'
DROPS        = [ID_VAR]
#Load data from s3
train = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3n://emr-related-files/train.csv')
test = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3n://emr-related-files/test.csv')
train.show(2)
# print(train.count)
#Work around for splitting wide data, you need to split on only an ID varaibles
#Then join back with a train varaible (bug in spark as of 2.1 with randomSplit())
(train1,valid1) = train.select(ID_VAR).randomSplit([0.7,0.3], seed=123)
valid = valid1.join(train, ID_VAR,'inner')
train = train1.join(train,ID_VAR,'inner')
print('TRAIN DATA')
train.show(2)
print('VALID DATA')
valid.show(2)

original_nums, cats = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark')



print("Encoding numberic variables...")
training_df_list, test_df_list,valid_df_list = list(),list(),list()
for i, var in enumerate(cats):
    total = len(cats)

    print('Encoding: ' + var + ' (' + str(i+1) + '/' + str(total) + ') ...')

    tr_enc,v_enc, ts_enc = target_encoder(train, test, var, Y,valid_frame=valid,frame_type='spark',id_col=ID_VAR)

    training_df_list.append(tr_enc)
    test_df_list.append(ts_enc)
    valid_df_list.append(v_enc)
#join all the new variables
for i, df in enumerate(training_df_list):
    train = train.join(training_df_list[i],ID_VAR,'inner')
    valid = valid.join(valid_df_list[i],ID_VAR,'inner')
    test = test.join(test_df_list[i],ID_VAR,'inner')

print('TRAIN DATA')
train.show(2)
print('VALID DATA')
valid.show(2)
print('TEST DATA')
test.show(2)

print('Done encoding.')


encoded_nums, cats = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark')


print('Combining features....')
(train, valid, test) = feature_combiner(train, test, encoded_nums, valid_frame = valid, frame_type='spark')
print('Done combining features.')

encoded_combined_nums, cats = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark')

################################################################################
#                 DONE WITH PREPROCESSING - START TRAINING                     #
################################################################################
import h2o
h2o.init(nthreads = -1)
h2o.show_progress()                                          # turn on progress bars
from h2o.estimators.glm import H2OGeneralizedLinearEstimator # import GLM models
from h2o.grid.grid_search import H2OGridSearch               # grid search
from pysparkling import *

hc = H2OContext.getOrCreate(spark)

print('Making h2o frames...')
trainHF = hc.as_h2o_frame(train, "trainTable")
validHF = hc.as_h2o_frame(valid, "testTable")
testHF = hc.as_h2o_frame(test, "validTable")
print('Done making h2o frames.')

base_train, stack_train = trainHF.split_frame([0.5], seed=12345)
base_valid, stack_valid = validHF.split_frame([0.5], seed=12345)

def glm_grid(X, y, train, valid):

    """ Wrapper function for penalized GLM with alpha and lambda search.

    :param X: List of inputs.
    :param y: Name of target variable.
    :param train: Name of training H2OFrame.
    :param valid: Name of validation H2OFrame.
    :return: Best H2Omodel from H2OGeneralizedLinearEstimator
    """

    alpha_opts = [0.01, 0.25, 0.5, 0.99] # always keep some L2
    hyper_parameters = {"alpha":alpha_opts}

    # initialize grid search
    grid = H2OGridSearch(
        H2OGeneralizedLinearEstimator(
            family="gaussian",
            lambda_search=True,
            seed=12345),
        hyper_params=hyper_parameters)

    # train grid
    grid.train(y=y,
               x=X,
               training_frame=train,
               validation_frame=valid)

    # show grid search results
    print(grid.show())

    best = grid.get_grid()[0]
    print(best)

    # plot top frame values
    yhat_frame = valid.cbind(best.predict(valid))
    print(yhat_frame[0:10, [y, 'predict']])

    # plot sorted predictions
    yhat_frame_df = yhat_frame[[y, 'predict']].as_data_frame()
    yhat_frame_df.sort_values(by='predict', inplace=True)
    yhat_frame_df.reset_index(inplace=True, drop=True)
    # _ = yhat_frame_df.plot(title='Ranked Predictions Plot')

    # select best model
    return best
print('Training..')
glm0 = glm_grid(original_nums, Y, base_train, base_valid)
glm1 = glm_grid(encoded_nums, Y, base_train, base_valid)
glm2 = glm_grid(encoded_combined_nums, Y, base_train, base_valid)
print('DONE training.')


# stack_train = stack_train.cbind(glm0.predict(stack_train))
# stack_valid = stack_valid.cbind(glm0.predict(stack_valid))
# stack_train = stack_train.cbind(glm1.predict(stack_train))
# stack_valid = stack_valid.cbind(glm1.predict(stack_valid))
# stack_train = stack_train.cbind(glm2.predict(stack_train))
# stack_valid = stack_valid.cbind(glm2.predict(stack_valid))
#
# test = test.cbind(glm0.predict(test))
# test = test.cbind(glm1.predict(test))
# test = test.cbind(glm2.predict(test))
#
# glm3 = glm_grid(encoded_combined_nums + ['predict', 'predict0', 'predict1'], Y, stack_train, stack_valid)
#
# sub = testHF[ID_VAR].cbind(glm3.predict(testHF))
# sub['predict'] = sub['predict'].exp()
# print(sub.head())
#
# # create time stamp
# import re
# import time
# time_stamp = re.sub('[: ]', '_', time.asctime())
#
# # save file for submission
# sub.columns = [ID_VAR, Y]
# sub_fname = '../data/submission_' + str(time_stamp) + '.csv'
# h2o.download_csv(sub, sub_fname)
