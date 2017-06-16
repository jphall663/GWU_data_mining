# imports
import pandas as pd
import numpy as np



def feature_combiner(training_frame, test_frame, nums, valid_frame = None,frame_type='h2o'):

    """ Combines numeric features using simple arithmatic operations.

    :param training_frame: Training frame from which to generate features and onto which generated
                           feeatures will be cbound.
    :param test_frame: Test frame from which to generate features and onto which generated
                       feeatures will be cbound.
    :param nums: List of original numeric features from which to generate combined features.
    :param valid_frame: To also combine features on a validation frame include this (optional)
    :param frame_type: The type of frame that is input and output. Accepted: 'h2o', 'pandas'
    return: Tuple of either (train_df, test_df) or (train_df, valid_df, test_df)
    """

    total = len(nums)

    if frame_type == 'spark':

        train_df = training_frame
        test_df = test_frame

        valid_df = None
        if valid_frame:
            valid_df = valid_frame

        for i, col_i in enumerate(nums):
            print('Combining: ' + col_i + ' (' + str(i+1) + '/' + str(total) + ') ...')

            for j, col_j in enumerate(nums):

                # don't repeat (i*j = j*i)
                if i < j:
                    combined_col_name = str(col_i + '|' + col_j)
                    # multiply, add a new column
                    train_df = train_df.withColumn(combined_col_name, train_df[col_i]*train_df[col_j])
                    test_df = test_df.withColumn(combined_col_name, test_df[col_i]*test_df[col_j])
                    if valid_frame:
                        valid_df = valid_df.withColumn(combined_col_name, valid_df[col_i]*valid_df[col_j])

        if valid_frame:
            return train_df, valid_df, test_df
        else:
            return train_df, test_df

        print('DONE combining features.')
    else:
        train_df, test_df, valid_df = None, None, None
        if frame_type == 'h2o':
            # convert to pandas
            train_df = training_frame.as_data_frame()
            test_df = test_frame.as_data_frame()
            valid_df = valid_frame.as_data_frame()
        elif frame_type == 'pandas':
            train_df = training_frame
            test_df = test_frame
            valid_df = valid_frame
        for i, col_i in enumerate(nums):

            print('Combining: ' + col_i + ' (' + str(i+1) + '/' + str(total) + ') ...')

            for j, col_j in enumerate(nums):

                # don't repeat (i*j = j*i)
                if i < j:

                    # convert to pandas
                    col_i_train_df = train_df[col_i]
                    col_j_train_df = train_df[col_j]
                    col_i_test_df = test_df[col_i]
                    col_j_test_df = test_df[col_j]
                    col_i_valid_df = valid_df[col_i]
                    col_j_valid_df = valid_df[col_j]

                    # multiply, convert back to h2o
                    train_df[str(col_i + '|' + col_j)] = col_i_train_df.values*col_j_train_df.values
                    test_df[str(col_i + '|' + col_j)] = col_i_test_df.values*col_j_test_df.values
                    if valid_frame:
                        valid_df[str(col_i + '|' + col_j)] = col_i_valid_df.values*col_j_valid_df.values
        print('DONE combining features.')


        if frame_type == 'pandas':
            if valid_frame:
                return (train_df, valid_df, test_df)
            else:
                return (train_df, test_df)
        elif frame_type == 'h2o':
            # convert back to h2o
            import h2o
            print('Converting to H2OFrame ...')
            # convert train back to h2o
            training_frame = h2o.H2OFrame(train_df)
            training_frame.columns = list(train_df)
            # conserve memory
            del train_df
            # convert test back to h2o
            test_frame = h2o.H2OFrame(test_df)
            test_frame.columns = list(test_df)
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
                return training_frame, validation_frame, test_frame
            else:
                return training_frame, test_frame
