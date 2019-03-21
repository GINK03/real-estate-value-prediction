
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.datasets import make_regression
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error as MAE
import numpy as np
import optuna
df = pd.read_csv('./encoded.csv')
y = df['yachin']
features = [c for c in df.columns if c not in ['yachin', 'country']]
x = df[features]
skf = KFold(n_splits=4)

def trainer(l1_ratio, alpha, search=True):
    dfImps = []
    maes = []
    for fold, (trn_idx, val_idx) in enumerate(skf.split(x, y)):
        x.iloc[trn_idx]
        regr = ElasticNet(random_state=0, alpha=l1_ratio, l1_ratio=alpha, max_iter=100000)
        regr.fit(x.iloc[trn_idx], y[trn_idx])
        ypred = regr.predict(x.iloc[val_idx])
        maes.append(MAE(y[val_idx], ypred))
        imps = pd.DataFrame({'features':features + ['__intercept__'], 'coefs':regr.coef_.tolist() + [regr.intercept_]})
        imps = imps.sort_values(by=['coefs'], ascending=False)
        imps['fold'] = fold
        dfImps.append(imps)
    dfImps = pd.concat(dfImps)
    dfImps = dfImps[['features', 'coefs']].groupby('features').mean().reset_index()
    if search is False:
        dfImps.sort_values(by=['coefs'], ascending=False).to_csv('imps.csv', index=None)
    return np.mean(maes)

def objective(trial):
    l1_ratio = trial.suggest_uniform('l1_ratio', 0, 1)
    alpha = trial.suggest_uniform('alpha', 0, 1)
    return trainer(l1_ratio, alpha, search=True)


study = optuna.create_study()
study.optimize(objective, n_trials=50)
print(study.best_value)
print(study.best_trial)
best_param = study.best_params
best_param['search'] = False
print('train with best param and dump features.')
print('score', trainer(**best_param))
