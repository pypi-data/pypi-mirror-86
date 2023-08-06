#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Wed 10 Jul 2019 08:42:21 PM CST

# File Name: munit.py
# Description:

"""

import torch
from torch.utils.data import DataLoader

import argparse
import numpy as np
import pandas as pd
import scanpy as sc
from anndata import AnnData
import os
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.style.use('ggplot')
sc.set_figure_params(dpi=80, figsize=(10,10), fontsize=20, frameon=False)
# sc.logging.print_versions()

from scalex.dataset import load_dataset, concat_data, preprocessing, SingleCellDataset
from scalex.sampler import splitBatchSampler
from scalex.net.vae import VAE
from scalex.net.utils import EarlyStopping
from scalex.metrics import mixingMetric, entropy_batch_mixing
from scalex.logger import create_logger
from scalex.visualize import plot_umap



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Single-Cell Analysis via Latent feature Extraction Universally')
    parser.add_argument('--name', type=str, default='')
    parser.add_argument('--batch', type=str, default='batch')
    
    parser.add_argument('--data_list', type=str, nargs='+', default=[])
    parser.add_argument('--batch_categories', type=str, nargs='+', default=None)
    parser.add_argument('--join', type=str, default='inner')
    parser.add_argument('--batch_key', type=str, default='batch')
    
    parser.add_argument('--min_genes', type=int, default=600)
    parser.add_argument('--min_cells', type=int, default=3)
    parser.add_argument('--n_top_genes', type=int, default=2000)
    parser.add_argument('--processed', action='store_true')
    
    parser.add_argument('--concat', action='store_true')
    parser.add_argument('--impute', action='store_true')
    parser.add_argument('--outdir', '-o', type=str, default='result')
    
    parser.add_argument('--lr', type=float, default=2e-4)
    parser.add_argument('--batch_size', '-b', type=int, default=64)
    parser.add_argument('-g','--gpu', type=int, default=0)
    parser.add_argument('--max_iteration', type=int, default=30000)
    parser.add_argument('--transfer', '-t', default=None)
    parser.add_argument('--repeat', action='store_true')
    parser.add_argument('--seed', type=int, default=124)
    parser.add_argument('--beta', type=float, default=0.5)
    parser.add_argument('--hid_dim', type=int, default=1024)
    parser.add_argument('--eval', action='store_true')

    args = parser.parse_args()

    np.random.seed(args.seed) # seed
    torch.manual_seed(args.seed)

    if torch.cuda.is_available(): # cuda device
        device='cuda'
        torch.cuda.set_device(args.gpu)
    else:
        device='cpu'
        
    # --------------
    #  Load Dataset
    # --------------
    if len(args.data_list)>0:
        adata = concat_data(args.data_list, args.batch_categories, join=args.join, batch_key=args.batch_key)
    else:
        adata = load_dataset(args.name)
    
        
    if args.batch != 'batch' and args.batch in adata.obs:
        adata.obs['batch'] = adata.obs[args.batch].astype('category')
    elif 'batch' not in adata.obs:
        adata.obs['batch'] = args.name
    adata.obs['batch'] = adata.obs['batch'].astype('category')
        
    if args.transfer:
        args.join = 'outer'
        args.transfer += '/'
        state = torch.load(args.transfer+'/checkpoint/config.pt')
        args.n_top_genes, enc, dec, n_domain = state['n_top_genes'], state['enc'], state['dec'], state['n_domain']
        if not args.repeat:
            outdir = os.path.join(args.transfer, 'transfer', args.name)+'/'
        else:
            outdir = os.path.join(args.outdir, args.name)+'/'
    else:
        outdir = os.path.join(args.outdir, args.name)+'/'
    os.makedirs(outdir, exist_ok=True)
    
    log = create_logger('', fh=outdir+'log.txt')
    log.info(args)
    log.info('Raw dataset shape: {}'.format(adata.shape))
        
    if not args.processed:
        adata = preprocessing(adata, 
                              min_genes=args.min_genes, 
                              min_cells=args.min_cells, 
                              n_top_genes=args.n_top_genes,
                             )
    
    scdata = SingleCellDataset(adata)  
    trainloader = DataLoader(scdata, batch_size=args.batch_size, 
                                 drop_last=True, shuffle=True, num_workers=4) # TO DO
    if not args.concat:
        batch_sampler = splitBatchSampler(args.batch_size, adata.obs['batch'], drop_last=False)
        testloader = DataLoader(scdata, batch_sampler=batch_sampler)
    else:
        testloader = DataLoader(scdata, batch_size=args.batch_size, shuffle=True, drop_last=False)
        
        
    # ----------------
    #  Training Model
    # ----------------
#     log.info('Raw dataset shape: {}'.format(adata.shape))
    log.info('Processed dataset shape: {}'.format(adata.shape))
                  
    if args.transfer:
        model = VAE(enc, dec, n_domain=n_domain)
        model.load_model(args.transfer+'/checkpoint/model.pt')
        model.to(device)
    else:
        os.makedirs(outdir+'checkpoint', exist_ok=True)
        early_stopping = EarlyStopping(patience=10, checkpoint_file=outdir+'checkpoint/model.pt')
        
        x_dim, n_domain = adata.shape[1], len(adata.obs['batch'].cat.categories)
        enc = [['fc', args.hid_dim, 1, 'relu'],['fc', 10, '', '']]  # TO DO
        dec = [['fc', x_dim, n_domain, 'sigmoid']]
        model = VAE(enc, dec, n_domain=n_domain)
        log.info('model\n'+model.__repr__())
        model.fit(trainloader, testloader=testloader,
                  lr=args.lr, 
                  max_iteration=args.max_iteration, 
                  device=device, 
                  early_stopping=early_stopping, 
                  log=log)
        torch.save({'n_top_genes':adata.var.index, 'enc':enc, 'dec':dec, 'n_domain':n_domain}, outdir+'checkpoint/config.pt')
        

    # --------------
    #  Save Results
    # --------------
    log.info('output dir: {}'.format(outdir))
    
    adata.obsm['latent'] = model.encodeBatch(testloader, device=device, eval=args.eval) # save latent rep
    if args.impute:
        adata.layers['impute'] = model.encodeBatch(testloader, out='impute', device=device)
    if args.transfer and not args.repeat:
        ref = sc.read_h5ad(args.transfer+'/adata.h5ad')
#         adata.write(outdir+'adata.h5ad', compression='gzip')
        adata = AnnData.concatenate(ref, adata, batch_categories=['reference', 'query'], 
                                    batch_key='transfer', index_unique=None)
    
    sc.pp.neighbors(adata, n_neighbors=30, use_rep='latent')
    sc.tl.umap(adata, min_dist=0.1)
    sc.tl.leiden(adata)
    #     sc.tl.louvain(adata)
    
    # pickle data
#     if args.transfer and not args.repeat:
#         adata.write(outdir+'adata_transfer.h5ad', compression='gzip')
#     else:
    adata.write(outdir+'adata.h5ad', compression='gzip')
        
    # UMAP visualization
    sc.settings.figdir = outdir
    cols = ['batch', 'donor', 'celltype', 'celltype0', 'leiden']
    color = [c for c in cols if c in adata.obs]
    if len(color) > 0:
        if args.transfer and not args.repeat:
            plot_umap(adata, by='transfer', savefig=outdir)
        else:
            sc.pl.umap(adata, color=color, save='.png', wspace=0.4, ncols=4)
    
            # metrics
            if len(adata.obs['batch'].cat.categories) > 1:
                entropy_score = entropy_batch_mixing(adata.obsm['X_umap'], adata.obs['batch'])
                log.info('entropy_batch_mixing: {:.3f}'.format(entropy_score))

            if 'celltype' in adata.obs:
                sil_score = silhouette_score(adata.obsm['X_umap'], adata.obs['celltype'].cat.codes)
                log.info("silhouette_score: {:.3f}".format(sil_score))