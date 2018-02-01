class DataPreperation(object):
    def __init__(self):
        pass

    @staticmethod
    def label_encoder(dataframe,columns=[],frame_type='spark'):
        """
        Converts a categorical column to numeric indexed features. Keeps the old
        columns and returns added new encoded columns (named column+'_encoded').

        Example output:
        id | gender | gender_encoded

        —-|———-|—————

        0 | M | 0.0

        1 | F | 1.0

        2 | F | 1.0

        3 | M | 0.0

        4 | M | 0.0

        5 | M | 0.0

        :param dataframe: The dataframe to encode
        :param columns: The columns to encode
        :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas', 'spark'
        return: A dataframe.
        """
        if frame_type == 'spark':
            from pyspark.ml.feature import StringIndexer

            df = dataframe

            for column in columns:
                indexer = StringIndexer(inputCol=column, outputCol=column+'_encoded')
                df = indexer.fit(df).transform(df)
            return df
        else:
            from sklearn.preprocessing import LabelEncoder

            df = None
            if frame_type == 'h2o':
                # convert to pandas
                df = dataframe.as_data_frame()
            elif frame_type == 'pandas':
                df = dataframe

            for column in columns:
                #give empty columns their own value
                df[column]=df[column].fillna(-1)
                #encode the column
                le = LabelEncoder()
                le.fit()
                le.fit(list(df[column].values))
                # Make a new encoded column
                df[column+'_encoded'] = le.transform(list(df[column].values))

            if frame_type == 'h2o':
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                df = h2o.H2OFrame(df)
                print('Done.')
                return df
            else:
                return df

    @staticmethod
    def imputer(dataframe,columns=[], type='median',frame_type='spark'):
        """
        Imputes columns given with a given imputation type.

        Spark supports: mean, median
        Pandas supports: mean, median, most_frequent

        :param dataframe: The dataframe to impute
        :param columns: The columns to impute
        :param type: The type of imputing to do
        :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas', 'spark'
        return: A dataframe.
        """
        if frame_type == 'spark':
            from pyspark.sql.functions import avg, lit, when, col

            df = dataframe
            for column in columns:
                if type == 'median':
                    # Greenwald-Khanna algorithm for finding quanitiles
                    median = df.approxQuantile(column, [0.5], 0.25)[0] # relative error - .25 is a measure of how accurate the number will be higher will be more expensive
                    df = df.withColumn(column,
                        when(col(column).isNull(), lit(median))
                        .otherwise(df[column]))
                elif type == 'mean':
                    #get the first element from list
                    mean = df.select(avg(column)).rdd.flatMap(list).collect()[0]
                    print(mean)
                    df = df.withColumn(column,
                        when(col(column).isNull(), lit(mean))
                        .otherwise(df[column]))
                else:
                    raise Exception('Type not supported. Please use a supported type.')
            return df
        else:
            from sklearn.preprocessing import Imputer

            df = None
            if frame_type == 'h2o':
                # convert to pandas
                df = dataframe.as_data_frame()
            elif frame_type == 'pandas':
                df = dataframe

            for column in columns:
                imputer = None
                if type == 'median':
                    imputer = Imputer(missing_values='NaN', #numpy nissing values
                            strategy="mean",
                            axis=0) #impute columns
                elif type == 'mean':
                    imputer = Imputer(missing_values='NaN', #numpy nissing values
                            strategy="median",
                            axis=0) #impute columns
                elif type == 'most_frequent':
                    imputer = Imputer(missing_values='NaN', #numpy nissing values
                            strategy="most_frequent",
                            axis=0) #impute columns
                else:
                    raise Exception('Type not supported. Please use a supported type.')

                df[column] = imputer.fit_transform(df[column])
            if frame_type == 'h2o':
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                df = h2o.H2OFrame(df)
                print('Done.')
                return df
            else:
                return df
    @staticmethod
    def polynomial_expansion(dataframe,columns=[], degree=3,frame_type='spark',only_return_polys=False,id_col='ID'):
        """
        Creates a polynomial expansion space based on the features. Both polynomials and interactions.

        Example Usage:
            df = DataPreperation.polynomial_expansion(df,['Col1', 'Col2'])

        :param dataframe: The dataframe to compute polynomials with
        :param columns: The columns to create polynomidals from
        :param degree: The degree to which you want to expand. degree 2 gets (x, x * x, y, x * y, y * y).
        :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas', 'spark'
        :parm string only_return_polys: will only return the new columns if set to true and not any of the orginal columns
        :parm string id_col: (required for spark) an ID column to join the frames back together
        return: A dataframe.
        """
        if(degree <2):
            raise Exception('Degree must be >= 2. Got: '+str(degree))
        if frame_type == 'spark':
            from pyspark.sql.functions import pow, col

            df = dataframe
            if only_return_polys:
                df = df.select(id_col, columns)

            for column in columns:
                for i in range(2,degree+1):
                    df = df.withColumn(column+'_'+'^'+str(i), pow(col(column), i) )
            return df
        else:
            pass

    #This is broken
    # @staticmethod
    # def polynomial_combiner(dataframe,columns=[], degree=3,frame_type='spark',only_return_polys=False,id_col='ID',sparkSession=None):
    #     """
    #     Creates a polynomial expansion space based on the features. Both polynomials and interactions.
    #
    #     :param dataframe: The dataframe to compute polynomials with
    #     :param columns: The columns to create polynomidals from
    #     :param degree: The degree to which you want to expand. degree 2 gets (x, x * x, y, x * y, y * y).
    #     :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas', 'spark'
    #     :parm string only_return_polys: will only return the new columns if set to true and not any of the orginal columns
    #     :parm string id_col: (required for spark) an ID column to join the frames back together
    #     :parm string sparkSession: (required for spark) the spark session for the application
    #     return: A dataframe.
    #     """
    #     if frame_type == 'spark':
    #         from pyspark.ml.feature import PolynomialExpansion
    #         from pyspark.ml.feature import VectorAssembler
    #
    #         df = dataframe
    #
    #         assembler = VectorAssembler(
    #             inputCols=[x for x in columns],
    #             outputCol='features')
    #         df = assembler.transform(df)
    #         df.show(2)
    #         polyExpansion = PolynomialExpansion(degree=degree, inputCol="features", outputCol="polyFeatures")
    #
    #         df = polyExpansion.transform(df)
    #         df.show(2)
    #
    #         #define a function for extracting pca vector column into their own columns
    #         def extract_vectors_with_id_col(row):
    #             """
    #             Takes a vector and extracts it into many columns from the vector.
    #             polyFeatures is the vector being extracted in this function.
    #             Vector values will be named  _2, _3, ...
    #             """
    #             # tuple(x for x in row if x not in ['pcaFeatures'])+
    #             return (row[id_col],)+tuple(float(x) for x in row.polyFeatures.values)
    #
    #
    #         def rename_columns(dataframe,new_prefix='poly_',old_colomn_starting_index=2,new_column_starting_index=1):
    #             """
    #             Takes a spark df and renames all columns to something like pca_1
    #             from the previously named columns.
    #             """
    #             old_column_index = old_colomn_starting_index
    #             new_column_index = new_column_starting_index
    #             for i in range(0,number_of_poly_features):
    #                 dataframe = dataframe.withColumnRenamed('_'+str(old_colomn_starting_index),new_prefix+str(new_column_starting_index))
    #                 old_colomn_starting_index+=1
    #                 new_column_starting_index+=1
    #             return dataframe
    #
    #         #calculate the number of terms that the expansion made
    #         number_of_poly_features = len(sparkSession.sparkContext.parallelize(df.select(id_col,'polyFeatures').rdd.top(1)).flatMap(list).collect()[1])
    #         df.show(38)
    #
    #         if only_return_polys: #only keep decompostion columns and id
    #             df = df.select(id_col,'polyFeatures').rdd.map(extract_vectors_with_id_col).toDF([id_col])
    #             df = rename_columns(df)
    #         else: #join on ID column and keep all columns
    #             df = df.rdd.map(extract_vectors_with_id_col).toDF([id_col]).join(df,id_col,'inner')
    #             df = rename_columns(df)
    #         df.show(37)
    #
    #
    #         return df.drop('polyFeatures','features')
    #     else:
    #         pass

    @staticmethod
    def get_top_correlations(dataframe,columns,frame_type='spark'):
        """
        Compute the pearson correlation between two columns and return a list of
        correlations with the highest correlations first.

        :param dataframe: The dataframe to compute correlations with
        :param columns: The columns to compute correlations on must be numeric
        :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas', 'spark'
        return: A list of dictionaries with correlations and columns ordered with highest first.
        """
        if frame_type == 'spark':
            import math
            correlation_list = []
            correlations_finished = [] #hold correlatons done to prevent repitition
            for i, col_i in enumerate(columns):
                for j, col_j in enumerate(columns):
                    if col_i+col_j not in correlations_finished: # don't repeat
                        columns = [col_i,col_j]
                        correlation = dataframe.stat.corr(col_i,col_j)
                        if math.isnan(correlation):
                            correlation=0.0
                        correlation_list.append({
                                'columns': columns,
                                'correlation': correlation,
                                'correlation_abs':math.fabs(correlation),
                            })
                        # print({
                        #     'columns': columns,
                        #     'correlation': correlation,
                        #     'correlation_abs':math.fabs(correlation),
                        # })
                        correlations_finished.append(col_i+col_j)
            #sort the list so highest correlations are first
            correlation_list = sorted(correlation_list, key=lambda x: x['correlation_abs'], reverse=True)
            return correlation_list
        else:
            pass
    @staticmethod
    def feature_combiner(training_frame, valid_frame = None, test_frame=None, columns=['X1','X2','...'],frame_type='spark'):
        """ Combines numeric features using simple arithmatic operations to create interactions terms.

        :param training_frame: Training frame from which to generate features and onto which generated feeatures will be cbound.
        :param valid_frame: (optional) To also combine features on a validation frame include this
        :param test_frame: (optional) Test frame from which to generate features and onto which generated feeatures will be cbound.
        :param columns: List of original numeric features from which to generate combined features.
        :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas', 'spark'
        return: Tuple of either (train_df, test_df) or (train_df, valid_df, test_df)
        """

        import math

        def nCr(n,r):
            f = math.factorial
            return f(n) // f(r) // f(n-r)
        total = nCr(len(columns),2)

        if frame_type == 'spark':

            train_df = training_frame

            test_df = None
            if test_frame:
                test_df = test_frame

            valid_df = None
            if valid_frame:
                valid_df = valid_frame

            completed = 1
            for i, col_i in enumerate(columns):
                for j, col_j in enumerate(columns):
                    # don't repeat (i*j = j*i)
                    if i < j:
                        print('Combining: ' + col_i + ' & ' + col_j + ' (' + str(completed) + '/' + str(total) + ')'+ '...')
                        combined_col_name = str(col_i + '|' + col_j)
                        # multiply, add a new column
                        train_df = train_df.withColumn(combined_col_name, train_df[col_i]*train_df[col_j])
                        if valid_frame:
                            valid_df = valid_df.withColumn(combined_col_name, valid_df[col_i]*valid_df[col_j])
                        if test_frame:
                            test_df = test_df.withColumn(combined_col_name, test_df[col_i]*test_df[col_j])
                        completed += 1
            print('DONE combining features.')
            if valid_frame:
                if test_frame:
                    return train_df, valid_df, test_df
                else:
                    return train_df, valid_df
            else:
                if test_frame:
                    return train_df, test_df
                else:
                    return train_df
        else:
            train_df, test_df, valid_df = None, None, None
            if frame_type == 'h2o':
                # convert to pandas
                train_df = training_frame.as_data_frame()
                if valid_frame:
                    valid_df = valid_frame.as_data_frame()
                if test_frame:
                    test_df = test_frame.as_data_frame()
            elif frame_type == 'pandas':
                train_df = training_frame
                valid_df = valid_frame
                test_df = test_frame

            completed = 1
            for i, col_i in enumerate(columns):
                for j, col_j in enumerate(columns):
                    # don't repeat (i*j = j*i)
                    if i < j:
                        print('Combining: ' + col_i + ' & ' + col_j+' (' + str(completed) + '/' + str(total) + ')'+ '...')
                        # convert to pandas
                        col_i_train_df = train_df[col_i]
                        col_j_train_df = train_df[col_j]
                        col_i_valid_df,col_j_valid_df = None,None
                        if valid_frame:
                            col_i_valid_df = valid_df[col_i]
                            col_j_valid_df = valid_df[col_j]
                        col_i_test_df, col_j_test_df = None,None
                        if test_frame:
                            col_i_test_df = test_df[col_i]
                            col_j_test_df = test_df[col_j]

                        # multiply columns together
                        train_df[str(col_i + '|' + col_j)] = col_i_train_df.values*col_j_train_df.values
                        if valid_frame:
                            valid_df[str(col_i + '|' + col_j)] = col_i_valid_df.values*col_j_valid_df.values
                        if test_frame:
                            test_df[str(col_i + '|' + col_j)] = col_i_test_df.values*col_j_test_df.values
                        completed += 1

            print('DONE combining features.')

            if frame_type == 'pandas':
                if valid_frame:
                    if test_frame:
                        return (train_df, valid_df, test_df)
                    else:
                        return (train_df, valid_df)
                else:
                    if test_frame:
                        return (train_df, test_df)
                    else:
                        return train_df
            elif frame_type == 'h2o':
                # convert back to h2o
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                training_frame = h2o.H2OFrame(train_df)
                training_frame.columns = list(train_df)
                # conserve memory
                del train_df
                validation_frame = None
                if valid_frame:
                    # convert test back to h2o
                    validation_frame = h2o.H2OFrame(valid_df)
                    validation_frame.columns = list(valid_df)
                    # conserve memory
                    del valid_df
                test_frame = None
                if test_frame:
                    # convert test back to h2o
                    test_frame = h2o.H2OFrame(test_df)
                    test_frame.columns = list(test_df)
                    # conserve memory
                    del test_df
                print('Done.')

                if valid_frame:
                    if test_frame:
                        return training_frame, validation_frame, test_frame
                    else:
                        return training_frame, validation_frame
                else:
                    if test_frame:
                        return training_frame, test_frame
                    else:
                        return training_frame

    @staticmethod
    def shrunken_averages_encoder(training_frame, valid_frame = None,test_frame=None, x='x', y='y', lambda_=0.15, perturb_range=0.05,threshold=150, test=False, frame_type='h2o',test_does_have_y=False,id_col=None,only_return_encoded=False):
        """ Applies simple target encoding to categorical variables.

        :param training_frame: Training frame which to create target means and to be encoded.
        :param valid_frame: (optional) To also combine features on a validation frame include this
        :param test_frame: (optional) Test frame to be encoded using information from training frame.
        :param x: Name of input variable to be encoded.
        :param y: Name of target variable to use for encoding.
        :param lambda_: Balance between level mean and overall mean for small groups.
        :param perturb_range: The percent range you want to perturb (enject random noise) levels. 0.05 means that the levels would be perturbed randomly inbetween -0.05% to +0.05% (set to 0 if you don't want to perturb)
        :param threshold: Number below which a level is considered small enough to be shrunken.
        :param test: Whether or not to print the row_val_dict for testing purposes.
        :param frame_type: The type of frame being used. Accepted: ['h2o','pandas','spark']
        :param bool test_does_have_y: if the test has y values. If it does then it will caculate independent averages from test frame to prevent feature leakage
        :param id_col: (spark required only) The name of the id column for spark dataframes
        :param only_return_encoded: (spark optional only) If set to true will only return the encoded columns and id_col
        :return: Tuple of 1-3 frames in order of train,valid,test
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
            # print(levels_average_list_train)

            levels_average_list_valid = None
            overall_mean_valid = None
            if valid_frame:
                #update overall_mean to valid frames mean
                overall_mean_valid = valid_frame.agg({y:'avg'}).rdd.flatMap(list).first()
                overall_mean = overall_mean_valid
                levels_average_list_valid = valid_frame.select(x,y).rdd.map(lambda i: (i[0], i[1])).groupByKey().map(find_shrunken_averages).collect()

            levels_average_list_test = None
            overall_mean_test = None
            if test_does_have_y:
                #update overall_mean to valid frames mean
                overall_mean_test = test_frame.agg({y:'avg'}).rdd.flatMap(list).first()
                overall_mean = overall_mean_test
                levels_average_list_test = test_frame.select(x,y).rdd.map(lambda i: (i[0], i[1])).groupByKey().map(find_shrunken_averages).collect()

            from pyspark.sql.functions import lit #creates a literal value
            # create new frames with a new column
            new_training_frame, new_test_frame, new_valid_frame = None,None,None
            if id_col != None:
                #filter out other columns to save memory if id_col specified
                new_training_frame = training_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_train))
                if valid_frame:
                    new_valid_frame = valid_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_valid))
                if test_does_have_y:
                    new_test_frame = test_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_test))
                else:
                    if valid_frame:
                        new_test_frame = test_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_valid))
                    else: #no valid frame so apply train means
                        new_test_frame = test_frame.select(id_col,x).withColumn(encode_name, lit(overall_mean_train))
            else:
                new_training_frame = training_frame.withColumn(encode_name, lit(overall_mean_train))
                if valid_frame:
                    new_valid_frame = valid_frame.withColumn(encode_name, lit(overall_mean_valid))
                if test_does_have_y:
                    new_test_frame = test_frame.withColumn(encode_name, lit(overall_mean_test))
                else:
                    if valid_frame:
                        new_test_frame = test_frame.withColumn(encode_name, lit(overall_mean_valid))
                    else: #no valid frame so apply train means
                        new_test_frame = test_frame.withColumn(encode_name, lit(overall_mean_train))

            #Replace the values in the dataframes with new encoded values
            from pyspark.sql.functions import when
            for k,v in levels_average_list_train:
                new_training_frame = new_training_frame.withColumn(encode_name,
                    when(new_training_frame[x] == k, v)
                    .otherwise(new_training_frame[encode_name]))
                if not test_does_have_y:
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
                    if not test_does_have_y:
                        new_test_frame= new_test_frame.withColumn(encode_name,
                            when(new_test_frame[x] == k, v)
                            .otherwise(new_test_frame[encode_name]))
            #if the test frame has its own levels
            if test_does_have_y:
                for k,v in levels_average_list_test:
                    new_test_frame= new_test_frame.withColumn(encode_name,
                        when(new_test_frame[x] == k, v)
                        .otherwise(new_test_frame[encode_name]))

            if perturb_range > 0 or perturb_range < 0:
                #This will perturb everything by the same amount udfs dont work.
                # from pyspark.sql.types import NumericType,FloatType
                # from pyspark.sql.functions import udf
                # def perturb_value(value):
                #     import numpy as np
                #     perturb_percent = np.random.uniform(low=1-perturb_range, high=1+perturb_range, size=(1))[0]
                #     return (value*perturb_percent)
                # perturb_value_udf = udf(perturb_value, FloatType())
                # new_training_frame = new_training_frame.withColumn(encode_name,perturb_value(new_training_frame[encode_name]))
                def perturb_value(tuple_input):
                    """
                    A mapper to inject random noise into each individual value.
                    """
                    id = tuple_input[0]
                    value = tuple_input[1]
                    from numpy.random import uniform
                    perturb_percent = uniform(low=1-perturb_range, high=1+perturb_range, size=(1))[0]
                    return (id, float(value*perturb_percent))
                # new_training_frame.select(encode_name).show(10)
                if training_frame:
                    #Do the transformations and perturb
                    temp_df = new_training_frame.select(id_col,encode_name).rdd.map(lambda i: (i[0], i[1])).map(perturb_value).toDF([id_col,encode_name])
                    #Join the perturbed row back onto the main set
                    new_training_frame = new_training_frame.drop(encode_name).join(temp_df,id_col,'inner')
                if valid_frame:
                    #Do the transformations and perturb
                    temp_df = new_valid_frame.select(id_col,encode_name).rdd.map(lambda i: (i[0], i[1])).map(perturb_value).toDF([id_col,encode_name])
                    #Join the perturbed row back onto the main set
                    new_valid_frame = new_valid_frame.drop(encode_name).join(temp_df,id_col,'inner')
                if test_frame:
                    #Do the transformations and perturb
                    temp_df = new_test_frame.select(id_col,encode_name).rdd.map(lambda i: (i[0], i[1])).map(perturb_value).toDF([id_col,encode_name])
                    #Join the perturbed row back onto the main set
                    new_test_frame = new_test_frame.drop(encode_name).join(temp_df,id_col,'inner')
                # new_training_frame.select(encode_name).show(10)

            if only_return_encoded:
                #remove origional x as its already in the original dfs
                if valid_frame:
                    if test_frame:
                        return new_training_frame.drop(x), new_valid_frame.drop(x),new_test_frame.drop(x)
                    else:
                        return new_training_frame.drop(x), new_valid_frame.drop(x)
                else:
                    if test_frame:
                        return new_training_frame.drop(x), new_test_frame.drop(x)
                    else:
                        return new_training_frame.drop(x)
            else:
                if valid_frame:
                    if test_frame:
                        return new_training_frame.drop(x).join(training_frame,id_col,'inner'), new_valid_frame.drop(x).join(valid_frame,id_col,'inner'), new_test_frame.drop(x).join(test_frame,id_col,'inner')
                    else:
                        return new_training_frame.drop(x).join(training_frame,id_col,'inner'), new_valid_frame.drop(x).join(valid_frame,id_col,'inner')
                else:
                    if test_frame:
                        return new_training_frame.drop(x).join(training_frame,id_col,'inner'), new_test_frame.drop(x).join(test_frame,id_col,'inner')
                    else:
                        return new_training_frame.drop(x).join(training_frame,id_col,'inner')
        else:
            import h2o
            import pandas as pd
            import numpy as np

            trdf, vdf, tsdf, tss = None, None, None, None
            if frame_type == 'h2o':
                # convert to pandas
                trdf = training_frame.as_data_frame().loc[:, [x,y]] # df
                if valid_frame:
                    vdf = valid_frame.as_data_frame().loc[:, [x,y]] # df
                if test_frame:
                    if test_does_have_y:
                        tsdf = test_frame.as_data_frame().loc[:, [x,y]] # df
                    else:
                        tss = test_frame.as_data_frame().loc[:, x]          # series
            elif frame_type == 'pandas':
                trdf = training_frame.loc[:, [x,y]] # df
                if valid_frame:
                    vdf = valid_frame.loc[:, [x,y]] # df
                if test_frame:
                    if test_does_have_y:
                        tsdf = test_frame.loc[:, [x,y]] # df
                    else:
                        tss = test_frame.loc[:, x] # series


            # create dictionary of level:encode val

            overall_mean_train = trdf[y].mean()
            overall_mean_valid = None
            if valid_frame:
                overall_mean_valid = vdf[y].mean()
            overall_mean_test = None
            if test_frame:
                if test_does_have_y:
                    overall_mean_test = tsdf[y].mean()
            row_val_dict_train = {}
            row_val_dict_valid = {}
            row_val_dict_test = {}

            for level in trdf[x].unique():
                level_df = trdf[trdf[x] == level][y]
                level_n = level_df.shape[0]
                level_mean = level_df.mean()
                if level_n >= threshold:
                    row_val_dict_train[level] = level_mean
                else:
                    row_val_dict_train[level] = ((1 - lambda_) * level_mean) +\
                                          (lambda_ * overall_mean_train)
            if valid_frame:
                for level in vdf[x].unique():
                    level_df = vdf[trdf[x] == level][y]
                    level_n = level_df.shape[0]
                    level_mean = level_df.mean()
                    if level_n >= threshold:
                        row_val_dict_valid[level] = level_mean
                    else:
                        row_val_dict_valid[level] = ((1 - lambda_) * level_mean) +\
                                              (lambda_ * overall_mean_valid)
            if test_frame:
                if test_does_have_y:
                    for level in tsdf[x].unique():
                        level_df = tsdf[tsdf[x] == level][y]
                        level_n = level_df.shape[0]
                        level_mean = level_df.mean()
                        if level_n >= threshold:
                            row_val_dict_test[level] = level_mean
                        else:
                            row_val_dict_test[level] = ((1 - lambda_) * level_mean) +\
                                                  (lambda_ * overall_mean_test)

            row_val_dict_train[np.nan] = overall_mean_train # handle missing values
            if valid_frame:
                row_val_dict_valid[np.nan] = overall_mean_valid # handle missing values
            if test_frame:
                if test_does_have_y:
                    row_val_dict_test[np.nan] = overall_mean_test # handle missing values

            if test:
                print(row_val_dict_train)
                print(row_val_dict_valid)

            from numpy.random import uniform

            # apply the transform to training data
            trdf[encode_name] = trdf[x].apply(lambda i: row_val_dict_train[i]*uniform(low=1-perturb_range, high=1+perturb_range))
            if valid_frame:
                vdf[encode_name] = vdf[x].apply(lambda i: row_val_dict_valid[i]*uniform(low=1-perturb_range, high=1+perturb_range))
            if test_frame:
                if test_does_have_y:
                    tsdf[encode_name] = tsdf[x].apply(lambda i: row_val_dict_test[i]*uniform(low=1-perturb_range, high=1+perturb_range))

            # apply the transform to test data if it doesn't have its own y values
            if test_frame:
                if not test_does_have_y:
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
                        tsdf[encode_name] = tsdf[x].apply(lambda i: row_val_dict_valid[i]*uniform(low=1-perturb_range, high=1+perturb_range))
                    else:
                        tsdf[encode_name] = tsdf[x].apply(lambda i: row_val_dict_train[i]*uniform(low=1-perturb_range, high=1+perturb_range))

            if frame_type == 'h2o':
                # convert back to H2O
                trdf = h2o.H2OFrame(trdf[encode_name].as_matrix())
                trdf.columns = [encode_name]
                if valid_frame:
                    vdf = h2o.H2OFrame(vdf[encode_name].as_matrix())
                    vdf.columns = [encode_name]
                if test_frame:
                    tsdf = h2o.H2OFrame(tsdf[encode_name].as_matrix())
                    tsdf.columns = [encode_name]
                if valid_frame:
                    if test_frame:
                        return (trdf,vdf, tsdf)
                    else:
                        return (trdf,vdf)
                else:
                    if test_frame:
                        return (trdf,tsdf)
                    else:
                        return trdf
            else: #pandas
                #just return pandas
                if valid_frame:
                    if test_frame:
                        return (trdf,vdf, tsdf)
                    else:
                        return (trdf,vdf)
                else:
                    if test_frame:
                        return (trdf,tsdf)
                    else:
                        return trdf
    @staticmethod
    def convert_boolean_to_int(frame, rejects=[],frame_type='spark'):
        """Converts all boolean types to integers.

        :param frame: The frame from which to determine types.
        :param rejects: Columns not to be converted
        :param frame_type: The type of frame being used. Accepted: ['h2o','pandas','spark']
        :return: The new dataframe
        """

        if frame_type == 'spark':
            from pyspark.sql.functions import when
            df = frame
            for column, dtype in df.dtypes:
                if column not in rejects:
                    if dtype == 'boolean':
                        df = df.withColumn(column,
                            when(df[column] == True, 1)
                            .when(df[column] == False,0)
                            .otherwise(None).cast('integer'))
            return df
        else:
            pass
    @staticmethod
    def get_type_lists(frame, rejects=['Id', 'ID','id'],frame_type='spark'):
        """Creates lists of numeric and categorical variables.

        :param frame: The frame from which to determine types.
        :param rejects: Variable names not to be included in returned lists.
        :param frame_type: The type of frame being used. Accepted: ['h2o','pandas','spark']
        :return: Tuple of lists for numeric and categorical variables in the frame.
        """

        #Handle spark type data frames
        if frame_type == 'spark':
            nums, cats = [], []
            for key, val in frame.dtypes:
                if key not in rejects:
                    if val == 'string' or val == 'boolean':
                        cats.append(key)
                    else: # ['int','double']
                        nums.append(key)
            print('Numeric =', nums)
            print()
            print('Categorical =', cats)
            return nums, cats
        else:
            nums, cats = [], []
            for key, val in frame.types.items():
                if key not in rejects:
                    if val == 'enum':
                        cats.append(key)
                    else:
                        nums.append(key)

            print('Numeric =', nums)
            print()
            print('Categorical =', cats)

            return nums, cats

    @staticmethod
    def remove_outliers_by_percentile(dataframe, columns, limits =.01, frame_type='spark'):
        """
        Remove all rows in a dataframe with columns outside of the percentiles.

        :param object df: The df to be tranformed
        :param list columns: columns to have outliers removed
        :param float limits: The percentage between 1-100 that should be removed on either side
        :param string frame_type: the frame type you want input and returned Accepted: 'h2o','spark','pandas'
        :return: the df with outlier rows removed
        """

        if frame_type == 'spark':
            import numpy as np
            df = dataframe

            def percentile_threshold(ardd, percentile):
                assert percentile > 0 and percentile <= 100, "percentile should be larger then 0 and smaller or equal to 100"
                # df.approxQuantile("x", [0.5], 0.25)
                return ardd.sortBy(lambda x: x).zipWithIndex().map(lambda x: (x[1], x[0])) \
                        .lookup(np.ceil(ardd.count() / 100 * percentile - 1))[0]

            for column in columns:
                def flatten_column(row):
                    return tuple(float(x) for x in row)
                #Compute the percentiles
                lower = percentile_threshold(df.select(column).rdd.flatMap(flatten_column),limits)
                upper = percentile_threshold(df.select(column).rdd.flatMap(flatten_column), 100 - limits)

                print('For {column} the lower limit is {lower}'.format(column=column,lower=str(lower)))
                print('For {column} the upper limit is {upper}'.format(column=column,upper=str(upper)))

                from pyspark.sql.functions import lit
                #Filter out outliers
                df = df.where("{column} < {upper} AND {column} > {lower} "\
                        .format(column=column,upper=upper,lower=lower))
            return df


        else:
            import numpy as np

            df = None
            if frame_type == 'h2o':
                # convert to pandas
                df = dataframe.as_data_frame()
            elif frame_type == 'pandas':
                df = dataframe

            for column in columns:
                ulimit = np.percentile(train_df[column].values, 100 - limits)
                llimit = np.percentile(train_df[column].values, limits)
                df[column] = df[df[column] < ulimit]
                df[column] = df[df[column] > llimit]

            if frame_type == 'h2o':
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                df = h2o.H2OFrame(df)
                print('Done.')
                return df
            else:
                return df

    @staticmethod
    def winsorize_columns(dataframe, columns, winzerize_type='percentile',limits =.01, standard_deviation_limit=3,frame_type='spark'):
        """
        Winzerize all columns specified in a dataframe.

        Must pick between type percentile and type stddev. stddev only supported by spark frames

        :param object df: The df to be tranformed
        :param list columns: columns to be winzerized
        :param string winzerize_type: The type of winserizing you want to do either percentile or stddev
        :param float limits: The percentage between 1-100 that should be winzerized on either side (for type percentile only)
        :param float standard_deviation_limit: The standard dev limits you want to remove on either side (for type stddev only)
        :param string frame_type: the frame type you want input and returned Accepted: 'h2o','spark','pandas'
        :return: the df with column(s) winzerized
        """

        if frame_type == 'spark':
            import numpy as np
            df = dataframe

            if winzerize_type == 'percentile':
                def percentile_threshold(ardd, percentile):
                    assert percentile > 0 and percentile <= 100, "percentile should be larger then 0 and smaller or equal to 100"

                    return ardd.sortBy(lambda x: x).zipWithIndex().map(lambda x: (x[1], x[0])) \
                            .lookup(np.ceil(ardd.count() / 100 * percentile - 1))[0]

                for column in columns:
                    def flatten_column(row):
                        return tuple(float(x) for x in row)
                    #Compute the percentiles
                    lower = percentile_threshold(df.select(column).rdd.flatMap(flatten_column),limits)
                    upper = percentile_threshold(df.select(column).rdd.flatMap(flatten_column), 100 - limits)

                    print('For {column} the lower limit is {lower}'.format(column=column,lower=str(lower)))
                    print('For {column} the upper limit is {upper}'.format(column=column,upper=str(upper)))

                    from pyspark.sql.functions import when
                    #Make columns greater then upper bound == to upper bound
                    df = df.withColumn(column,
                        when(df[column] > upper, upper)
                        .otherwise(df[column]))
                    #Make columns less then lower bound == to lower bound
                    df = df.withColumn(column,
                        when(df[column] < lower, lower)
                        .otherwise(df[column]))
                return df
            elif winzerize_type == 'stddev':
                def replace(df,column_to_filter,standard_deviations=3):
                    """
                    Will remove the outliers that have a stddev higher then x(param standard_deviations).

                    """
                    import math
                    #This function will flatten the row of the dataframe
                    def flatten_column(row):
                        return tuple(float(x) for x in row)
                    stats = df.select(column_to_filter).rdd.flatMap(flatten_column).stats()
                    mean = stats.mean()
                    variance = stats.variance()
                    stddev = math.sqrt(variance)
                    stddev_threshhold =  stddev*standard_deviations
                    # print(stddev_threshhold)
                    from pyspark.sql.functions import lit,abs
                    from pyspark.sql.functions import when

                    df = df.withColumn(column_to_filter,
                        when((abs(df[column_to_filter] - mean) > stddev_threshhold) & ((df[column_to_filter] - mean) > 0), (mean+stddev_threshhold))
                        .otherwise(df[column_to_filter]))
                    df = df.withColumn(column_to_filter,
                        when((abs(df[column_to_filter] - mean) > stddev_threshhold) & ((df[column_to_filter] - mean) < 0), (mean-stddev_threshhold))
                        .otherwise(df[column_to_filter]))

                    return df
                for column in columns:
                    df = replace(df,column,standard_deviation_limit)
                return df
        else:
            from scipy.stats.mstats import winsorize

            df = None
            if frame_type == 'h2o':
                # convert to pandas
                df = dataframe.as_data_frame()
            elif frame_type == 'pandas':
                df = dataframe

            for column in columns:
                df[column] = winsorize(df[column], limits = limits)

            if frame_type == 'h2o':
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                df = h2o.H2OFrame(df)
                print('Done.')
                return df
            else:
                return df

    @staticmethod
    def remove_outliers_by_std(dataframe, columns, standard_deviation_limit = 3, frame_type='spark'):
        """
        Remove rows from a dataframe that contain outliers in columns.

        :param object dataframe: the dataframe to remove outliers from
        :param list columns: the columns you want to use to calculate outliers to remove
        :param numeric standard_deviation_limit: the propertion of standard deviation that makes a column value an outlier
        :param string frame_type: the frame type you want input and returned
        :return: the df with outliers removed
        """
        if frame_type == 'spark':
            def remove(df,column_to_filter,standard_deviations=3):
                """
                Will remove the outliers that have a stddev higher then x(param standard_deviations).

                """
                import math
                #This function will flatten the row of the dataframe
                def flatten_column(row):
                    return tuple(float(x) for x in row)
                stats = df.select(column_to_filter).rdd.flatMap(flatten_column).stats()
                mean = stats.mean()
                variance = stats.variance()
                stddev = math.sqrt(variance)
                stddev_threshhold =  stddev*standard_deviations
                print(stddev_threshhold)
                from pyspark.sql.functions import lit
                df = df.where("abs({column_to_filter} - {mean}) > {stddev_threshhold}"\
                        .format(column_to_filter=column_to_filter,mean=mean,stddev_threshhold=stddev_threshhold))
                return df
            df = dataframe
            for column in columns:
                df = remove(df,column,standard_deviation_limit)
            return df
        else:
            import numpy as np

            df = None
            if frame_type == 'h2o':
                # convert to pandas
                df = dataframe.as_data_frame()
            elif frame_type == 'pandas':
                df = dataframe

            for column in columns:
                stddev = df[column].values.std(ddof=1)
                mean = stddev = df[column].values.mean()
                df[column] = df[abs(df[column] - mean) < stddev*standard_deviations]

            if frame_type == 'h2o':
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                df = h2o.H2OFrame(df)
                print('Done.')
                return df
            else:
                return df

    @staticmethod
    def create_spark_estimator_vector(df, ignore = [], out_put_column='features' ):
        """
        Creates a vector of features to use for SparkML estimators.

        :param object df: A spark data frame
        :param list ignore: list of columns that won't be used
        :param string out_put_column: the name of the output vector
        :return: The df with new vector column added
        """
        from pyspark.ml.feature import VectorAssembler
        assembler = VectorAssembler(
            inputCols=[x for x in df.columns if x not in ignore],
            outputCol=out_put_column)

        return assembler.transform(df)

    @staticmethod
    def dimensionality_reduction(train_frame,valid_frame=None,test_frame=None,columns=[],n_comp=320,random_seed=420,decompositions_to_run=['PCA','TSVD','ICA','GRP','SRP'],frame_type='spark',test_does_have_y=False,only_return_decompositions=False,id_col='ID', column_name=None):
        """
        Shrink input features in n_comp features using one or more decomposition functions.
        h2o/pandas frames supports: ['PCA','TSVD','ICA','GRP','SRP']
        spark frame supports: ['PCA','SVD']
        :param object train_frame: an input frame of the training data
        :param object valid_frame: (optional) an input frame with validation data
        :param object test_frame: (optional) an input frame of the test data
        :param list columns: the columns to decompose
        :param int n_comp: the number of features you want return (per technique)
        :param int random_seed: the random seed you want to make the decompositions with
        :param string frame_type: the frame type you want input and returned Accepted: 'h2o','spark','pandas'
        :param bool test_does_have_y: if the test has y values. If it does then it will caculate independent vectors to prevent feature leakage
        :parm bool only_return_decompositions: will only return the decompositions if set to true and not any of the orginal columns
        :parm string only_return_decompositions: will only return the decompositions if set to true and not any of the orginal columns
        :parm string id_col: (required for spark) an ID column to join the frames back together
        :parm string column_name: (optional) if you want something to come before the pca_#
        :return: Up to three frames in order train, valid, test (depends on how many frames you input)
        """
        if frame_type == 'spark':
            from pyspark.ml.feature import PCA
            from pyspark.ml.linalg import Vectors
            from pyspark.ml.feature import VectorAssembler
            # from pyspark.ml.feature import VectorDisassembler
            from pyspark.ml.feature import StandardScaler
            from pyspark.ml import Pipeline

            train_df, valid_df, test_df = None,None,None
            train_df = train_frame
            if valid_frame:
                valid_df = valid_frame
            if test_frame:
                test_df = test_frame

            assembler = VectorAssembler(
                inputCols=columns,
                outputCol="features")
            scaler = StandardScaler(inputCol=assembler.getOutputCol(),
                                    outputCol="scaledFeatures",
                                    withStd=False,
                                    withMean=True)
            pca = PCA(k=n_comp, inputCol=scaler.getOutputCol(), outputCol="pcaFeatures")
            pipeline = Pipeline(stages=[assembler,scaler, pca])

            #define a function for extracting pca vector column into their own columns
            def extract_vectors(row):
                """
                Takes a vector and extracts it into many columns from the vector.
                pcaFeatures is the vector being extracted in this function.
                Vector values will be named  _2, _3, ...
                """
                # tuple(x for x in row if x not in ['pcaFeatures'])+
                return tuple(float(x) for x in row.pcaFeatures.values)

            #define a function for extracting pca vector column into their own columns
            def extract_vectors_with_id_col(row):
                """
                Takes a vector and extracts it into many columns from the vector.
                pcaFeatures is the vector being extracted in this function.
                Vector values will be named  _2, _3, ...
                """
                # tuple(x for x in row if x not in ['pcaFeatures'])+
                return (row[id_col],)+tuple(float(x) for x in row.pcaFeatures.values)

            def rename_columns(dataframe,new_prefix='pca_',old_colomn_starting_index=2,new_column_starting_index=1):
                """
                Takes a spark df and renames all columns to something like pca_1
                from the previously named columns.
                """
                old_column_index = old_colomn_starting_index
                new_column_index = new_column_starting_index
                for i in range(0,n_comp):
                    if column_name:
                        dataframe = dataframe.withColumnRenamed('_'+str(old_colomn_starting_index),column_name+'_'+new_prefix+str(new_column_starting_index))
                    else:
                        dataframe = dataframe.withColumnRenamed('_'+str(old_colomn_starting_index),new_prefix+str(new_column_starting_index))
                    old_colomn_starting_index+=1
                    new_column_starting_index+=1
                return dataframe

            #Do PCA tranformation for training data
            model_train = pipeline.fit(train_frame)
            result_train = model_train.transform(train_frame)
            extracted_pca_train = result_train.rdd.map(extract_vectors_with_id_col).toDF([id_col])
            extracted_pca_train = rename_columns(extracted_pca_train)

            #Do PCA tranformation for validation data if it was given
            extracted_pca_valid = None
            model_valid = None #Will need this to fit test if it doesn't have y values
            if valid_frame:
                model_valid = pipeline.fit(valid_frame)
                result_valid = model_train.transform(valid_frame)
                extracted_pca_valid = result_valid.rdd.map(extract_vectors_with_id_col).toDF([id_col])
                extracted_pca_valid = rename_columns(extracted_pca_valid)

            #Do PCA tranformation for test data if it was given
            extracted_pca_test = None
            if test_frame:
                model_test = pipeline.fit(test_frame)
                result_test = model_test.transform(test_frame)
                extracted_pca_test = result_test.rdd.map(extract_vectors_with_id_col).toDF([id_col])
                extracted_pca_test = rename_columns(extracted_pca_test)
            ###
            ### SVD ###
            ###
            # https://stackoverflow.com/questions/33428589/pyspark-and-pca-how-can-i-extract-the-eigenvectors-of-this-pca-how-can-i-calcu/33500704#33500704
            # https://github.com/apache/spark/blob/master/examples/src/main/python/mllib/svd_example.py
            # https://blog.dominodatalab.com/pca-on-very-large-neuroimaging-datasets-using-pyspark/
            from pyspark.mllib.linalg.distributed import RowMatrix
            from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix
            from pyspark.mllib.linalg import DenseVector

            def extract_svd_vectors_with_id_col(row):
                """
                Takes a vector and extracts it into many columns from the vector.
                pcaFeatures is the vector being extracted in this function.
                Vector values will be named  _2, _3, ...
                """
                # tuple(x for x in row if x not in ['pcaFeatures'])+
                return (row[id_col],)+tuple(float(x) for x in row.svdFeatures.values)

            if 'SVD' in decompositions_to_run:
                #Train first
                mat = IndexedRowMatrix(result_train.rdd.map(lambda row: IndexedRow(row[id_col],DenseVector(row['pcaFeatures']))))
                svd = mat.computeSVD(n_comp, computeU=True)
                U = svd.U       # The U factor is a RowMatrix.
                s = svd.s       # The singular values are stored in a local dense vector.
                V = svd.V
                # Print vectors for testing
#                 collected = U.rows.collect()
#                 print("U factor is:")
#                 for vector in collected:
#                     print(vector)
#                 print("Singular values are: %s" % s)
#                 print("V factor is:\n%s" % V)
                extracted_svd_train = U.rows.map(lambda x: (x, )).toDF().rdd.map(lambda x: (x['_1'][0],x['_1'][1] )).toDF([id_col,'svdFeatures']).rdd.map(extract_svd_vectors_with_id_col).toDF([id_col])
                extracted_svd_train = rename_columns(extracted_svd_train,new_prefix='svd_')
                if valid_frame:
                    mat = IndexedRowMatrix(result_valid.rdd.map(lambda row: IndexedRow(row[id_col],DenseVector(row['pcaFeatures']))))
                    svd = mat.computeSVD(n_comp, computeU=True)
                    U = svd.U       # The U factor is a RowMatrix.
                    s = svd.s       # The singular values are stored in a local dense vector.
                    V = svd.V       # The V factor is a local dense matrix.
                    extracted_svd_valid = U.rows.map(lambda x: (x, )).toDF().rdd.map(lambda x: (x['_1'][0],x['_1'][1] )).toDF([id_col,'svdFeatures']).rdd.map(extract_svd_vectors_with_id_col).toDF([id_col])
                    extracted_svd_valid = rename_columns(extracted_svd_valid,new_prefix='svd_')
                if test_frame:
                    mat = IndexedRowMatrix(result_valid.rdd.map(lambda row: IndexedRow(row[id_col],DenseVector(row['pcaFeatures']))))
                    svd = mat.computeSVD(n_comp, computeU=True)
                    U = svd.U       # The U factor is a RowMatrix.
                    s = svd.s       # The singular values are stored in a local dense vector.
                    V = svd.V       # The V factor is a local dense matrix.
                    extracted_svd_test = U.rows.map(lambda x: (x, )).toDF().rdd.map(lambda x: (x['_1'][0],x['_1'][1] )).toDF([id_col,'svdFeatures']).rdd.map(extract_svd_vectors_with_id_col).toDF([id_col])
                    extracted_svd_test = rename_columns(extracted_svd_test,new_prefix='svd_')

            if only_return_decompositions:
                train_df = train_df.select(id_col)
                if valid_df:
                    train_df = valid_df.select(id_col)
                if test_df:
                    test_df = test_df.select(id_col)
            if 'PCA' in decompositions_to_run:
                train_df = extracted_pca_train.join(train_df,id_col,'inner')
                if valid_df:
                    valid_df = extracted_pca_valid.join(valid_df,id_col,'inner')
                if test_df:
                    test_df = extracted_pca_test.join(test_df,id_col,'inner')
            if 'SVD' in decompositions_to_run:
                train_df = extracted_svd_train.join(train_df,id_col,'inner')
                if valid_df:
                    valid_df = extracted_svd_valid.join(valid_df,id_col,'inner')
                if test_df:
                    test_df = extracted_svd_test.join(test_df,id_col,'inner')
            # return the right number of frames
            if valid_frame:
                if test_frame:
                    return train_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures'),valid_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures'),test_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures')
                else:
                    return train_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures'),valid_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures')
            else:
                if test_frame:
                    return train_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures'),test_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures')
                else:
                    return train_df.drop('features','scaledFeatures','pcaFeatures','svdFeatures')

        elif frame_type in ['h2o','pandas']:
            from sklearn.random_projection import GaussianRandomProjection
            from sklearn.random_projection import SparseRandomProjection
            from sklearn.decomposition import PCA, FastICA
            from sklearn.decomposition import TruncatedSVD
            import pandas as pd

            train_df, test_df, valid_df = None, None, None
            if frame_type == 'h2o':
                # convert to pandas
                train_df = train_frame.as_data_frame()
                if valid_frame:
                    valid_df = valid_frame.as_data_frame()
                test_df = test_frame.as_data_frame()
            elif frame_type == 'pandas':
                train_df = training_frame
                if valid_frame:
                    valid_df = valid_frame
                test_df = test_frame

            train_df = train_df[columns]
            if valid_frame:
                valid_df = valid_df[columns]
            test_df = test_df[columns]


            tsvd_results_train, tsvd_results_valid, tsvd_results_test = None, None, None
            if 'TSVD' in decompositions_to_run:
                tsvd = TruncatedSVD(n_components=n_comp, random_state=random_seed)
                tsvd_results_train = tsvd.fit_transform(train_df)
                tsvd_results_valid, tsvd_results_test = None, None
                if valid_frame:
                    tsvd2 = TruncatedSVD(n_components=n_comp, random_state=random_seed)
                    tsvd_results_valid = tsvd2.fit_transform(valid_df)
                    if test_frame:
                        if test_does_have_y:
                            tsvd3 = TruncatedSVD(n_components=n_comp, random_state=random_seed)
                            tsvd_results_test = tsvd3.fit_transform(test_df)
                        else:
                            tsvd_results_test = tsvd2.transform(test_df)
                else:
                    if test_frame:
                        if test_does_have_y:
                            tsvd3 = TruncatedSVD(n_components=n_comp, random_state=random_seed)
                            tsvd_results_test = tsvd3.fit_transform(test_df)
                        else:
                            tsvd_results_test = tsvd.transform(test_df)

            #PCA
            pca_results_train, pca_results_valid, pca_results_test = None, None, None
            if 'PCA' in decompositions_to_run:
                pca = PCA(n_components=n_comp, random_state=random_seed)
                pca_results_train = pca.fit_transform(train_df)
                if valid_frame:
                    pca2 = PCA(n_components=n_comp, random_state=random_seed)
                    pca_results_valid = pca2.fit_transform(valid_df)
                    if test_frame:
                        if test_does_have_y:
                            pca3 = PCA(n_components=n_comp, random_state=random_seed)
                            pca_results_test = pca3.fit_transform(test_df)
                        else:
                            pca_results_test = pca2.transform(test_df)
                else:
                    if test_frame:
                        if test_does_have_y:
                            pca3 = PCA(n_components=n_comp, random_state=random_seed)
                            pca_results_test = pca3.fit_transform(test_df)
                        else:
                            pca_results_test = pca.transform(test_df)

            # ICA
            ica_results_train, ica_results_valid, ica_results_test = None, None, None
            if 'ICA' in decompositions_to_run:
                ica = FastICA(n_components=n_comp, random_state=random_seed)
                ica_results_train = ica.fit_transform(train_df)
                if valid_frame:
                    ica2 = FastICA(n_components=n_comp, random_state=random_seed)
                    ica_results_valid = ica2.fit_transform(valid_df)
                    if test_frame:
                        if test_does_have_y:
                            ica3 = FastICA(n_components=n_comp, random_state=random_seed)
                            ica_results_test = ica3.fit_transform(test_df)
                        else:
                            ica_results_test = ica2.transform(test_df)
                else:
                    if test_frame:
                        if test_does_have_y:
                            ica3 = FastICA(n_components=n_comp, random_state=random_seed)
                            ica_results_test = ica3.fit_transform(test_df)
                        else:
                            ica_results_test = ica.transform(test_df)


            # GRP
            grp_results_train, grp_results_valid, grp_results_test = None, None, None
            if 'GRP' in decompositions_to_run:
                grp = GaussianRandomProjection(n_components=n_comp,eps=0.1, random_state=random_seed)
                grp_results_train = grp.fit_transform(train_df)
                if valid_frame:
                    grp2 = GaussianRandomProjection(n_components=n_comp,eps=0.1, random_state=random_seed)
                    grp_results_valid = grp2.fit_transform(valid_df)
                    if test_frame:
                        if test_does_have_y:
                            grp3 = GaussianRandomProjection(n_components=n_comp,eps=0.1, random_state=random_seed)
                            grp_results_test = grp3.fit_transform(test_df)
                        else:
                            grp_results_test = grp2.transform(test_df)
                else:
                    if test_frame:
                        if test_does_have_y:
                            grp3 = GaussianRandomProjection(n_components=n_comp,eps=0.1, random_state=random_seed)
                            grp_results_test = grp3.fit_transform(test_df)
                        else:
                            grp_results_test = grp.transform(test_df)

            # SRP
            srp_results_train, srp_results_valid, srp_results_test = None, None, None
            if 'SRP' in decompositions_to_run:
                srp = SparseRandomProjection(n_components=n_comp, dense_output=True, random_state=random_seed)
                srp_results_train = srp.fit_transform(train_df)
                if valid_frame:
                    srp2 = SparseRandomProjection(n_components=n_comp, dense_output=True, random_state=random_seed)
                    srp_results_valid = srp2.fit_transform(valid_df)
                    if test_frame:
                        if test_does_have_y:
                            srp3 = SparseRandomProjection(n_components=n_comp, dense_output=True, random_state=random_seed)
                            srp_results_test = srp3.fit_transform(test_df)
                        else:
                            srp_results_test = srp2.transform(test_df)
                else:
                    if test_frame:
                        if test_does_have_y:
                            srp3 = SparseRandomProjection(n_components=n_comp, dense_output=True, random_state=random_seed)
                            srp_results_test = srp3.fit_transform(test_df)
                        else:
                            srp_results_test = srp.transform(test_df)

            if only_return_decompositions:
                train_df = pd.DataFrame()
                if valid_frame:
                    valid_df = pd.DataFrame()
                if test_frame:
                    test_df = pd.DataFrame()
            for i in range(1, n_comp + 1):
                if 'PCA' in decompositions_to_run:
                    train_df['pca_' + str(i)] = pca_results_train[:, i - 1]
                    if valid_frame:
                        valid_df['pca_' + str(i)] = pca_results_valid[:, i - 1]
                    if test_frame:
                        test_df['pca_' + str(i)] = pca_results_test[:, i - 1]

                if 'ICA' in decompositions_to_run:
                    train_df['ica_' + str(i)] = ica_results_train[:, i - 1]
                    if valid_frame:
                        valid_df['pca_' + str(i)] = ica_results_valid[:, i - 1]
                    if test_frame:
                        test_df['ica_' + str(i)] = ica_results_test[:, i - 1]

                if 'TSVD' in decompositions_to_run:
                    train_df['tsvd_' + str(i)] = tsvd_results_train[:, i - 1]
                    if valid_frame:
                        valid_df['pca_' + str(i)] = tsvd_results_valid[:, i - 1]
                    if test_frame:
                        test_df['tsvd_' + str(i)] = tsvd_results_test[:, i - 1]

                if 'GRP' in decompositions_to_run:
                    train_df['grp_' + str(i)] = grp_results_train[:, i - 1]
                    if valid_frame:
                        valid_df['pca_' + str(i)] = grp_results_valid[:, i - 1]
                    if test_frame:
                        test_df['grp_' + str(i)] = grp_results_test[:, i - 1]

                if 'SRP' in decompositions_to_run:
                    train_df['srp_' + str(i)] = srp_results_train[:, i - 1]
                    if valid_frame:
                        valid_df['pca_' + str(i)] = srp_results_valid[:, i - 1]
                    if test_frame:
                        test_df['srp_' + str(i)] = srp_results_test[:, i - 1]

            if frame_type == 'pandas':
                if valid_frame:
                    if test_frame:
                        return (train_df, valid_df, test_df)
                    else:
                        return (train_df, valid_df)
                else:
                    if test_frame:
                        return (train_df, test_df)
                    else:
                        return (train_df)
            elif frame_type == 'h2o':
                # convert back to h2o
                import h2o
                print('Converting to H2OFrame ...')
                # convert train back to h2o
                training_frame = h2o.H2OFrame(train_df)
                training_frame.columns = list(train_df)
                # conserve memory
                del train_df
                testing_frame = None
                if test_frame:
                    # convert test back to h2o
                    testing_frame = h2o.H2OFrame(test_df)
                    testing_frame.columns = list(test_df)
                    # conserve memory
                    del test_df
                validation_frame = None
                if valid_frame:
                    # convert test back to h2o
                    validation_frame = h2o.H2OFrame(valid_df)
                    validation_frame.columns = list(valid_df)
                    # conserve memory
                    del valid_df

                print('Done.')

                if valid_frame:
                    if test_frame:
                        return training_frame, validation_frame, testing_frame
                    else:
                        return training_frame, validation_frame
                else:
                    if test_frame:
                        return training_frame, testing_frame
                    else:
                        return training_frame
    @staticmethod
    def pca(frame,columns=[],k=320,frame_type='spark'):
        """Computes the top `k` principal components, corresponding scores, and all eigenvalues.

        Note:
            All eigenvalues should be returned in sorted order (largest to smallest). `eigh` returns
            each eigenvectors as a column.  This function should also return eigenvectors as columns.

        Args:
            df: A Spark dataframe with a 'features' column, which (column) consists of DenseVectors.
            k (int): The number of principal components to return.

        Returns:
            tuple of (np.ndarray, RDD of np.ndarray, np.ndarray): A tuple of (eigenvectors, `RDD` of
            scores, eigenvalues).  Eigenvectors is a multi-dimensional array where the number of
            rows equals the length of the arrays in the input `RDD` and the number of columns equals
            `k`.  The `RDD` of scores has the same number of rows as `data` and consists of arrays
            of length `k`.  Eigenvalues is an array of length d (the number of features).
         """
        if frame_type == 'spark':
            # https://stackoverflow.com/questions/33428589/pyspark-and-pca-how-can-i-extract-the-eigenvectors-of-this-pca-how-can-i-calcu/33481471
            from numpy.linalg import eigh
            from pyspark.ml.linalg import Vectors
            from pyspark.ml.feature import VectorAssembler
            from pyspark.ml.feature import StandardScaler
            from pyspark.ml import Pipeline

            assembler = VectorAssembler(
                inputCols=columns,
                outputCol="features")
            scaler = StandardScaler(inputCol=assembler.getOutputCol(),
                                    outputCol="scaledFeatures",
                                    withStd=False,
                                    withMean=True)
            pipeline = Pipeline(stages=[assembler,scaler])
            model = pipeline.fit(frame)
            df = model.transform(frame)

            def estimateCovariance(df):
                """Compute the covariance matrix for a given dataframe.

                Note:
                    The multi-dimensional covariance array should be calculated using outer products.  Don't
                    forget to normalize the data by first subtracting the mean.

                Args:
                    df:  A Spark dataframe with a column named 'features', which (column) consists of DenseVectors.

                Returns:
                    np.ndarray: A multi-dimensional array where the number of rows and columns both equal the
                        length of the arrays in the input dataframe.
                """
                import numpy as np
                m = df.select(df['scaledFeatures']).map(lambda x: x[0]).mean()
                dfZeroMean = df.select(df['scaledFeatures']).map(lambda x:   x[0]).map(lambda x: x-m)  # subtract the mean

                return dfZeroMean.map(lambda x: np.outer(x,x)).sum()/df.count()

            cov = estimateCovariance(df)
            col = cov.shape[1]
            eigVals, eigVecs = eigh(cov)
            inds = np.argsort(eigVals)
            eigVecs = eigVecs.T[inds[-1:-(col+1):-1]]
            components = eigVecs[0:k]
            eigVals = eigVals[inds[-1:-(col+1):-1]]  # sort eigenvals
            score = df.select(df['scaledFeatures']).map(lambda x: x[0]).map(lambda x: np.dot(x, components.T) )

            #Show the Variance explained
            print('Vairance Explained:', sum(eigVals[0:k])/sum(eigVals) )

            # Return the `k` principal components, `k` scores, and all eigenvalues
            return components.T, score, eigVals
        elif frame_type in ['h2o','pandas']:
            raise Exception('Not Implemented yet.')
