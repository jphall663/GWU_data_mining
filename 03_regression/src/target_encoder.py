import numpy as np 
import pandas as pd 
import h2o 
 
def target_encoder(training_frame, test_frame, x, y, lambda_=0.15, threshold=150, test=False): 
 
    """ Applies simple target encoding to categorical variables. 
 
    :param training_frame: Training frame which to create target means and to be encoded. 
    :param test_frame: Test frame to be encoded using information from training frame. 
    :param x: Name of input variable to be encoded. 
    :param y: Name of target variable to use for encoding. 
    :param lambda_: Balance between level mean and overall mean for small groups. 
    :param threshold: Number below which a level is considered small enough to be shrunken. 
    :param test: Whether or not to print the row_val_dict for testing purposes. 
    :return: Tuple of encoded variable from train and test set as H2OFrames. 
 
    """ 
 
    # convert to pandas 
    trdf = training_frame.as_data_frame().loc[:, [x,y]] # df 
    tss = test_frame.as_data_frame().loc[:, x]          # series 
 
 
    # create dictionary of level:encode val 
 
    encode_name = x + '_Tencode' 
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