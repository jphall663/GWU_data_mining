#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# specify blackboard roster as command line arg

import numpy as np
import pandas as pd
import sys
    
def main(argv):

    roster = pd.read_excel(argv[0])
    row = np.random.choice(roster.shape[0])

    name = ' '.join(['|', roster.iloc[row, 1], roster.iloc[row, 0], '!!', '|'])
    pad = '| ' + ' ' * (len(name)-4) + ' |'
    border = '-' * len(name)
    
    print('\n'.join([border, pad, name, pad, border]))
    
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    