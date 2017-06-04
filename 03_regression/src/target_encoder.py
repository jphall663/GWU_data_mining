def target_encoder(training_frame, test_frame, x, y, lambda_=0.15, threshold=150, test=False, frame_type='h2o',id_col=None):

    """ Applies simple target encoding to categorical variables.

    :param training_frame: Training frame which to create target means and to be encoded.
    :param test_frame: Test frame to be encoded using information from training frame.
    :param x: Name of input variable to be encoded.
    :param y: Name of target variable to use for encoding.
    :param lambda_: Balance between level mean and overall mean for small groups.
    :param threshold: Number below which a level is considered small enough to be shrunken.
    :param test: Whether or not to print the row_val_dict for testing purposes.
    :param frame_type: The type of frame being used. Accepted: ['h2o','pandas','spark']
    :param id_col: The name of the id column for spark dataframes only. Will conserve memory and only return 3 columns in dfs(id,x,x_Tencode)
    :return: Tuple of encoded variable from train and test set as H2OFrames.

    """

    encode_name = x + '_Tencode'

    if frame_type == 'spark':
        # x_column_type = training_frame.select(x).dtypes.flatMap(list)[1]

        #To get the average out of the df have to convert to an rdd and flatMap
        #it. Then take the first and only value from the list returned.
        overall_mean = training_frame.agg({y:'avg'}).rdd.flatMap(list).first()
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
        levels_average_list = training_frame.select(x,y).rdd.map(lambda i: (i[0], i[1])).groupByKey().map(find_shrunken_averages).collect()
        # print(levels_average_list)

        from pyspark.sql.functions import lit #creates a literal value
        # create new frames with a new column
        new_training_frame, new_test_frame = None,None
        if id_col != None:
            #filter out other columns to save memory if id_col specified
            new_training_frame = training_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean))
            new_test_frame = test_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean))
        else:
            new_training_frame = training_frame.withColumn(encode_name, lit(overall_mean))
            new_test_frame = test_frame.withColumn(encode_name, lit(overall_mean))

        #Replace the values in the dataframes with new encoded values
        from pyspark.sql.functions import when
        for k,v in levels_average_list:
            new_training_frame = new_training_frame.withColumn(encode_name,
                when(new_training_frame[x] == k, v)
                .otherwise(new_training_frame[encode_name]))
            new_test_frame= new_test_frame.withColumn(encode_name,
                when(new_test_frame[x] == k, v)
                .otherwise(new_test_frame[encode_name]))

        if id_col != None:
            #remove origional x as its already in the original dfs
            return new_training_frame.drop(x), new_test_frame.drop(x)
        else:
            return new_training_frame, new_test_frame

    else:
        import h2o
        import pandas as pd
        import numpy as np

        trdf, tss = None, None
        if frame_type == 'h2o':
            # convert to pandas
            trdf = training_frame.as_data_frame().loc[:, [x,y]] # df
            tss = test_frame.as_data_frame().loc[:, x]          # series
        elif frame_type == 'pandas':
            trdf = training_frame.loc[:, [x,y]] # df
            tss = test_frame.loc[:, x]          # series


        # create dictionary of level:encode val

        overall_mean = trdf[y].mean()
        row_val_dict = {}

        for level in trdf[x].unique():
            level_df = trdf[trdf[x] == level][y]
            level_n = level_df.shape[0]
            level_mean = level_df.mean()
            if level_n >= threshold:
                row_val_dict[level] = level_mean
            else:
                row_val_dict[level] = ((1 - lambda_) * level_mean) +\
                                      (lambda_ * overall_mean)

        row_val_dict[np.nan] = overall_mean # handle missing values

        if test:
            print(row_val_dict)

        # apply the transform to training data
        trdf[encode_name] = trdf[x].apply(lambda i: row_val_dict[i])

        # apply the transform to test data
        tsdf = pd.DataFrame(columns=[x, encode_name])
        tsdf[x] = tss
        tsdf.loc[:, encode_name] = overall_mean # handle previously unseen values
        # handle values that are seen in tsdf but not row_val_dict
        for i, col_i in enumerate(tsdf[x]):
            try:
                row_val_dict[col_i]
            except:
                # a value that appeared in tsdf isn't in the row_val_dict so just
                # make it the overall_mean
                row_val_dict[col_i] = overall_mean
        tsdf[encode_name] = tsdf[x].apply(lambda i: row_val_dict[i])


        # convert back to H2O

        trdf = h2o.H2OFrame(trdf[encode_name].as_matrix())
        trdf.columns = [encode_name]

        tsdf = h2o.H2OFrame(tsdf[encode_name].as_matrix())
        tsdf.columns = [encode_name]

        return (trdf, tsdf)

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
