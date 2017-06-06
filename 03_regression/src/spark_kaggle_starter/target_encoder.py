def target_encoder(training_frame, test_frame, x, y, lambda_=0.15, threshold=150, test=False, valid_frame = None,frame_type='h2o',id_col=None):

    """ Applies simple target encoding to categorical variables.

    :param training_frame: Training frame which to create target means and to be encoded.
    :param test_frame: Test frame to be encoded using information from training frame.
    :param x: Name of input variable to be encoded.
    :param y: Name of target variable to use for encoding.
    :param lambda_: Balance between level mean and overall mean for small groups.
    :param threshold: Number below which a level is considered small enough to be shrunken.
    :param test: Whether or not to print the row_val_dict for testing purposes.
    :param valid_frame: To also combine features on a validation frame include this (optional)
    :param frame_type: The type of frame being used. Accepted: ['h2o','pandas','spark']
    :param id_col: The name of the id column for spark dataframes only. Will conserve memory and only return 2 columns in dfs(id,x_Tencode)
    :return: Tuple of encoded variable from train and test set as H2OFrames.

    """

    encode_name = x + '_Tencode'

    if frame_type == 'spark':
        # x_column_type = training_frame.select(x).dtypes.flatMap(list)[1]

        #To get the average out of the df have to convert to an rdd and flatMap
        #it. Then take the first and only value from the list returned.
        overall_mean = training_frame.agg({y:'avg'}).rdd.flatMap(list).first()
        overall_mean_train = overall_mean
        #ALTERNATIVE way to do the same thing with sql functions
        # from pyspark.sql.functions import col, avg
        # overall_mean = training_frame.agg(avg(col(y))).rdd.flatMap(list).first()

        def find_shrunken_averages(tuple_input):
            """
            Reduce function to return the proper average for a given level.

            :return: A tuple of (level, ajusted_mean||overall_mean)
            """
            #The categorical level.
            level = tuple_input[0]
            # The labels list (y varaibale) from a map function.
            labels = tuple_input[1]
            # The total number of level occurances in the frame (ie count)
            level_n = len(labels)
            level_mean = sum(labels) / level_n

            # Determine if there enough occurances of a level. If NOT return overall_mean
            if level_n >= threshold:
                return(level,level_mean)
            else:
                return(level, ((1 - lambda_) * level_mean) +\
                                      (lambda_ * overall_mean) )
        #This article shows why one has to use a map-groupByKey-map rather then map-reduce order. To collect all values into one reducer
        #you have to do a groupByKey.
        #https://databricks.gitbooks.io/databricks-spark-knowledge-base/content/best_practices/prefer_reducebykey_over_groupbykey.html
        levels_average_list_train = training_frame.select(x,y).rdd.map(lambda i: (i[0], i[1])).groupByKey().map(find_shrunken_averages).collect()
        levels_average_list_valid = None
        overall_mean_valid = None
        if valid_frame:
            #update overall_mean to valid frames mean
            overall_mean_valid = valid_frame.agg({y:'avg'}).rdd.flatMap(list).first()
            overall_mean = overall_mean_valid
            levels_average_list_valid = valid_frame.select(x,y).rdd.map(lambda i: (i[0], i[1])).groupByKey().map(find_shrunken_averages).collect()
        # print(levels_average_list_train)

        from pyspark.sql.functions import lit #creates a literal value
        # create new frames with a new column
        new_training_frame, new_test_frame, new_valid_frame = None,None,None
        if id_col != None:
            #filter out other columns to save memory if id_col specified
            new_training_frame = training_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_train))
            if valid_frame:
                new_valid_frame = valid_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_valid))
                new_test_frame = test_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_valid))
            else:
                new_test_frame = test_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_train))
        else:
            new_training_frame = training_frame.withColumn(encode_name, lit(overall_mean_train))
            if valid_frame:
                new_valid_frame = valid_frame.withColumn(encode_name, lit(overall_mean_valid))
                new_test_frame = test_frame.withColumn(encode_name, lit(overall_mean_valid))
            else:
                new_test_frame = test_frame.withColumn(encode_name, lit(overall_mean_train))

        #Replace the values in the dataframes with new encoded values
        from pyspark.sql.functions import when
        for k,v in levels_average_list_train:
            new_training_frame = new_training_frame.withColumn(encode_name,
                when(new_training_frame[x] == k, v)
                .otherwise(new_training_frame[encode_name]))
            if not valid_frame:
                new_test_frame= new_test_frame.withColumn(encode_name,
                    when(new_test_frame[x] == k, v)
                    .otherwise(new_test_frame[encode_name]))
        #if we have a validation frame we want to set the test levels to the original_numerics
        #from the averaged valid frame instead of the test frame
        if valid_frame:
            for k,v in levels_average_list_valid:
                new_valid_frame = new_valid_frame.withColumn(encode_name,
                    when(new_valid_frame[x] == k, v)
                    .otherwise(new_valid_frame[encode_name]))
                new_test_frame= new_test_frame.withColumn(encode_name,
                    when(new_test_frame[x] == k, v)
                    .otherwise(new_test_frame[encode_name]))
        if id_col != None:
            #remove origional x as its already in the original dfs
            if valid_frame:
                return new_training_frame.drop(x), new_valid_frame.drop(x),new_test_frame.drop(x)
            else:
                return new_training_frame.drop(x), new_test_frame.drop(x)
        else:
            if valid_frame:
                return new_training_frame, new_valid_frame, new_test_frame
            else:
                return new_training_frame, new_test_frame

    else:
        import h2o
        import pandas as pd
        import numpy as np

        trdf, vdf, tss = None, None, None
        if frame_type == 'h2o':
            # convert to pandas
            trdf = training_frame.as_data_frame().loc[:, [x,y]] # df
            vdf = valid_frame.as_data_frame().loc[:, [x,y]] # df
            tss = test_frame.as_data_frame().loc[:, x]          # series
        elif frame_type == 'pandas':
            trdf = training_frame.loc[:, [x,y]] # df
            vdf = valid_frame.loc[:, [x,y]] # df
            tss = test_frame.loc[:, x]          # series


        # create dictionary of level:encode val

        overall_mean_train = trdf[y].mean()
        overall_mean_valid = vdf[y].mean()
        row_val_dict_train = {}
        row_val_dict_valid = {}

        for level in trdf[x].unique():
            level_df = trdf[trdf[x] == level][y]
            level_n = level_df.shape[0]
            level_mean = level_df.mean()
            if level_n >= threshold:
                row_val_dict_train[level] = level_mean
            else:
                row_val_dict_train[level] = ((1 - lambda_) * level_mean) +\
                                      (lambda_ * overall_mean_train)
        for level in vdf[x].unique():
            level_df = vdf[trdf[x] == level][y]
            level_n = level_df.shape[0]
            level_mean = level_df.mean()
            if level_n >= threshold:
                row_val_dict_valid[level] = level_mean
            else:
                row_val_dict_valid[level] = ((1 - lambda_) * level_mean) +\
                                      (lambda_ * overall_mean_valid)

        row_val_dict_train[np.nan] = overall_mean_train # handle missing values
        row_val_dict_valid[np.nan] = overall_mean_valid # handle missing values

        if test:
            print(row_val_dict_train)
            print(row_val_dict_valid)

        # apply the transform to training data
        trdf[encode_name] = trdf[x].apply(lambda i: row_val_dict_train[i])
        vdf[encode_name] = vdf[x].apply(lambda i: row_val_dict_valid[i])

        # apply the transform to test data
        tsdf = pd.DataFrame(columns=[x, encode_name])
        tsdf[x] = tss
        if valid_frame:
            tsdf.loc[:, encode_name] = overall_mean_valid # handle previously unseen values
        else:
            tsdf.loc[:, encode_name] = overall_mean_train # handle previously unseen values
        # handle values that are seen in tsdf but not row_val_dict
        for i, col_i in enumerate(tsdf[x]):
            try:
                row_val_dict_train[col_i]
            except:
                # a value that appeared in tsdf isn't in the row_val_dict so just
                # make it the overall_mean
                row_val_dict_train[col_i] = overall_mean_train

        if valid_frame:
            for i, col_i in enumerate(vdf[x]):
                try:
                    row_val_dict_valid[col_i]
                except:
                    # a value that appeared in tsdf isn't in the row_val_dict so just
                    # make it the overall_mean
                    row_val_dict_valid[col_i] = overall_mean_valid
            tsdf[encode_name] = tsdf[x].apply(lambda i: row_val_dict_valid[i])
        else:
            tsdf[encode_name] = tsdf[x].apply(lambda i: row_val_dict_train[i])



        if frame_type == 'h2o':
            # convert back to H2O
            trdf = h2o.H2OFrame(trdf[encode_name].as_matrix())
            trdf.columns = [encode_name]
            if valid_frame:
                vdf = h2o.H2OFrame(vdf[encode_name].as_matrix())
                vdf.columns = [encode_name]

            tsdf = h2o.H2OFrame(tsdf[encode_name].as_matrix())
            tsdf.columns = [encode_name]
            if valid_frame:
                return (trdf,vdf, tsdf)
            else:
                return (trdf,tsdf)
        else: #pandas
            #just return pandas
            if valid_frame:
                return (trdf,vdf, tsdf)
            else:
                return (trdf,tsdf)
#EXAMPLE OF HOW TO RUN WITH A SPARK CLUSTER
# import pandas as pd
# import numpy as np
# import time
# import os
#
# import sys
# from operator import add
# from pyspark import SparkContext
# from pyspark.sql import SparkSession
# from pyspark.sql import SQLContext
# from pyspark.sql import functions as F #https://stackoverflow.com/questions/39504950/python-pyspark-get-sum-of-a-pyspark-dataframe-column-values
#
# from get_type_lists import get_type_lists
# from target_encoder import target_encoder
#
# sc = SparkContext(appName="App")
# sqlContext = SQLContext(sc)
#
#
# Y            = 'y'
# ID_VAR       = 'ID'
# DROPS        = [ID_VAR]
#
# train = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3n://emr-related-files/train.csv')
# test = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3n://emr-related-files/test.csv')
#
# print(train.schema)
# print(train.dtypes)
#
# original_numerics, categoricals = get_type_lists(frame=train,rejects=[ID_VAR,Y],frame_type='spark') #These three have test varaibles that don't occur in the train dataset
#
#
#
# print("Encoding numberic variables...")
# training_df_list, test_df_list = list(),list()
# for i, var in enumerate(categoricals):
#     total = len(categoricals)
#
#     print('Encoding: ' + var + ' (' + str(i+1) + '/' + str(total) + ') ...')
#
#     tr_enc, ts_enc = target_encoder(train, test, var, Y,frame_type='spark',id_col=ID_VAR)
#     training_df_list.append(tr_enc)
#     test_df_list.append(ts_enc)
# #join all the new variables
# for i, df in enumerate(training_df_list):
#     train = train.join(training_df_list[i],ID_VAR,'inner')
#     test = test.join(test_df_list[i],ID_VAR,'inner')
# print(train.rdd.collect())
# print('Done encoding.')
