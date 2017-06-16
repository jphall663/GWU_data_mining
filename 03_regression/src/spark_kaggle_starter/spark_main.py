# imports
import pandas as pd
import numpy as np
import time
import os
from tabulate import tabulate

import sys
from operator import add
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import functions as F #https://stackoverflow.com/questions/39504950/python-pyspark-get-sum-of-a-pyspark-dataframe-column-values

from get_type_lists import get_type_lists
from target_encoder import target_encoder
from feature_combiner import feature_combiner

from logging_lib.LoggingController import LoggingController

#Define your s3 bucket to load and store data
S3_BUCKET = 'emr-related-files'

#Create a custom logger to log statistics and plots
logger = LoggingController()
logger.s3_bucket = S3_BUCKET

#.config('spark.executor.cores','6') \
spark = SparkSession.builder \
        .appName("App") \
        .getOrCreate()
        # .master("local[*]") \
        # .config('spark.cores.max','16')
        #.master("local") \
        # .config("spark.some.config.option", "some-value") \

spark.sparkContext.setLogLevel('WARN') #Get rid of all the junk in output

Y            = 'y'
ID_VAR       = 'ID'
DROPS        = [ID_VAR]
#From an XGBoost model
# NOTE the top 6 are categorical, might want to look into this.
MOST_IMPORTANT_VARS_ORDERD = ['X5','X0','X8','X3','X1','X2','X314','X47','X118',\
'X315','X29','X127','X236','X115','X383','X152','X151','X351','X327','X77','X104',\
'X267','X95','X142']
#Load data from s3
train = spark.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3n://'+S3_BUCKET+'/train.csv')
test = spark.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3n://'+S3_BUCKET+'/test.csv')
#this needs to be done for h2o glm.predict() bug (which needs same number of columns)
test = test.withColumn(Y,test[ID_VAR])


#Work around for splitting wide data, you need to split on only an ID varaibles
#Then join back with a train varaible (bug in spark as of 2.1 with randomSplit())
(train1,valid1) = train.select(ID_VAR).randomSplit([0.7,0.3], seed=123)
valid = valid1.join(train, ID_VAR,'inner')
train = train1.join(train,ID_VAR,'inner')
# print('TRAIN DATA')
# train.show(2)
# print('VALID DATA')
# valid.show(2)

#workdaround for h2o predict
test1 = test.select(ID_VAR,Y)
test2 = test.drop(Y)
test = test1.join(test2,ID_VAR,'inner')


original_nums, cats = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark')



print("Encoding numberic variables...")
training_df_list, test_df_list,valid_df_list = list(),list(),list()
for i, var in enumerate(cats):
    total = len(cats)

    print('Encoding: ' + var + ' (' + str(i+1) + '/' + str(total) + ') ...')
    logger.log_string('Encoding: ' + var + ' (' + str(i+1) + '/' + str(total) + ') ...')

    tr_enc,v_enc, ts_enc = target_encoder(train, test, var, Y,valid_frame=valid,frame_type='spark',id_col=ID_VAR)

    training_df_list.append(tr_enc)
    test_df_list.append(ts_enc)
    valid_df_list.append(v_enc)
#join all the new variables
for i, df in enumerate(training_df_list):
    train = train.join(training_df_list[i],ID_VAR,'inner')
    valid = valid.join(valid_df_list[i],ID_VAR,'inner')
    test = test.join(test_df_list[i],ID_VAR,'inner')

# print('TRAIN DATA')
# train.show(2)
# print('VALID DATA')
# valid.show(2)
# print('TEST DATA')
# test.show(2)

print('Done encoding.')


encoded_nums, cats = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark')

#Remplace cats with encoded cats from MOST_IMPORTANT_VARS_ORDERD
for i, v in enumerate(MOST_IMPORTANT_VARS_ORDERD):
    if v in cats:
        MOST_IMPORTANT_VARS_ORDERD[i] = v + '_Tencode'

#
# print('Combining features....')
# (train, valid, test) = feature_combiner(train, test, MOST_IMPORTANT_VARS_ORDERD, valid_frame = valid, frame_type='spark')
# print('Done combining features.')
#
# encoded_combined_nums, cats = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark')

################################################################################
#                 DONE WITH PREPROCESSING - START TRAINING                     #
################################################################################
import h2o
h2o.show_progress()                                          # turn on progress bars
from h2o.estimators.glm import H2OGeneralizedLinearEstimator # import GLM models
from h2o.estimators.deeplearning import H2ODeepLearningEstimator
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator
from h2o.grid.grid_search import H2OGridSearch               # grid search
from h2o.estimators.xgboost import H2OXGBoostEstimator
from h2o.estimators.stackedensemble import H2OStackedEnsembleEstimator
import xgboost as xgb
import matplotlib
matplotlib.use('Agg')                                       #Need this if running matplot on a server w/o display
from pysparkling import *

conf = H2OConf(spark=spark)
conf.nthreads = -1
hc = H2OContext.getOrCreate(spark,conf)


print('Making h2o frames...')
trainHF = hc.as_h2o_frame(train, "trainTable")
validHF = hc.as_h2o_frame(valid, "validTable")
testHF = hc.as_h2o_frame(test, "testTable")
print('Done making h2o frames.')

logger.log_string("Train Summary:")
logger.log_string("Rows:{}".format(trainHF.nrow))
logger.log_string("Cols:{}".format(trainHF.ncol))
# print(trainHF.summary(return_data=True))
# logger.log_string(tabulate(trainHF.summary(return_data=True),tablefmt="grid"))
# logger.log_string(trainHF._ex._cache._tabulate('grid',False))

base_train, stack_train = trainHF.split_frame([0.5], seed=12345)
base_valid, stack_valid = validHF.split_frame([0.5], seed=12345)

# def upload_submission(sub,predict_column='predict'):
#     # create time stamp
#     import re
#     import time
#     time_stamp = re.sub('[: ]', '_', time.asctime())
#
#     # save file for submission
#     # sub.columns = [ID_VAR, Y]
#     sub_fname = 'Submission_'+str(time_stamp) + '.csv'
#     # h2o.download_csv(sub, 's3n://'+S3_BUCKET+'/kaggle_submissions/Mercedes/' +sub_fname)
#
#     spark_sub_frame = hc.as_spark_frame(sub)
#
#     spark_sub_frame.select(ID_VAR,predict_column).coalesce(1).write.option("header","true").csv('s3n://'+S3_BUCKET+'/Kaggle_Submissions/Mercedes/' +sub_fname)

def glm_grid(X, y, train, valid, should_submit = False):
    """ Wrapper function for penalized GLM with alpha and lambda search.

    :param X: List of inputs.
    :param y: Name of target variable.
    :param train: Name of training H2OFrame.
    :param valid: Name of validation H2OFrame.
    :return: Best H2Omodel from H2OGeneralizedLinearEstimator
    """

    alpha_opts = [0.01, 0.25, 0.5, 0.99] # always keep some L2
    family = ["gaussian", "binomial", "quasibinomial", "multinomial", "poisson", "gamma", "tweedie"]
    hyper_parameters = {"alpha":alpha_opts
                        }

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
    # if should_submit:
    #     sub_frame = testHF[ID_VAR].cbind(best.predict(testHF))
    #     print(sub_frame.col_names)
    #     print('Submission frame preview:')
    #     print(sub_frame[0:10, [ID_VAR, 'predict']])
    #     upload_submission(sub_frame,'predict')
    # plot top frame values
    print('yhat_frame')
    yhat_frame = valid.cbind(best.predict(valid))
    print(yhat_frame[0:10, [y, 'predict']])

    # plot sorted predictions
    yhat_frame_df = yhat_frame[[y, 'predict']].as_data_frame()
    yhat_frame_df.sort_values(by='predict', inplace=True)
    yhat_frame_df.reset_index(inplace=True, drop=True)
    plt = yhat_frame_df.plot(title='Ranked Predictions Plot')
    logger.log_string('Ranked Predictions Plot')
    logger.log_matplotlib_plot(plt)

    # select best model
    return best
def neural_net_grid(X, y, train, valid):
    # define random grid search parameters
    hyper_parameters = {'hidden': [[170, 320], [80, 190], [320, 160, 80], [100], [50, 50, 50, 50]],
                        'l1':[s/1e4 for s in range(0, 1000, 100)],
                        'l2':[s/1e5 for s in range(0, 1000, 100)],
                        'input_dropout_ratio':[s/1e2 for s in range(0, 20, 2)]}

    # define search strategy
    search_criteria = {'strategy':'RandomDiscrete',
                       'max_models':100,
                       'max_runtime_secs':60*60*2,  #2 hours
                       }

    # initialize grid search
    gsearch = H2OGridSearch(H2ODeepLearningEstimator,
                            hyper_params=hyper_parameters,
                            search_criteria=search_criteria)

    # execute training w/ grid search
    gsearch.train(x=X,
                  y=y,
                  training_frame=train,
                  validation_frame=valid,
                  activation='TanhWithDropout',
                  epochs=2000,
                  stopping_rounds=20,
                  sparse=True, # handles data w/ many zeros more efficiently
                  ignore_const_cols=True,
                  adaptive_rate=True)
    best_model = gsearch.get_grid()[0]

    return best_model

def gboosting_grid(X, y, train, valid):
    # define random grid search parameters
    hyper_parameters = {'ntrees':list(range(0, 500, 50)),
                        'max_depth':list(range(0, 20, 2)),
                        'sample_rate':[s/float(10) for s in range(1, 11)],
                        'col_sample_rate':[s/float(10) for s in range(1, 11)]}

    # define search strategy
    search_criteria = {'strategy':'RandomDiscrete',
                       'max_models':100,
                       'max_runtime_secs':60*60*2,  #2 hours
                       }

    # initialize grid search
    gsearch = H2OGridSearch(H2OGradientBoostingEstimator,
                            hyper_params=hyper_parameters,
                            search_criteria=search_criteria)

    # execute training w/ grid search
    gsearch.train(x=X,
                  y=y,
                  training_frame=train,
                  validation_frame=valid)

    best_model = gsearch.get_grid()[0]

    return best_model


h2o_xgb_model = H2OXGBoostEstimator(
    ntrees = 10000,
    learn_rate = 0.005,
    sample_rate = 0.1,
    col_sample_rate = 0.8,
    max_depth = 5,
    nfolds = 3,
    keep_cross_validation_predictions=True,
    stopping_rounds = 10,
    seed = 12345)

# execute training
h2o_xgb_model.train(x=encoded_combined_nums,
                    y=Y,
                    training_frame=trainHF,
                    validation_frame=validHF)

print('Training..')
logger.log_string('glm0')
glm0 = glm_grid(original_nums, Y, base_train, base_valid)
logger.log_string('glm1')
glm1 = glm_grid(encoded_nums, Y, base_train, base_valid)
logger.log_string('glm2')
glm2 = glm_grid(encoded_combined_nums, Y, base_train, base_valid)
#
# logger.log_string('rnn0')
# rnn0 = neural_net_grid(original_nums, Y, base_train, base_valid)
# logger.log_string('rnn1')
# rnn1 = neural_net_grid(encoded_nums, Y, base_train, base_valid)
# logger.log_string('rnn2')
# rnn2 = neural_net_grid(encoded_combined_nums, Y, base_train, base_valid)
#
# logger.log_string('gbm0')
# gbm0 = gboosting_grid(original_nums, Y, base_train, base_valid)
# logger.log_string('gbm1')
# gbm1 = gboosting_grid(encoded_nums, Y, base_train, base_valid)
# logger.log_string('gbm2')
# gbm2 = gboosting_grid(encoded_combined_nums, Y, base_train, base_valid)
print('DONE training.')


stack_train = stack_train.cbind(glm0.predict(stack_train))
stack_valid = stack_valid.cbind(glm0.predict(stack_valid))
stack_train = stack_train.cbind(glm1.predict(stack_train))
stack_valid = stack_valid.cbind(glm1.predict(stack_valid))
stack_train = stack_train.cbind(glm2.predict(stack_train))
stack_valid = stack_valid.cbind(glm2.predict(stack_valid))

#
# stack_train = stack_train.cbind(rnn0.predict(stack_train))
# stack_valid = stack_valid.cbind(rnn0.predict(stack_valid))
# stack_train = stack_train.cbind(rnn1.predict(stack_train))
# stack_valid = stack_valid.cbind(rnn1.predict(stack_valid))
# stack_train = stack_train.cbind(rnn2.predict(stack_train))
# stack_valid = stack_valid.cbind(rnn2.predict(stack_valid))
#
# stack_train = stack_train.cbind(gbm0.predict(stack_train))
# stack_valid = stack_valid.cbind(gbm0.predict(stack_valid))
# stack_train = stack_train.cbind(gbm1.predict(stack_train))
# stack_valid = stack_valid.cbind(gbm1.predict(stack_valid))
# stack_train = stack_train.cbind(gbm2.predict(stack_train))
# stack_valid = stack_valid.cbind(gbm2.predict(stack_valid))


testHF = testHF.cbind(glm0.predict(testHF))
testHF = testHF.cbind(glm1.predict(testHF))
testHF = testHF.cbind(glm2.predict(testHF))
# testHF = testHF.cbind(rnn0.predict(testHF))
# testHF = testHF.cbind(rnn1.predict(testHF))
# testHF = testHF.cbind(rnn2.predict(testHF))
# testHF = testHF.cbind(gbm0.predict(testHF))
# testHF = testHF.cbind(gbm1.predict(testHF))
# testHF = testHF.cbind(gbm2.predict(testHF))

logger.log_string('glm3')
# glm3 = glm_grid(encoded_combined_nums + ['predict', 'predict0','predict1'], Y, stack_train, stack_valid, should_submit=True)
rnn = neural_net_grid(MOST_IMPORTANT_VARS_ORDERD + ['predict', 'predict0', 'predict1','predict2', 'predict3', 'predict4','predict5', 'predict6', 'predict7'], Y, stack_train, stack_valid)




sub = testHF[ID_VAR].cbind(rnn.predict(testHF))
print(sub.head())


# create time stamp
import re
import time
time_stamp = re.sub('[: ]', '_', time.asctime())

# save file for submission
sub.columns = [ID_VAR, Y]
sub_fname = 'Submission_'+str(time_stamp) + '.csv'
# h2o.download_csv(sub, 's3n://'+S3_BUCKET+'/kaggle_submissions/Mercedes/' +sub_fname)

spark_sub_frame = hc.as_spark_frame(sub)

spark_sub_frame.select(ID_VAR,Y).coalesce(1).write.option("header","true").csv('s3n://'+S3_BUCKET+'/Kaggle_Submissions/Mercedes/' +sub_fname)
