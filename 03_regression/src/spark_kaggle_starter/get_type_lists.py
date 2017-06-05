def get_type_lists(frame, rejects=['Id', 'ID','id'],frame_type='h2o'):

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
                if val == 'string':
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
