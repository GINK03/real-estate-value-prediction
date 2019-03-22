# Real Estate Value Prediction
Awesome real estate value prediction with machine-learnings.

## 序
 - 機械学習で不動産を予想する意味  
  特徴量から重要度を知ることができる
  
 - EndUserにとって嬉しいこととは？  
  Chrome Extentionなどでその情報の正当性を推し量る事ができる
  
## 破

### データを集める  
 - ダウンロード済みのデータはこちら[Link](https://www.dropbox.com/s/a1jc2hoed3bxnvp/data.tar.gz?dl=0)
 
### モデルを検討する
 - ElasticNetを利用  
ElasticNetはL1, L2の正則化をあわせた線形モデルで、オーバーフィットを強力に避けて、予想するアルゴリズム  

```
1 / (2 * n_samples) * ||y - w*x||^2
+ alpha * l1_ratio * ||w||
+ 0.5 * alpha * (1 - l1_ratio) * ||w||^2
```
目的関数はこのように定義され、alpha, l1_ratioのパラメータを自由に設定することでCross-Validationの性能を確認することができる
 
 - 独立な情報でone-hotベクトルを仮定  
線形モデルは事象が可能な限り独立であると嬉しく、特に特徴量の重要度を知りたい場合、categoricalな変数がone-hotベクトルで表現されている方が、continiusな値の係数を出すより解釈性能として優れる（これは性能とトレードオフの場合がある） 
 
 - optunaで最適化
 alpha, l1_ratioは自由に決められる 0 ~ 1の値なので、探索する値の対象となる。  
 [optuna](https://optuna.org/)というライブラリが超楽に探索できる
 
```python
def objective(trial):
    l1_ratio = trial.suggest_uniform('l1_ratio', 0, 1)
    alpha = trial.suggest_uniform('alpha', 0, 1)
    loss = trainer(l1_ratio, alpha) # <- 具体的なfoldをとって計算するコード
    return loss
```
このように目的関数を定義して、最適化の対象となる変数を必要なだけ作成する 
 
### 東京と全国でモデルを分ける
TODO
 
### Chrome Extentionを作る
TODO:@hayashi
 
## 分析結果
 - 東京23区の一般的な特徴量（部屋の種類、何区、設備など）からt-sneを行うと、クラスタが分かれるより連続している事がわかる  
<div align="center">
   <img width="500px" src="https://user-images.githubusercontent.com/4949982/54764073-69e5e900-4c3a-11e9-9fb8-63f9175cbf68.png">
</div> 

 - 東京23区の一万円あたりで借りられる面積のバイオリン図
<div align="center">
    <img width="100%" src="https://user-images.githubusercontent.com/4949982/54757849-65b3ce80-4c2e-11e9-992e-e92db27fa6fe.png">
</div>

 - 都道府県の一万円あたりで借りられる面積のバイオリン図
<div align="center">
   <img width="100%" src="https://user-images.githubusercontent.com/4949982/54755783-1370ae80-4c2a-11e9-8bc5-b6b0b23a677b.png">
</div>
 
## 急
 - 東京の結果
<div align="center">
   <img width="100%" src="https://user-images.githubusercontent.com/4949982/54759796-25564f80-4c32-11e9-8919-c6d964ba751b.png">
 <div>細かいので拡大して閲覧してください</div>
</div>

 - 全国の結果  
 <div align="center">
   <img width="100%" src="https://user-images.githubusercontent.com/4949982/54760160-dceb6180-4c32-11e9-9b5f-9bfddfa9e7fc.png">
 <div>細かいので拡大して閲覧してください</div>
</div>

 
 - Chrome Extentionのユースケース
 
 - 価格差が大きいとはなにか例外があるということ  
 
