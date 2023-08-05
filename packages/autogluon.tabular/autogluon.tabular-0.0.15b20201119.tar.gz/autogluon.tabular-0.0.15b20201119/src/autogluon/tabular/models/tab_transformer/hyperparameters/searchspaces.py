from autogluon.core import Real, Categorical, Int

# TODO: May have to split search space's by problem type. Not necessary right now.
def get_default_searchspace():
    params = {
        'lr': Real(5e-5, 5e-3, default=1e-3, log=True),
        'weight_decay': Real(1e-6, 5e-2, default=1e-6, log=True),
        'p_dropout': Categorical(0.1, 0, 0.2, 0.3, 0.4, 0.5),
        'n_heads': Categorical(8, 2, 4),
        'hidden_dim': Categorical(128, 32, 64, 256),
        'n_layers': Categorical(1, 2, 3, 4, 5),
        'feature_dim': Int(8, 128, default=64),
        'tab_readout': Categorical('none', 'readout_emb', 'mean', 'concat_pool', 'concat_pool_all', 'concat_pool_add', 'all_feat_embs', 'mean_feat_embs'),
        'num_output_layers': Categorical(2, 1, 3),
    }

    return params.copy()
