#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Tue 19 Nov 2019 04:23:35 PM CST

# File Name: sampler.py
# Description:

"""

import numpy as np
from torch.utils.data.sampler import Sampler
                
                
class splitBatchSampler(Sampler):
    """
    split multi-datasets Batch Sampler
    One batch of sampled data is from the same dataset.
    """
    def __init__(self, batch_size, batch_id, drop_last=False):
        self.batch_size = batch_size
        self.drop_last = drop_last
        self.batch_id = batch_id

    def __iter__(self):
        batch = {}
        sampler = np.random.permutation(len(self.batch_id))
        for idx in sampler:
            c = self.batch_id[idx]
            if c not in batch:
                batch[c] = []
            batch[c].append(idx)

            if len(batch[c]) == self.batch_size:
                yield batch[c]
                batch[c] = []

        for c in batch.keys():
            if len(batch[c]) > 0 and not self.drop_last:
                yield batch[c]
            
    def __len__(self):
        if self.drop_last:
            return len(self.batch_id) // self.batch_size
        else:
            return (len(self.batch_id)+self.batch_size-1) // self.batch_size
        
        
class concatBatchSampler(Sampler):
    """
    concat multi-datasets Batch Sampler
    """
    def __init__(self, batch_size, batch_id, drop_last=False):
        self.batch_size = batch_size
        self.drop_last = drop_last
        self.batch_id = batch_id
        
        indices_ = []
        for b in np.unique(self.batch_id):
            indices = np.where(self.batch_id==b)[0]
            indices_.append(indices)

        self.num_samples = max([len(indices) for indices in indices_])
        self.indices_ = indices_

    def __iter__(self):            
        batch = []
        samplers = [indices[np.random.permutation(len(indices))] for indices in self.indices_]
        for i in range(self.num_samples):
            for sampler in samplers:
                idx = sampler[i]
                batch.append(idx)
            if len(batch) == self.batch_size * len(self.indices_):
                yield batch
                batch = []
        if len(batch) > 0 and not self.drop_last:
            yield batch
                
    def __len__(self):
        if self.drop_last:
            return self.num_samples // self.batch_size
        else:
            return (self.num_samples+self.batch_size-1) // self.batch_size